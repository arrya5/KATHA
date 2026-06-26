"""Provider-swappable LLM layer (docs/01 sec 0, principle 3).

The rest of the engine depends only on the LLMProvider interface, never on a vendor.
Default is the offline MockProvider so everything runs with no API keys.
"""
from __future__ import annotations

from ..config import settings
from .base import LLMProvider
from .mock import MockProvider


def get_provider() -> LLMProvider:
    if settings.llm_provider == "ollama":
        from .ollama import OllamaProvider
        return OllamaProvider()
    if settings.llm_provider == "gemini":
        from .gemini import GeminiProvider
        from .fallback import FallbackProvider
        return FallbackProvider(primary=GeminiProvider(), fallback=MockProvider())
    return MockProvider()
