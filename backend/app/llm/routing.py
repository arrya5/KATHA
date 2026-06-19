"""Shared, deterministic narrator routing.

Routing (which character speaks, and the player's intent) is narrator logic — we keep it
rule-based and identical across providers, so only *dialogue generation* varies by provider.
"""
from __future__ import annotations

import json
import re
from ..models import Intent

# Map a WHOLE-WORD keyword in free text to a riddle choice. Word-boundary matching is
# essential: the bare letters a/b/c must not match inside words like "Betaal" or "company".
_CHOICE_KEYWORDS = {
    "head": "A", "a": "A",
    "body": "B", "b": "B",
    "neither": "C", "none": "C", "c": "C",
}


def route_rules(context: str, user: str) -> dict:
    """`context` is a JSON scene payload; `user` is the player's input."""
    try:
        payload = json.loads(context) if context else {}
    except json.JSONDecodeError:
        payload = {}

    text = (user or "").strip().lower()

    # A tapped choice button is an unambiguous judgment / stance.
    if payload.get("choice_id"):
        return {"active_npc_id": "betaal", "intent": Intent.JUDGE.value,
                "choice_id": payload["choice_id"], "investigate_target": None}

    # Address a tale character by name -> investigate (lean-in).
    for agent in payload.get("mini_agents", []):
        if agent.lower() in text:
            return {"active_npc_id": agent, "intent": Intent.INVESTIGATE.value,
                    "investigate_target": agent}

    # Begin / continue the narration.
    if text in {"", "begin", "start", "continue", "next", "tell me a tale", "go on"}:
        return {"active_npc_id": "betaal", "intent": Intent.NARRATE.value,
                "investigate_target": None}

    # Free-text answer to a pending riddle / stance (whole-word match only).
    if payload.get("riddle_pending"):
        for kw, choice in _CHOICE_KEYWORDS.items():
            if re.search(rf"\b{kw}\b", text):
                return {"active_npc_id": "betaal", "intent": Intent.JUDGE.value,
                        "choice_id": choice, "investigate_target": None}

    return {"active_npc_id": "betaal", "intent": Intent.SMALLTALK.value,
            "investigate_target": None}
