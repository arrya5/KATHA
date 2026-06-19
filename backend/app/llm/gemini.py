"""Gemini provider — production cloud option (stub until GEMINI_API_KEY + SDK present).

Enable with KATHA_LLM_PROVIDER=gemini + GEMINI_API_KEY. Routing stays rule-based (shared);
only dialogue generation uses the model. NOTE: update GEMINI_MODEL to a current model
(e.g. a Flash tier for the cheap layer / Pro for the narrator) when wiring for real.
"""
from __future__ import annotations

from ..config import settings
from .routing import route_rules


class GeminiProvider:
    name = "gemini"

    def __init__(self) -> None:
        if not settings.gemini_api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not set. Use KATHA_LLM_PROVIDER=mock (offline) or "
                "=ollama (free local), or provide a key."
            )
        try:
            import google.generativeai as genai  # type: ignore
        except ImportError as e:  # pragma: no cover
            raise RuntimeError(
                "google-generativeai not installed. `pip install -r requirements.txt`."
            ) from e
        genai.configure(api_key=settings.gemini_api_key)
        self._model = genai.GenerativeModel(settings.gemini_model)

    def route(self, *, system: str, context: str, user: str) -> dict:
        return route_rules(context, user)

    def generate(self, *, system: str, context: str, user: str,
                 reference: str = "", temperature: float = 0.7) -> str:
        prompt = (
            f"{system}\n\n# Context you are aware of (reveal nothing not here)\n{context}\n\n"
            f"# The player says:\n\"{user}\"\n\n# Respond in character, concisely:"
        )
        resp = self._model.generate_content(
            prompt, generation_config={"temperature": temperature}
        )
        return (resp.text or "").strip()
