"""Vector store abstraction.

Two retrieval modes behind one .add()/.query() API:
  * lexical (default) — token-overlap (Jaccard). Offline, zero-dependency.
  * semantic — real embeddings (cosine similarity) when an Embedder is enabled
               (KATHA_EMBEDDINGS=ollama). See embeddings.py.

Production swap: ChromaDB (dev) / Pinecone (prod) behind this same API — both bundle
embeddings, replacing both the lexical fallback and the Ollama embedder.
"""
from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from typing import Callable, Optional

from .embeddings import get_embedder

_TOKEN = re.compile(r"[a-z0-9']+")

_STOP = {
    "the", "a", "an", "and", "or", "of", "to", "in", "on", "at", "by", "for", "with",
    "his", "her", "their", "its", "he", "she", "they", "it", "him", "them", "did", "do",
    "what", "who", "whom", "that", "this", "was", "were", "is", "are", "be", "been",
    "you", "your", "i", "me", "my", "upon", "from", "as", "so", "not",
}


def _tokens(text: str) -> set[str]:
    return {t for t in _TOKEN.findall(text.lower()) if t not in _STOP and len(t) > 1}


def _cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb) if na and nb else 0.0


@dataclass
class Record:
    id: str
    text: str
    metadata: dict
    vector: Optional[list[float]] = field(default=None)


class InMemoryVectorStore:
    def __init__(self, embedder=None) -> None:
        self._collections: dict[str, list[Record]] = {}
        self.embedder = embedder if embedder is not None else get_embedder()

    @property
    def semantic(self) -> bool:
        return getattr(self.embedder, "enabled", False)

    def add(self, collection: str, id: str, text: str, metadata: Optional[dict] = None) -> None:
        vector = self.embedder.embed([text])[0] if self.semantic else None
        self._collections.setdefault(collection, []).append(
            Record(id=id, text=text, metadata=metadata or {}, vector=vector)
        )

    def query(
        self,
        collection: str,
        text: str,
        k: int = 5,
        where: Optional[Callable[[dict], bool]] = None,
    ) -> list[Record]:
        records = self._collections.get(collection, [])
        candidates = [r for r in records if not where or where(r.metadata)]

        # Semantic path: cosine similarity over real embeddings.
        if self.semantic:
            qv = self.embedder.embed([text])[0]
            if qv is not None and any(r.vector for r in candidates):
                scored = [(_cosine(qv, r.vector), r) for r in candidates if r.vector]
                scored.sort(key=lambda s: s[0], reverse=True)
                return [r for _, r in scored[:k]]
            # else fall through to lexical (e.g. query embed failed)

        # Lexical path (default / fallback).
        q = _tokens(text)
        scored: list[tuple[float, Record]] = []
        for rec in candidates:
            if not q:
                scored.append((0.0, rec))
                continue
            overlap = q & _tokens(rec.text)
            if not overlap:
                continue
            score = len(overlap) / len(q | _tokens(rec.text))
            scored.append((score, rec))
        scored.sort(key=lambda s: s[0], reverse=True)
        return [r for _, r in scored[:k]]


_store: Optional[InMemoryVectorStore] = None


def get_vector_store() -> InMemoryVectorStore:
    global _store
    if _store is None:
        _store = InMemoryVectorStore()
    return _store
