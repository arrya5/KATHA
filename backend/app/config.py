"""Configuration for the Katha backend.

Everything is read from environment variables so no secret ever lives in the repo.
With no env set, the app runs fully offline using the MockProvider and the in-memory
stores — see app/llm/mock.py and app/rag/vector_store.py.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path


def _load_dotenv() -> None:
    """Load backend/.env into os.environ (stdlib only, no python-dotenv required).

    Walks up from this file's directory to find the nearest `.env` inside a `backend/`
    folder. Variables already set in the real environment are NOT overwritten, so
    shell overrides still work: `SARVAM_API_KEY=xyz python -m app.webserver`.
    """
    # Look for .env next to this file's parent 'backend/' directory.
    candidate = Path(__file__).resolve().parent.parent / ".env"  # backend/.env
    if not candidate.is_file():
        return
    with candidate.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            key = key.strip()
            val = val.strip()
            # Strip optional surrounding quotes (single or double)
            if len(val) >= 2 and val[0] in ('"', "'") and val[-1] == val[0]:
                val = val[1:-1]
            if key and key not in os.environ:  # never overwrite real env vars
                os.environ[key] = val


_load_dotenv()  # Must run before Settings fields are evaluated below.


def _get(name: str, default: str = "") -> str:
    return os.environ.get(name, default)


@dataclass
class Settings:
    # --- LLM provider --------------------------------------------------------
    # "mock"  : offline, deterministic (default; returns authored lines)
    # "ollama": real local generation, NO API KEY (e.g. hermes3) — for dev/testing
    # "gemini": cloud (requires GEMINI_API_KEY)
    llm_provider: str = field(default_factory=lambda: _get("KATHA_LLM_PROVIDER", "mock"))
    gemini_api_key: str = field(default_factory=lambda: _get("GEMINI_API_KEY", ""))
    gemini_model: str = field(default_factory=lambda: _get("GEMINI_MODEL", "gemini-1.5-pro"))
    # Ollama (local, free): run `ollama serve`; default model hermes3.
    ollama_url: str = field(default_factory=lambda: _get("OLLAMA_URL", "http://localhost:11434"))
    ollama_model: str = field(default_factory=lambda: _get("KATHA_OLLAMA_MODEL", "hermes3"))

    # --- Voice (Sarvam TTS + STT) --------------------------------------------
    # With no key, the web client falls back to the browser's built-in speech (free).
    # Setting SARVAM_API_KEY is sufficient — KATHA_VOICE=1 is optional but kept for
    # explicit override (e.g. force-enable in CI with a test key).
    sarvam_api_key: str = field(default_factory=lambda: _get("SARVAM_API_KEY", ""))
    voice_enabled: bool = field(default_factory=lambda: _get("KATHA_VOICE", "0") == "1")
    sarvam_tts_url: str = field(default_factory=lambda: _get("SARVAM_TTS_URL", "https://api.sarvam.ai/text-to-speech"))
    sarvam_stt_url: str = field(default_factory=lambda: _get("SARVAM_STT_URL", "https://api.sarvam.ai/speech-to-text"))
    sarvam_model: str = field(default_factory=lambda: _get("SARVAM_MODEL", "bulbul:v3"))
    sarvam_sample_rate: int = 22050
    # Default language code sent to Sarvam (BCP-47). Profiles may override per-character.
    sarvam_default_language: str = field(default_factory=lambda: _get("SARVAM_LANGUAGE", "hi-IN"))

    @property
    def tts_enabled(self) -> bool:
        """True when a Sarvam key is present (key presence is sufficient; KATHA_VOICE is optional)."""
        return bool(self.sarvam_api_key)

    # --- Vector store --------------------------------------------------------
    # "memory" (in-process, default) | "chroma" | "pinecone"
    vector_store: str = field(default_factory=lambda: _get("KATHA_VECTOR_STORE", "memory"))
    # Retrieval mode for the in-memory store:
    # "lexical" (token overlap, offline, default) | "ollama" (real semantic, free local)
    embeddings: str = field(default_factory=lambda: _get("KATHA_EMBEDDINGS", "lexical"))
    ollama_embed_model: str = field(default_factory=lambda: _get("KATHA_OLLAMA_EMBED_MODEL", "nomic-embed-text"))

    # --- Orchestrator --------------------------------------------------------
    # "simple" (stdlib runner, default, zero-install) | "langgraph" (production)
    orchestrator: str = field(default_factory=lambda: _get("KATHA_ORCHESTRATOR", "simple"))

    # --- Database ------------------------------------------------------------
    # default: in-memory session store. Set DATABASE_URL for SQLite/Postgres later.
    database_url: str = field(default_factory=lambda: _get("DATABASE_URL", ""))

    # --- Gameplay tuning -----------------------------------------------------
    canon_top_k: int = 5
    memory_top_k: int = 5
    strike_limit: int = 3

    @property
    def offline(self) -> bool:
        return self.llm_provider == "mock"


settings = Settings()
