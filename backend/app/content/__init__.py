"""Phase-1 content (Vikram aur Betaal) and content loading.

Importing this package registers each tale's canon facts into the vector store so the
knowledge-state engine can retrieve (and filter) them. See docs/11.
"""
from __future__ import annotations

from ..rag.vector_store import get_vector_store
from .tales import TALES


def load_canon() -> None:
    vs = get_vector_store()
    for tale in TALES.values():
        for fact in tale.get("canon_facts", []):   # stub tales (2-4) carry no facts yet
            vs.add(
                "canon",
                id=fact["chunk_id"],
                text=fact["text"],
                metadata={
                    "tale_id": tale["id"],
                    "speaker": fact.get("speaker", "narrator"),
                    "characters_present": fact.get("characters_present", []),
                    "themes": fact.get("themes", []),
                },
            )


load_canon()
