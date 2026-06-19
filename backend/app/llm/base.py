"""The LLM interface every node programs against."""
from __future__ import annotations

from typing import Protocol


class LLMProvider(Protocol):
    def generate(self, *, system: str, context: str, user: str,
                 reference: str = "", temperature: float = 0.7) -> str:
        """Generate an in-character line.

        system    : the character's bible / persona prompt (static).
        context   : dynamic, bounded context the character may use (witnessed facts,
                    memories, trust) — assembled by the knowledge-state engine, so a real
                    model physically cannot see what the character didn't witness.
        user      : the player's input.
        reference : the authored fallback line. The offline MockProvider returns it
                    verbatim (deterministic); real providers may use it as a hint and fall
                    back to it on failure (handled by the caller).
        """
        ...

    def route(self, *, system: str, context: str, user: str) -> dict:
        """Structured narrator routing (rule-based, identical across providers)."""
        ...
