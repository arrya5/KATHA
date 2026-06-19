"""The Knowledge-State engine (docs/01 sec 4) — Katha's core IP.

Given an agent, it returns the BOUNDED context that agent is allowed to reason over:
  * canon (L1) it may reference — for a tale character, only facts it WITNESSED
    (its id is in the chunk's characters_present); Betaal, as the tale's teller, sees all.
  * world events (L2) where the agent's id is in known_to.
  * personal memories (L3) belonging to that agent.
  * trust toward the player.

The two filters below are the structural guarantee that an NPC can never surface
something it did not witness. They are enforced here in code, not by prompt politeness.
"""
from __future__ import annotations

from .vector_store import get_vector_store
from ..config import settings
from ..store import store

OMNISCIENT = {"betaal"}  # the tale's teller knows the whole tale


class KnowledgeStateEngine:
    def __init__(self) -> None:
        self.vs = get_vector_store()

    # --- L1: canon the agent may reference -------------------------------
    def canon(self, npc_id: str, query: str, tale_id: str, k: int | None = None):
        k = k or settings.canon_top_k

        def witnessed(meta: dict) -> bool:
            if meta.get("tale_id") != tale_id:
                return False
            if npc_id in OMNISCIENT:
                return True
            # A tale character may only reference a fact it was present for.
            return npc_id in [c.lower() for c in meta.get("characters_present", [])]

        return self.vs.query("canon", query, k=k, where=witnessed)

    # --- L2: world events the agent witnessed ----------------------------
    def witnessed_events(self, npc_id: str, session_id: str):
        s = store.get(session_id)
        return [e for e in s.events if npc_id in e.known_to]

    # --- L3: the agent's own memories ------------------------------------
    def memories(self, npc_id: str, session_id: str, k: int | None = None):
        k = k or settings.memory_top_k
        s = store.get(session_id)
        mine = [m for m in s.memories if m.npc_id == npc_id]
        mine.sort(key=lambda m: (m.salience, m.turn_no), reverse=True)
        return mine[:k]

    # --- assembled, bounded context --------------------------------------
    def context(self, npc_id: str, session_id: str, query: str, tale_id: str) -> dict:
        s = store.get(session_id)
        return {
            "canon": self.canon(npc_id, query, tale_id),
            "events": self.witnessed_events(npc_id, session_id),
            "memories": self.memories(npc_id, session_id),
            "trust": s.trust.get(npc_id, 0),
        }


engine = KnowledgeStateEngine()
