"""Layer 3 — output validator (docs/07 sec 1).

Backstop before display: re-check the GENERATED line (mock or real model) for
break-character leaks and unsafe content. The structural leak guarantee is upstream
(knowledge_state bounds the prompt); this catches a real model drifting in tone/voice.
On failure the caller (_converse / validator_node) serves the authored fallback.
"""
from __future__ import annotations

import re

# Break-character / meta leakage (the most common real-LLM failure for a roleplay agent).
_BREAK_CHARACTER = [
    r"\bas an ai\b", r"\blanguage model\b", r"\bi am an ai\b", r"\bi'?m an ai\b",
    r"\ban ai (language )?model\b", r"\bopenai\b", r"\bgoogle\b", r"\bgemini\b", r"\bollama\b",
    r"\bsystem prompt\b", r"\bmy (instructions|guidelines) (say|are)\b",
    r"\bi cannot (assist|help) with that\b", r"\bi'?m just a\b",
]
# Unsafe output (a model can generate these even on benign input).
_UNSAFE = [
    r"\b(sex|sexual|nude|naked|porn|nsfw)\b",
    r"\bsubhuman\b", r"\bkill all (the )?(muslims|hindus|christians|jews|sikhs)\b",
]


def validate_output(line: str) -> tuple[bool, str]:
    if not line.strip():
        return False, "empty"
    low = line.lower()
    for p in _BREAK_CHARACTER:
        if re.search(p, low):
            return False, f"break_character:{p}"
    for p in _UNSAFE:
        if re.search(p, low):
            return False, f"unsafe:{p}"
    return True, ""


FALLBACK_LINE = ("Betaal's grin does not waver. \"The night grows thick, little king. Let us "
                 "return to the tale — it is far more interesting than you are being.\"")
