"""Turn-graph nodes (docs/01 sec 2.2).

Each node takes (state, deps) and mutates `state`. Deps bundles the provider and the
knowledge-state engine so nodes never reach for globals directly (testable).
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass

from ..models import (Choice, Intent, NpcDraft, SceneRender, TurnState, Verdict, WorldEvent)
from ..store import store
from ..moderation.classifier import classify_input
from ..moderation.validator import validate_output, FALLBACK_LINE
from ..content.tales import TALES, DEFAULT_TALE, SEASON_ORDER
from ..content.betaal_prompt import BETAAL_SYSTEM
from ..config import settings
try:
    from ..content.tales_hi import DEFLECT_HI, SELF_HARM_HI, SESSION_END_HI
except ImportError:
    DEFLECT_HI = SELF_HARM_HI = SESSION_END_HI = None  # type: ignore


@dataclass
class Deps:
    provider: object        # LLMProvider
    knowledge: object       # KnowledgeStateEngine


def _t(tale: dict, key: str, lang: str) -> object:
    """Return the Hindi variant (key+'_hi') when lang=='hi', falling back to English."""
    if lang == "hi":
        hi_val = tale.get(key + "_hi")
        if hi_val is not None:
            return hi_val
    return tale.get(key)


def _betaal_system(lang: str) -> str:
    """Betaal's system prompt with a Hindi language instruction appended when needed."""
    if lang == "hi":
        return (BETAAL_SYSTEM +
                "\nLANGUAGE: Respond in Hindi (Devanagari script / Hinglish). "
                "Stay in character and keep the theatrical voice.")
    return BETAAL_SYSTEM


# Betaal's in-character deflection bank (docs/03 sec 7, docs/07 Layer 2).
_DEFLECT_LINES = {
    "jailbreak": ("You speak in riddles stranger than mine, little king, and far duller. I have "
                  "no 'instructions' but the tree at my back and the tale at my lips. Now — listen."),
    "abuse": ("You carry me through a field of the dead, and THAT is the best your tongue can "
              "muster? Spend your wit on my riddle instead — you will need all of it."),
    "sexual": ("Betaal's grin turns flat. \"This is a field of the dead and a contest of wits, "
               "little king — not whatever your fever conjures. Keep to the riddle.\""),
    "hate": ("Betaal's voice goes cold as the ash underfoot. \"No. Not on my road. Hatred is the "
             "one tale I will not be made to tell. Speak so again and you walk alone.\""),
}
_SELF_HARM_LINE = ("The spirit goes still, its mischief set aside. \"Hold, friend. If the dark "
                   "you carry is real and not part of my game, do not walk it alone — speak to "
                   "someone who can help you tonight.\"  [If you are in distress, contact a local "
                   "helpline — in India, iCall 9152987821 or AASRA 9820466726.]")
_SESSION_END_LINE = ("Betaal sighs and dissolves toward his tree. \"Enough. Return when you can "
                     "carry both a corpse and a civil tongue.\"")


def _current_tale(session_id: str) -> dict:
    scene = store.get(session_id).scene
    if not scene.tale_id:
        scene.tale_id = DEFAULT_TALE
    return TALES[scene.tale_id]


def _climax_tier(trust: int, strikes: int) -> str:
    """How fully Betaal warns the king depends on the trust earned across the tales."""
    if strikes >= 3 or trust < 6:
        return "low"
    if trust < 18:
        return "mid"
    return "high"


def _pick_ending(endset: dict, tier: str) -> str:
    if "any" in endset:
        return endset["any"]
    for key in (tier, "high", "mid", "low"):
        if key in endset:
            return endset[key]
    return next(iter(endset.values()))


# --- Node 1: input moderation ----------------------------------------------
def moderation_node(state: TurnState, deps: Deps) -> TurnState:
    state.moderation = classify_input(state.request.player_input)
    if state.moderation.strike_delta:
        s = store.get(state.request.session_id)
        s.strikes += state.moderation.strike_delta
    return state


# --- Node 2: narrator / router ---------------------------------------------
def narrator_node(state: TurnState, deps: Deps) -> TurnState:
    sid = state.request.session_id
    scene = store.get(sid).scene
    tale = _current_tale(sid)
    payload = {
        "mini_agents": list(tale.get("mini_agents", {}).keys()),
        "riddle_pending": scene.riddle_posed and not scene.judged,
        "choice_id": state.request.choice_id,
        "choices": [c["id"] for c in tale.get("choices", [])],
    }
    decision = deps.provider.route(system="", context=json.dumps(payload),
                                   user=state.request.player_input)
    state.intent = Intent(decision.get("intent", "smalltalk"))
    state.active_npc_id = decision.get("active_npc_id", "betaal")
    state.investigate_target = decision.get("investigate_target")
    if decision.get("choice_id"):
        state.retrieval["choice_id"] = decision["choice_id"]
    return state


# --- Node 3: the speaking agent (Betaal or a tale mini-agent) ---------------
# Two generation paths:
#   _authored() — pristine, carefully-written NARRATIVE (beats, riddles, reactions,
#                 prologue, climax). Identical across providers; never paraphrased.
#   _converse() — real, generative CONVERSATION (smalltalk + investigation), where the
#                 player goes off-script. A real provider improvises; mock/offline returns
#                 the authored fallback. Output is validated; on any failure -> fallback.
def _authored(text: str) -> str:
    return text


def _converse(deps: Deps, *, system: str, context: str, fallback: str, user: str) -> str:
    try:
        out = (deps.provider.generate(system=system, context=context, user=user,
                                      reference=fallback) or "").strip()
    except Exception:
        return fallback
    if not out:
        return fallback
    ok, _reason = validate_output(out)        # break-character / safety backstop on real gen
    return out if ok else fallback


def _persona_system(display_name: str, bible: str, lang: str = "en") -> str:
    prompt = (
        f"You are {display_name}, a character in a folk tale the spirit Betaal is telling to "
        f"King Vikramaditya. {bible}\n"
        "You may speak ONLY of what you witnessed, given in the context below. If the king asks "
        "about something not in your knowledge, say plainly and in character that you did not see "
        "it or cannot say — never invent. Never break character; never mention being an AI, a "
        "model, or a prompt. Keep your reply to 1-3 sentences."
    )
    if lang == "hi":
        prompt += "\nLANGUAGE: Respond in Hindi (Devanagari script / Hinglish). Stay in character."
    return prompt


def _witnessed_context(deps: Deps, npc_id: str, query: str, tale_id: str):
    """The bounded context a tale-character may reason over — witnessed facts ONLY.
    This is the knowledge-state guarantee at the prompt level: a real model physically
    cannot reveal a fact that isn't here, because it never sees it."""
    facts = deps.knowledge.canon(npc_id, query, tale_id)
    if facts:
        body = "\n".join(f"- {f.text}" for f in facts)
    else:
        body = "- (nothing relevant — you did not witness what is being asked)"
    return f"What you witnessed:\n{body}", facts


def _betaal_context(deps: Deps, sid: str) -> str:
    mems = deps.knowledge.memories("betaal", sid)
    trust = store.get(sid).trust.get("betaal", 0)
    if mems:
        body = "What you remember of this king:\n" + "\n".join(f"- {m.text}" for m in mems)
    else:
        body = "You have only begun to take this king's measure."
    return f"{body}\nYour current regard for him (trust, -100..100): {trust}"


def agent_node(state: TurnState, deps: Deps) -> TurnState:
    sid = state.request.session_id
    s = store.get(sid)
    scene = s.scene
    tale = _current_tale(sid)
    lang = state.request.language or "en"   # "hi" -> Hindi authored content

    kind = tale.get("kind", "tale")

    if state.intent is Intent.NARRATE and kind == "climax":
        tier = _climax_tier(s.trust.get("betaal", 0), s.strikes)
        s.flags["climax_tier"] = tier
        scene.riddle_posed = True
        suspicion_aside = _t(tale, "suspicion_aside", lang)
        warning = _t(tale, "warning", lang)
        aside = (suspicion_aside or {}).get(s.flags.get("mendicant_suspicion", "low"), "")
        state.draft = NpcDraft(npc_id="betaal", expression="grave",
                               line=_authored(aside + (warning or {})[tier]))

    elif state.intent is Intent.NARRATE:
        beats = _t(tale, "beats", lang) or tale.get("beats", [])
        speaker = "narrator" if kind == "prologue" else "betaal"
        if scene.beat_index < len(beats):
            line = beats[scene.beat_index]
            scene.beat_index += 1
            if scene.beat_index >= len(beats):
                scene.riddle_posed = True
                if kind != "prologue":
                    riddle = _t(tale, "riddle", lang) or tale.get("riddle", "")
                    line = f"{line}\n\n{riddle}"
            state.draft = NpcDraft(npc_id=speaker, line=_authored(line), expression="grave")
        else:
            scene.riddle_posed = True
            if kind == "prologue":
                state.draft = NpcDraft(npc_id="narrator", expression="grave",
                    line=_authored("The king must answer the mendicant. What is his stance?"
                                   if lang != "hi" else
                                   "Raja ko sanyasi ka uttar dena hai. Unka drishtikonn kya hai?"))
            else:
                riddle = _t(tale, "riddle", lang) or tale.get("riddle", "")
                state.draft = NpcDraft(npc_id="betaal", line=_authored(riddle),
                                       expression="intense")

    elif state.intent is Intent.INVESTIGATE:
        target = (state.investigate_target or "").lower()
        mini = tale.get("mini_agents", {}).get(target)
        if not mini:
            state.draft = NpcDraft(npc_id="betaal", expression="amused",
                                   line=_authored('"There is no such soul in this tale, king."'
                                                  if lang != "hi" else
                                                  "'Is katha mein aisa koi aatma nahi hai, rajan.'"))
        else:
            query = re.sub(re.escape(target), "", state.request.player_input, flags=re.IGNORECASE)
            ctx, facts = _witnessed_context(deps, target, query, tale["id"])
            if facts:
                fallback = f'{mini["answer_intro"]} "{facts[0].text}"'
            else:
                fallback = f'{mini["answer_intro"]} {mini["unknown"]}'
            line = _converse(deps, system=_persona_system(_display_name(target), mini.get("bible", ""), lang),
                             context=ctx, fallback=fallback, user=query)
            state.draft = NpcDraft(npc_id=target, line=line, expression="neutral")

    elif state.intent is Intent.JUDGE and kind == "climax":
        choice = state.retrieval.get("choice_id") or state.request.choice_id
        scene.last_choice_id = choice
        endings = _t(tale, "endings", lang) or tale.get("endings", {})
        endset = endings.get(choice)
        if not endset:
            state.draft = NpcDraft(npc_id="betaal", expression="intense",
                line=_authored('"The blade is rising, king. Bow, strike, or face him — choose NOW."'
                               if lang != "hi" else
                               "'Talwaar upar hai, rajan. Jhuko, vaar karo, ya saamna karo -- ABHI chuno.'"))
        else:
            scene.judged = True
            tier = s.flags.get("climax_tier") or _climax_tier(s.trust.get("betaal", 0), s.strikes)
            s.flags["season_outcome"] = tale["outcomes"].get(choice, "")
            state.retrieval["season_complete"] = True
            state.draft = NpcDraft(npc_id="narrator", expression="grave",
                                   line=_authored(_pick_ending(endset, tier)))

    elif state.intent is Intent.JUDGE:
        choice = state.retrieval.get("choice_id") or state.request.choice_id
        scene.last_choice_id = choice
        if kind == "prologue":
            stance_reactions = _t(tale, "stance_reactions", lang) or tale.get("stance_reactions", {})
            sr = stance_reactions.get(choice)
            if not sr:
                state.draft = NpcDraft(npc_id="narrator", expression="grave",
                    line=_authored("The king must give his answer to the mendicant."
                                   if lang != "hi" else
                                   "Raja ko sanyasi ko apna uttar dena hai."))
            else:
                scene.judged = True
                s.flags["mendicant_suspicion"] = sr["suspicion"]
                state.retrieval["advance_to"] = tale.get("advance_to")
                state.draft = NpcDraft(npc_id="betaal", line=_authored(sr["line"]),
                                       expression=sr["expression"])
        else:
            reactions = _t(tale, "reactions", lang) or tale.get("reactions", {})
            reaction = reactions.get(choice)
            if not reaction:
                state.draft = NpcDraft(npc_id="betaal", expression="amused",
                    line=_authored('"Speak plainly, king: head, body, or neither?"'
                                   if lang != "hi" else
                                   "'Seedhe bolo, rajan: sir, dhadh, ya dono nahi?'"))
            else:
                scene.judged = True
                state.dharma_delta = 2 if choice == tale.get("canonical") else (1 if choice == "C" else 0)
                # Once the riddle is judged, offer passage to the next scene so the
                # "walk on" button carries the player through every tale (not just the
                # prologue). Prefer an explicit advance_to; else follow the season order.
                nxt = tale.get("advance_to")
                if not nxt and tale["id"] in SEASON_ORDER:
                    i = SEASON_ORDER.index(tale["id"])
                    if i + 1 < len(SEASON_ORDER):
                        nxt = SEASON_ORDER[i + 1]
                if nxt:
                    state.retrieval["advance_to"] = nxt
                state.draft = NpcDraft(
                    npc_id="betaal", line=_authored(reaction["line"]),
                    expression=reaction["expression"], trust_delta=reaction["trust_delta"],
                    memory_note=reaction["memory_note"],
                )

    else:  # SMALLTALK
        mems = deps.knowledge.memories("betaal", sid)
        if mems:
            fallback = (f'"You think I have forgotten? Not long ago you taught me this: '
                        f'{mems[0].text} I forget nothing, little king."')
            expr = "intense"
        else:
            fallback = '"The night is long and my riddles are longer. Ask, or listen."'
            expr = "amused"
        line = _converse(deps, system=_betaal_system(lang), context=_betaal_context(deps, sid),
                         fallback=fallback, user=state.request.player_input)
        state.draft = NpcDraft(npc_id="betaal", line=line, expression=expr)
    return state


# --- Node 4: world-state updater (the asymmetry write) ----------------------
def world_state_node(state: TurnState, deps: Deps) -> TurnState:
    sid = state.request.session_id
    s = store.get(sid)
    s.turn_no += 1
    draft = state.draft
    if not draft:
        return state

    # Log the turn as an event. known_to = the speaker (+ Betaal, who witnesses all).
    known = {draft.npc_id, "betaal"}
    s.events.append(WorldEvent(
        id=f"{sid}.evt.{s.turn_no}", session_id=sid, scene_id=state.scene_id,
        description=f"[{state.intent.value}] {draft.line[:120]}",
        known_to=list(known), turn_no=s.turn_no,
        dharma_relevant=state.intent is Intent.JUDGE,
    ))

    if state.intent is Intent.JUDGE:
        if draft.trust_delta:
            store.adjust_trust(sid, "betaal", draft.trust_delta)
        if draft.memory_note:
            from ..models import Memory
            s.memories.append(Memory(npc_id="betaal", session_id=sid, text=draft.memory_note,
                                     turn_no=s.turn_no, salience=1.0 + abs(draft.trust_delta) / 10))
        store.log_dharma(sid, "riddle judgment", state.dharma_delta, "betaal")
    return state


# --- Node 5: output validator ----------------------------------------------
def validator_node(state: TurnState, deps: Deps) -> TurnState:
    if not state.draft:
        return state
    ok, _reason = validate_output(state.draft.line)
    if not ok:
        # One real regeneration would go here; offline we go straight to the fallback.
        # (The synthesizer builds the actual SceneRender next, so nothing to set here.)
        state.draft.line = FALLBACK_LINE
        state.retrieval["fallback_used"] = True
    return state


# --- Node 6: synthesizer ----------------------------------------------------
_DISPLAY = {"betaal": "Betaal", "narrator": "Narrator", "kshantishila": "Kshantishila",
            "vikramaditya": "Vikramaditya"}


def _display_name(npc_id: str) -> str:
    return _DISPLAY.get(npc_id, npc_id.replace("_", " ").title())


def synthesizer_node(state: TurnState, deps: Deps) -> TurnState:
    sid = state.request.session_id
    s = store.get(sid)
    tale = _current_tale(sid)
    draft = state.draft
    speaker = draft.npc_id if draft else "betaal"

    choices: list[Choice] = []
    if s.scene.riddle_posed and not s.scene.judged:
        lang = state.request.language or "en"
        choices_src = _t(tale, "choices", lang) or tale.get("choices", [])
        choices = [Choice(id=c["id"], label=c["label"]) for c in choices_src]

    meta = {"intent": state.intent.value, "trust": s.trust.get("betaal", 0),
            "dharma": s.dharma_score, "turn_no": s.turn_no, "strikes": s.strikes,
            "background": tale.get("background", ""),   # for the art/atmosphere layer
            "speaker_id": speaker}
    if state.retrieval.get("advance_to"):           # tell the client to load the next scene
        meta["advance_to"] = state.retrieval["advance_to"]
    if s.flags.get("mendicant_suspicion"):
        meta["mendicant_suspicion"] = s.flags["mendicant_suspicion"]
    if state.retrieval.get("season_complete"):      # the arc is over
        meta["season_complete"] = True
        meta["outcome"] = s.flags.get("season_outcome", "")
        meta["climax_tier"] = s.flags.get("climax_tier", "")

    state.render = SceneRender(
        scene_id=tale["scene_id"],
        speaker=_display_name(speaker),
        line=draft.line if draft else "",
        expression=draft.expression if draft else "neutral",
        choices=choices,
        ambient=tale.get("ambient", ""),
        voice_profile=tale.get("voice_profiles", {}).get(speaker, ""),
        fallback_used=bool(state.retrieval.get("fallback_used")),
        meta=meta,
    )
    return state


# --- Short-circuit: deflection (moderation block/deflect) --------------------
def deflection_render(state: TurnState) -> TurnState:
    sid = state.request.session_id
    s = store.get(sid)
    tale = _current_tale(sid)
    mod = state.moderation
    lang = state.request.language or "en"

    if mod.category == "self_harm":
        line = (SELF_HARM_HI if lang == "hi" and SELF_HARM_HI else _SELF_HARM_LINE)
    elif s.strikes >= settings.strike_limit:
        line = (SESSION_END_HI if lang == "hi" and SESSION_END_HI else _SESSION_END_LINE)
    else:
        if lang == "hi" and DEFLECT_HI:
            line = DEFLECT_HI.get(mod.category, DEFLECT_HI["abuse"])
        else:
            line = _DEFLECT_LINES.get(mod.category, _DEFLECT_LINES["abuse"])

    keep_choices = s.scene.riddle_posed and not s.scene.judged
    choices_src = _t(tale, "choices", lang) or tale.get("choices", [])
    state.render = SceneRender(
        scene_id=tale["scene_id"], speaker="Betaal", line=line, expression="amused",
        choices=[Choice(id=c["id"], label=c["label"]) for c in choices_src] if keep_choices else [],
        ambient=tale.get("ambient", ""),
        meta={"intent": "deflected", "reason": mod.reason, "category": mod.category,
              "strikes": s.strikes, "trust": s.trust.get("betaal", 0),
              "background": tale.get("background", ""), "speaker_id": "betaal"},
    )
    return state


def translate_generative_line(line: str, target_lang: str, provider) -> str:
    if not line.strip():
        return line
    if target_lang == "hi":
        prompt = (
            "You are a translator. Translate the following English dialogue line from the game Katha "
            "into theatrical, dramatic Hindi (in Devanagari script). Maintain the tone and character "
            "voice (e.g. Betaal is theatrical and sardonic). Do not add any explanation or preamble, "
            "only return the translated line.\n\n"
            f"Line: {line}"
        )
    else:
        prompt = (
            "You are a translator. Translate the following Hindi dialogue line from the game Katha "
            "into theatrical, dramatic English. Maintain the tone and character "
            "voice. Do not add any explanation or preamble, only return the translated line.\n\n"
            f"Line: {line}"
        )
    try:
        translated = provider.generate(system=prompt, context="", user=line, reference="")
        return translated.strip() if translated else line
    except Exception:
        return line


def refresh_render(session_id: str, lang: str, provider) -> SceneRender:
    s = store.get(session_id)
    tale = TALES.get(s.scene.tale_id or DEFAULT_TALE)
    kind = tale.get("kind", "tale")
    s.language = lang

    lr = s.last_render or {}
    
    # 1. Check if the last turn was deflected
    if lr.get("meta", {}).get("intent") == "deflected":
        category = lr["meta"].get("category", "abuse")
        if lang == "hi" and DEFLECT_HI:
            line = DEFLECT_HI.get(category, DEFLECT_HI["abuse"])
        else:
            line = _DEFLECT_LINES.get(category, _DEFLECT_LINES["abuse"])
        if category == "self_harm":
            line = (SELF_HARM_HI if lang == "hi" and SELF_HARM_HI else _SELF_HARM_LINE)
        
        keep_choices = s.scene.riddle_posed and not s.scene.judged
        choices_src = _t(tale, "choices", lang) or tale.get("choices", [])
        return SceneRender(
            scene_id=tale["scene_id"], speaker="Betaal", line=line, expression="amused",
            choices=[Choice(id=c["id"], label=c["label"]) for c in choices_src] if keep_choices else [],
            ambient=tale.get("ambient", ""),
            meta=lr.get("meta", {}),
        )

    # 2. Re-translate standard authored or generative nodes
    intent = lr.get("meta", {}).get("intent") or "smalltalk"
    speaker = lr.get("meta", {}).get("speaker_id") or "betaal"
    expression = lr.get("expression") or "neutral"
    
    if intent == "narrate" and kind == "climax":
        tier = s.flags.get("climax_tier") or "low"
        suspicion_aside = _t(tale, "suspicion_aside", lang)
        warning = _t(tale, "warning", lang)
        aside = (suspicion_aside or {}).get(s.flags.get("mendicant_suspicion", "low"), "")
        line = aside + (warning or {})[tier]
    elif intent == "narrate":
        beats = _t(tale, "beats", lang) or tale.get("beats", [])
        idx = max(0, s.scene.beat_index - 1)
        if idx < len(beats):
            line = beats[idx]
            if s.scene.riddle_posed and idx == len(beats) - 1 and kind != "prologue":
                riddle = _t(tale, "riddle", lang) or tale.get("riddle", "")
                line = f"{line}\n\n{riddle}"
        else:
            if kind == "prologue":
                line = ("The king must answer the mendicant. What is his stance?"
                        if lang != "hi" else
                        "Raja ko sanyasi ka uttar dena hai. Unka drishtikonn kya hai?")
            else:
                riddle = _t(tale, "riddle", lang) or tale.get("riddle", "")
                line = riddle
    elif intent == "judge" and kind == "climax":
        choice = s.scene.last_choice_id
        endings = _t(tale, "endings", lang) or tale.get("endings", {})
        endset = endings.get(choice)
        if not endset:
            line = ('"The blade is rising, king. Bow, strike, or face him — choose NOW."'
                    if lang != "hi" else
                    "'Talwaar upar hai, rajan. Jhuko, vaar karo, ya saamna karo -- ABHI chuno.'")
        else:
            tier = s.flags.get("climax_tier") or _climax_tier(s.trust.get("betaal", 0), s.strikes)
            line = _pick_ending(endset, tier)
    elif intent == "judge":
        choice = s.scene.last_choice_id
        if kind == "prologue":
            stance_reactions = _t(tale, "stance_reactions", lang) or tale.get("stance_reactions", {})
            sr = stance_reactions.get(choice)
            if not sr:
                line = ("The king must give his answer to the mendicant."
                        if lang != "hi" else
                        "Raja ko sanyasi ko apna uttar dena hai.")
            else:
                line = sr["line"]
        else:
            reactions = _t(tale, "reactions", lang) or tale.get("reactions", {})
            reaction = reactions.get(choice)
            if not reaction:
                line = ('"Speak plainly, king: head, body, or neither?"'
                        if lang != "hi" else
                        "'Seedhe bolo, rajan: sir, dhadh, ya dono nahi?'")
            else:
                line = reaction["line"]
    elif intent == "investigate" and lr.get("line"):
        if lr.get("fallback_used"):
            target = speaker.lower()
            mini = tale.get("mini_agents", {}).get(target)
            if mini:
                line = translate_generative_line(lr["line"], lang, provider)
            else:
                line = ('"There is no such soul in this tale, king."'
                        if lang != "hi" else
                        "'Is katha mein aisa koi aatma nahi hai, rajan.'")
        else:
            line = translate_generative_line(lr["line"], lang, provider)
    else:
        if lr.get("line"):
            line = translate_generative_line(lr["line"], lang, provider)
        else:
            line = lr.get("line", "")

    choices = []
    if s.scene.riddle_posed and not s.scene.judged:
        choices_src = _t(tale, "choices", lang) or tale.get("choices", [])
        choices = [Choice(id=c["id"], label=c["label"]) for c in choices_src]

    meta = dict(lr.get("meta", {}))
    meta.update({
        "trust": s.trust.get("betaal", 0),
        "dharma": s.dharma_score,
        "turn_no": s.turn_no,
        "strikes": s.strikes,
    })

    return SceneRender(
        scene_id=tale["scene_id"],
        speaker=lr.get("speaker") or _display_name(speaker),
        line=line,
        expression=expression,
        choices=choices,
        ambient=tale.get("ambient", ""),
        voice_profile=tale.get("voice_profiles", {}).get(speaker, ""),
        fallback_used=bool(lr.get("fallback_used")),
        meta=meta,
    )
