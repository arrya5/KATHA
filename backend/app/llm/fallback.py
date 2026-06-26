"""FallbackProvider — wraps a primary provider with a secondary fallback.

If the primary's generate() raises any exception or returns an empty string,
the fallback provider's generate() is called instead. This keeps the demo
running on free-tier Gemini quota without ever showing the player a blank line.

The route() method delegates to the primary only (routing is rule-based and
never fails, so no fallback path is needed there).
"""
from __future__ import annotations

import logging

from .base import LLMProvider

logger = logging.getLogger(__name__)


class FallbackProvider:
    """Wraps *primary* with *fallback*: on any error or empty response, uses fallback."""

    name = "fallback"

    def __init__(self, primary: LLMProvider, fallback: LLMProvider) -> None:
        self._primary = primary
        self._fallback = fallback

    def route(self, *, system: str, context: str, user: str) -> dict:
        return self._primary.route(system=system, context=context, user=user)

    def generate(self, *, system: str, context: str, user: str,
                 reference: str = "", temperature: float = 0.7) -> str:
        try:
            result = self._primary.generate(
                system=system, context=context, user=user,
                reference=reference, temperature=temperature,
            )
            if result:
                return result
            logger.warning("Primary provider returned empty response; falling back.")
        except Exception as exc:
            logger.warning("Primary provider raised %s: %s; falling back.", type(exc).__name__, exc)
        return self._fallback.generate(
            system=system, context=context, user=user,
            reference=reference, temperature=temperature,
        )
