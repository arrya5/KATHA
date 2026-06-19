"""Ollama provider — real LOCAL generation, no API key (docs: build on this, swap to a
paid provider before launch).

Talks to a local Ollama server (default http://localhost:11434) over plain HTTP using
the standard library only — no extra dependencies. Enable with:

    ollama serve            # in one terminal (if not already running)
    ollama pull hermes3     # once
    KATHA_LLM_PROVIDER=ollama python -m app.webserver

Routing stays rule-based (shared). Only dialogue generation uses the model. The caller
(_converse in agents/nodes.py) falls back to the authored line if generation fails, so a
slow/absent Ollama never breaks the game.
"""
from __future__ import annotations

import json
import urllib.error
import urllib.request

from ..config import settings
from .routing import route_rules


class OllamaProvider:
    name = "ollama"

    def __init__(self) -> None:
        self.url = settings.ollama_url.rstrip("/") + "/api/generate"
        self.model = settings.ollama_model

    def route(self, *, system: str, context: str, user: str) -> dict:
        return route_rules(context, user)

    def generate(self, *, system: str, context: str, user: str,
                 reference: str = "", temperature: float = 0.7) -> str:
        prompt = (
            f"{system}\n\n"
            f"# Context you are aware of (do not reveal anything not here)\n{context}\n\n"
            f"# The king says to you:\n\"{user}\"\n\n"
            "# Respond in character, in one short vivid reply. Do not break character. "
            "Do not mention being an AI, a model, or a prompt."
        )
        payload = json.dumps({
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": temperature, "num_predict": 220},
        }).encode("utf-8")
        req = urllib.request.Request(self.url, data=payload,
                                     headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read())
            return (data.get("response") or "").strip()
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError) as e:
            # Surface to the caller, which falls back to the authored line.
            raise RuntimeError(f"ollama generate failed: {e}") from e
