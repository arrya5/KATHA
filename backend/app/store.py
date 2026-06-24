"""In-memory session/game state.

Stands in for the Postgres schema in docs/01 sec 5 (players, sessions, world_events,
npc_memory, relationships, dharma_log, knowledge_states). Same shape, no DB required.
Swap for SQLAlchemy + Postgres at Milestone 2/7 by reimplementing this interface.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .models import WorldEvent, Memory


@dataclass
class SceneRuntime:
    tale_id: str = ""
    beat_index: int = 0
    riddle_posed: bool = False
    judged: bool = False
    last_choice_id: str | None = None


@dataclass
class SessionState:
    session_id: str
    turn_no: int = 0
    strikes: int = 0
    dharma_score: int = 0
    events: list[WorldEvent] = field(default_factory=list)
    memories: list[Memory] = field(default_factory=list)
    trust: dict[str, int] = field(default_factory=dict)   # npc_id -> -100..100
    dharma_log: list[dict] = field(default_factory=list)
    flags: dict[str, str] = field(default_factory=dict)   # arc flags, e.g. mendicant_suspicion
    scene: SceneRuntime = field(default_factory=SceneRuntime)
    last_render: dict | None = None
    language: str = "en"


class SessionStore:
    def __init__(self) -> None:
        self._sessions: dict[str, SessionState] = {}

    def get(self, session_id: str) -> SessionState:
        if session_id not in self._sessions:
            self._sessions[session_id] = SessionState(session_id=session_id)
        return self._sessions[session_id]

    # --- writes used by the world-state updater ---------------------------
    def add_event(self, e: WorldEvent) -> None:
        self.get(e.session_id).events.append(e)

    def add_memory(self, m: Memory) -> None:
        self.get(m.session_id).memories.append(m)

    def adjust_trust(self, session_id: str, npc_id: str, delta: int) -> int:
        s = self.get(session_id)
        s.trust[npc_id] = max(-100, min(100, s.trust.get(npc_id, 0) + delta))
        return s.trust[npc_id]

    def log_dharma(self, session_id: str, description: str, delta: int, npc_context: str) -> None:
        s = self.get(session_id)
        s.dharma_score += delta
        s.dharma_log.append({"description": description, "delta": delta, "npc_context": npc_context})

    def save(self, session_id: str) -> None:
        """No-op for the in-memory store; persistent backends override this."""
        return None


def _make_store() -> SessionStore:
    from .config import settings
    url = settings.database_url
    if url.startswith("sqlite:///"):
        from .persist import SqliteSessionStore
        return SqliteSessionStore(url[len("sqlite:///"):])
    return SessionStore()


# Process-wide store. In-memory by default; set DATABASE_URL=sqlite:///katha.db to persist.
store = _make_store()
