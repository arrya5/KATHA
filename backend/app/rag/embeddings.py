"""Embeddings — pluggable, free-local-first (docs/02 sec 4).

Default is `lexical` (no embeddings — the in-memory store uses token overlap, zero deps,
fully offline). Set KATHA_EMBEDDINGS=ollama for REAL semantic retrieval using a local
Ollama embedding model (e.g. `ollama pull nomic-embed-text`) — no API key, stdlib only.

The vector store calls `embed()` at add() and query() time; if the embedder is not
`enabled` (or unhealthy), the store transparently falls back to lexical matching.
"""
from __future__ import annotations

import json
import urllib.error
import urllib.request

from ..config import settings


class NullEmbedder:
    """No embeddings — the store uses lexical overlap. Offline, zero-dependency default."""
    enabled = False

    def embed(self, texts: list[str]) -> list[list[float] | None]:
        return [None for _ in texts]


class OllamaEmbedder:
    """Real semantic embeddings from a local Ollama model (free, no key)."""
    enabled = True

    def __init__(self) -> None:
        base = settings.ollama_url.rstrip("/")
        self.url_new = base + "/api/embed"          # newer Ollama: {input} -> {embeddings:[[..]]}
        self.url_old = base + "/api/embeddings"     # older Ollama: {prompt} -> {embedding:[..]}
        self.model = settings.ollama_embed_model

    def _one(self, text: str) -> list[float] | None:
        # Try the new endpoint, then the old one.
        for url, key, payload in (
            (self.url_new, "embeddings", {"model": self.model, "input": text}),
            (self.url_old, "embedding", {"model": self.model, "prompt": text}),
        ):
            req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"),
                                         headers={"Content-Type": "application/json"})
            try:
                with urllib.request.urlopen(req, timeout=60) as resp:
                    data = json.loads(resp.read())
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError):
                continue
            vec = data.get(key)
            if key == "embeddings" and vec:        # list-of-lists
                vec = vec[0]
            if vec:
                return vec
        return None

    def embed(self, texts: list[str]) -> list[list[float] | None]:
        return [self._one(t) for t in texts]

    def healthy(self) -> bool:
        return self.embed(["healthcheck"])[0] is not None


def get_embedder():
    if settings.embeddings == "ollama":
        e = OllamaEmbedder()
        if e.healthy():
            return e
        print(f"[katha] Ollama embeddings unavailable (model '{e.model}' not pulled?) — "
              f"falling back to lexical retrieval.")
    return NullEmbedder()
