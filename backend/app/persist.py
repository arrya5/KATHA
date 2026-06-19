"""SQLite persistence — progress survives restarts. Standard library only (no SQLAlchemy
install needed for the local/free build; SQLAlchemy + Postgres is the documented prod swap,
docs/01 sec 5).

Each session is stored as one JSON blob (the whole SessionState). That's deliberately
simple and durable for the MVP; the normalized schema in docs/01 is the production target.
Enable with DATABASE_URL=sqlite:///katha.db.

Thread-safe for the dev web server via connect-per-operation (ThreadingHTTPServer).
"""
from __future__ import annotations

import json
import sqlite3
import threading
from contextlib import closing
from dataclasses import asdict

from .models import Memory, WorldEvent
from .store import SceneRuntime, SessionState, SessionStore


def _serialize(s: SessionState) -> str:
    return json.dumps(asdict(s))


def _deserialize(sid: str, text: str) -> SessionState:
    d = json.loads(text)
    return SessionState(
        session_id=sid,
        turn_no=d.get("turn_no", 0),
        strikes=d.get("strikes", 0),
        dharma_score=d.get("dharma_score", 0),
        trust=d.get("trust", {}),
        dharma_log=d.get("dharma_log", []),
        flags=d.get("flags", {}),
        scene=SceneRuntime(**d.get("scene", {})),
        events=[WorldEvent(**e) for e in d.get("events", [])],
        memories=[Memory(**m) for m in d.get("memories", [])],
    )


class SqliteSessionStore(SessionStore):
    def __init__(self, path: str) -> None:
        super().__init__()
        self.path = path or "katha.db"
        self._lock = threading.Lock()
        # closing() ensures the connection is CLOSED (sqlite3's own context manager only
        # commits/rolls back) — important on Windows, where an open handle locks the file.
        with closing(sqlite3.connect(self.path)) as c:
            c.execute("CREATE TABLE IF NOT EXISTS sessions "
                      "(session_id TEXT PRIMARY KEY, state TEXT, updated_at TEXT)")
            c.commit()

    def get(self, session_id: str) -> SessionState:
        if session_id in self._sessions:
            return self._sessions[session_id]
        with closing(sqlite3.connect(self.path)) as c:
            row = c.execute("SELECT state FROM sessions WHERE session_id=?",
                            (session_id,)).fetchone()
        self._sessions[session_id] = (
            _deserialize(session_id, row[0]) if row else SessionState(session_id=session_id)
        )
        return self._sessions[session_id]

    def save(self, session_id: str) -> None:
        s = self._sessions.get(session_id)
        if s is None:
            return
        data = _serialize(s)
        with self._lock, closing(sqlite3.connect(self.path)) as c:
            c.execute(
                "INSERT INTO sessions (session_id, state, updated_at) "
                "VALUES (?, ?, datetime('now')) "
                "ON CONFLICT(session_id) DO UPDATE SET state=excluded.state, "
                "updated_at=excluded.updated_at",
                (session_id, data),
            )
            c.commit()
