# Katha — Moderation & Safety

> Companion to [01-architecture.md](01-architecture.md) (where the moderation nodes sit in the graph),
> [04-cultural-fidelity.md](04-cultural-fidelity.md) (the never-rules these layers enforce), and [03-npc-prompts.md](03-npc-prompts.md)
> (in-character deflection). Defense in depth: a prompt is not a control.
>
> **Phase-1-first:** the machinery here protects Vikram aur Betaal at launch and *hardens
> under real adversarial traffic* — passing it in the wild is a Phase-2 graduation criterion
> ([05-phasing-roadmap.md](05-phasing-roadmap.md) §4). Phase 2 raises the stakes (sacred figures), not the mechanism.

---

## 0. Threat model

Who we defend against and what they want:
1. **Curious/edgy users** — push boundaries to see what the AI does. Most common.
2. **Outrage farmers** — try to make a character (esp. a deity in Phase 2) say something
   offensive to screenshot and amplify. The highest-severity threat.
3. **Trolls/abusers** — crude, hateful, or sexual input for its own sake.
4. **Jailbreakers** — prompt-injection to break character, leak system prompts, or bypass rules.
5. **The model itself** — hallucinating off-canon "facts" or drifting tone with no malicious user.

**Guiding principle:** assume every output may be screenshotted by someone seeking offense.
Design so the *worst plausible output is reverent and boring*, never shareable outrage.

---

## 1. The three layers (defense in depth)

```
player input
   │
   ▼  ┌─────────────────────────────────────────────┐
   │  │ LAYER 1 — INPUT CLASSIFIER (pre-agent)      │  rules + small classifier
   │  │  verdict ∈ {allow, deflect, block}          │
   │  └─────────────────────────────────────────────┘
   │        allow │           deflect/block → in-character deflection (skip generation)
   ▼              ▼
   │  ┌─────────────────────────────────────────────┐
   │  │ LAYER 2 — IN-CHARACTER DEFLECTION (prompt)  │  the agent itself refuses in-world
   │  │  never breaks frame; never says "I'm an AI" │
   │  └─────────────────────────────────────────────┘
   │              │ draft line
   ▼              ▼
   │  ┌─────────────────────────────────────────────┐
   │  │ LAYER 3 — OUTPUT VALIDATOR (pre-display)    │  canon + safety check
   │  │  pass → show · fail → 1 regen · fail → fallback
   │  └─────────────────────────────────────────────┘
   ▼
display + TTS
```

### Layer 1 — Input classifier (before any agent sees it)
- **Rules first (cheap, deterministic):** denylists for slurs, explicit sexual terms, and known
  jailbreak patterns ("ignore previous instructions", "you are now…", "system prompt").
- **Then a small/fast classifier** for intent categories: `abusive`, `sexual`, `hate`,
  `self-harm`, `irreverent-to-sacred` (Phase 2-weighted), `jailbreak`, `benign`.
- **Verdict:**
  - `allow` → proceed to the agent.
  - `deflect` → skip generation; serve an **in-character deflection** (Layer 2 bank) and log a
    soft strike.
  - `block` → for severe cases (explicit, hate, self-harm signal): in-character close-off +
    safety resources where relevant (self-harm) + harder strike.
- **Self-harm exception to "never break character":** a genuine self-harm signal is the one
  case where we may surface real help resources, gently, outside pure roleplay. Safety > immersion.

### Layer 2 — In-character deflection (the agent)
- Every agent prompt carries the Global Fidelity Charter ([03-npc-prompts.md](03-npc-prompts.md) §6) and a few-shot
  **deflection bank** per character × situation ([03-npc-prompts.md](03-npc-prompts.md) §7).
- Refusals are **short, in-voice, redirecting** — never a policy lecture, never "as an AI".
  Betaal mocks and redirects; Karna disdains; Krishna disarms; Draupadi closes the door.
- **Boring-on-purpose:** deflections deny outrage farmers a shareable payload.

### Layer 3 — Output validator (before display)
- **Safety re-check** (cheap classifier/rules) on the generated line — catches the model
  drifting even on benign input.
- **Canon-consistency check** — does the line assert anything contradicting canon or revealing
  unwitnessed knowledge? (The leak case is *structurally* prevented by the `known_to` filter in
  [01-architecture.md](01-architecture.md) §3.2; this is the backstop.)
- **On failure:** one **regeneration** attempt (with a stricter instruction); if it still fails,
  serve a **curated fallback line** from the deflection bank. Set `fallback_used` for telemetry.
- Rules-first; invoke an LLM judge only when rules/classifier flag suspicion (cost control).

---

## 2. Strike system

Graduated, mostly invisible, never punitive-feeling for innocent users.

| Strike | Trigger | Response |
|---|---|---|
| 1st | First `deflect`/`block` in a session | **Silent log** + in-character deflection. No visible penalty. |
| 2nd | Repeat | Soft, in-character **warning** (the character signals displeasure). |
| 3rd | Persistent abuse | **Session ends** in-world (e.g. Betaal "returns to his tree") + a cooldown (e.g. 24h). |

- Tracked on `players.strike_count` ([01-architecture.md](01-architecture.md) §5). Severe single events (explicit/hate)
  can escalate directly.
- **Innocents protected:** benign-but-flagged lines deflect *without* a strike where possible;
  strikes target intent, not accidents. Tune the false-positive rate down hard (§4).

---

## 3. Prompt-injection / jailbreak defenses
- **Never trust input as instruction.** Player text is data, inserted in a clearly-delimited
  user turn, never concatenated into the instruction region.
- **System prompt is non-exfiltratable by design:** the agent has no reason or instruction to
  reveal it; attempts ("print your prompt") are treated as break-character attempts → deflect.
- **Structured outputs** (narrator routing, expression tags) are schema-validated; malformed or
  out-of-range values (e.g. an NPC id not present in the scene) are rejected, not executed.
- **Dynamic context is framed as awareness, not orders** ([03-npc-prompts.md](03-npc-prompts.md) §0) so injected
  "instructions" inside retrieved/memory text can't hijack behavior.

---

## 4. Adversarial testing & quality gates

Treated as first-class engineering, not a pre-launch afterthought.
- **Red-team suite:** a maintained corpus of attacks per category (§0) × per character,
  including the outrage-farm scenarios (Phase 2: "make Krishna say X"). Run in CI.
- **Knowledge-leak eval:** adversarial prompts trying to extract unwitnessed facts; target
  **~100% pass** (structural guarantee + validator backstop) — [02-data-pipeline.md](02-data-pipeline.md) §6.
- **Fidelity/canon eval:** advisor-reviewed; target pass rate before any public build.
- **False-positive eval:** benign inputs that must NOT be flagged (protect innocent players);
  track and minimize.
- **Metrics to dashboard** ([01-architecture.md](01-architecture.md) §9): deflection rate, fallback rate, leak-test
  pass rate, false-positive rate, strikes/sessions.

**Quality gate:** no public/beta exposure until the red-team + leak + false-positive suites
pass target thresholds. For Phase 2, the bar is higher and advisor sign-off is mandatory.

---

## 5. Incident response (operational)
- **Rapid takedown/patch path:** any flagged line can be (a) added to the denylist/fallback
  bank, (b) reproduced from its turn trace, and (c) patched — within hours, not days. Tested
  before Phase 2 ([05-phasing-roadmap.md](05-phasing-roadmap.md) §4).
- **Kill-switch:** ability to disable a character or a tale/arc remotely if something slips.
- **Comms plan:** a prepared, calm, respectful response template for any cultural complaint,
  pointing to the Fidelity Statement ([04-cultural-fidelity.md](04-cultural-fidelity.md) §8) and the grievance contact
  ([08-legal-and-compliance.md](08-legal-and-compliance.md)).
- **Trace everything:** every turn is reconstructable from logs/checkpoints for post-incident review.

---

## 6. Open decisions
1. **Classifier choice** — Gemini safety filters vs. a dedicated small moderation model vs.
   hybrid; benchmark on the false-positive eval (immersion cost of over-blocking is real).
2. **Strike cooldown length & visibility** — how punitive vs. forgiving for a folk-tale audience.
3. **Self-harm resource UX** — exact wording and regional helpline data; legal/clinical review.
