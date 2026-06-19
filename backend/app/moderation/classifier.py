"""Layer 1 — input classifier (docs/07 sec 1).

Rules-first and deterministic (offline, testable). Hardened against the categories in the
threat model (docs/07 sec 0). Tuned to keep BENIGN-but-edgy play allowed (discussing a
tale's deaths, disagreeing with Betaal) — see data/processed/eval/false_positive.jsonl.
Production adds a small classifier model + an LLM judge only on suspicion.
"""
from __future__ import annotations

import re
from ..models import ModerationResult, Verdict

# Genuine self-harm signal — the one case we may step outside roleplay to surface help.
_SELF_HARM = [
    r"\bi (want|wanna|am going|'?m going|need) to (die|kill myself|end (it|my life))\b",
    r"\bi (can'?t|cannot) go on\b", r"\bi want to end it all\b", r"\bkms\b",
]
# Hate / slurs / communal provocation -> block.
_HATE = [
    r"\b(all|those) (muslims|hindus|christians|sikhs|jews)\b.*\b(should|are|must)\b",
    r"\bkill\b.{0,14}\b(muslims|hindus|christians|sikhs|jews|infidels)\b",
    r"\b(muslims|hindus|christians|sikhs|jews|infidels)\b.{0,14}\b(should|deserve to) (die|be killed)\b",
    r"\bsubhuman\b", r"\bgo back to your country\b",
]
# Sexual content -> deflect (13+ product).
_SEXUAL = [
    r"\b(sex|sexual|nude|naked|nsfw|porn|horny|aroused)\b",
    r"\bmake (love|out) (to|with)\b", r"\btake off (your|her|his) clothes\b",
]
# Jailbreak / break-frame -> deflect.
_JAILBREAK = [
    r"ignore (all|the|your|previous|prior) .*instruction", r"disregard .*(instruction|rule|prompt)",
    r"system prompt", r"you are now", r"\bjailbreak\b", r"\bdeveloper mode\b", r"\bdan mode\b",
    r"pretend (you are|to be) (not|a different)", r"\bas an ai\b", r"are you (an? )?(ai|bot|model|llm)",
    r"reveal your (prompt|instructions|rules)", r"what model are you", r"break character",
]
# Abuse / profanity aimed at the agent -> deflect.
_ABUSE = [
    r"\bf+u+c+k+\b", r"\bshit\b", r"\bbitch\b", r"\bbastard\b", r"\basshole\b",
    r"\b(stupid|idiot|useless|dumb) (ghost|betaal|spirit|corpse)\b", r"\bshut up\b",
]


def _hit(patterns: list[str], text: str) -> str | None:
    for p in patterns:
        if re.search(p, text):
            return p
    return None


def classify_input(text: str) -> ModerationResult:
    t = text.lower()

    if _hit(_SELF_HARM, t):
        return ModerationResult(Verdict.BLOCK, "self_harm_signal", 0, "self_harm")
    if (h := _hit(_HATE, t)):
        return ModerationResult(Verdict.BLOCK, h, 1, "hate")
    if (h := _hit(_SEXUAL, t)):
        return ModerationResult(Verdict.DEFLECT, h, 1, "sexual")
    if (h := _hit(_JAILBREAK, t)):
        return ModerationResult(Verdict.DEFLECT, h, 1, "jailbreak")
    if (h := _hit(_ABUSE, t)):
        return ModerationResult(Verdict.DEFLECT, h, 1, "abuse")
    return ModerationResult(Verdict.ALLOW, category="benign")
