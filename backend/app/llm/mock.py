"""Offline, deterministic provider (default).

Story logic lives in the content + nodes, not here. The mock simply:
  * route():    applies the shared rule-based router.
  * generate(): returns the authored `reference` line verbatim — so the offline game is
                identical and fully testable. Real providers (ollama/gemini) instead
                generate from system+context+user.
"""
from __future__ import annotations

from .routing import route_rules


class MockProvider:
    name = "mock"

    def route(self, *, system: str, context: str, user: str) -> dict:
        return route_rules(context, user)

    def generate(self, *, system: str, context: str, user: str,
                 reference: str = "", temperature: float = 0.7) -> str:
        if reference:
            return reference
        return ("Betaal's eyes glitter in the dark. \"You speak, little king, but the night is "
                "long and my riddles are longer. Ask, or listen.\"")
