"""Best-effort player telemetry — an append-only event log for real usage data.

The whole point of this module: get accurate, durable numbers about how people actually
play (how many, how far, where they drop off) without ever slowing down or breaking a turn.

Design guarantees:
  * NEVER blocks a turn. emit() drops the event on a bounded queue and returns; a single
    daemon thread flushes to the backend.
  * NEVER breaks a turn. Every failure (network, disk, bad config) is swallowed and logged
    at DEBUG. A dead analytics backend is invisible to the player.
  * Zero new dependencies. Supabase is written over its PostgREST REST endpoint using
    stdlib urllib, matching the project's zero-install ethos.

Backend is chosen automatically (see config.py):
  * Supabase   — SUPABASE_URL + SUPABASE_SERVICE_KEY set. Durable; survives HF restarts.
  * SQLite     — else, if KATHA_ANALYTICS_DB is set. Local dev/offline capture.
  * Disabled   — else (or KATHA_ANALYTICS=0). emit() is a no-op; nothing is written.

Row schema (one row per event):
  event_id TEXT PK, ts TEXT (UTC ISO-8601), player_id TEXT, session_id TEXT,
  event_type TEXT, tale_id TEXT, turn_no INT, payload JSON

The Supabase table DDL is documented at the bottom of this file.
"""
from __future__ import annotations

import atexit
import json
import logging
import queue
import sqlite3
import threading
import time
import urllib.request
import uuid
from contextlib import closing
from datetime import datetime, timezone

from .config import settings

log = logging.getLogger("katha.analytics")

_QUEUE_MAX = 10_000
_HTTP_TIMEOUT = 10


# --- Backends ---------------------------------------------------------------
class _SqliteWriter:
    """Connect-per-write (Windows-safe, like persist.py). Idempotent on event_id."""

    def __init__(self, path: str) -> None:
        self.path = path
        with closing(sqlite3.connect(self.path)) as c:
            c.execute(
                "CREATE TABLE IF NOT EXISTS events ("
                "event_id TEXT PRIMARY KEY, ts TEXT, player_id TEXT, session_id TEXT, "
                "event_type TEXT, tale_id TEXT, turn_no INTEGER, payload TEXT)"
            )
            c.execute("CREATE INDEX IF NOT EXISTS idx_events_ts ON events(ts)")
            c.execute("CREATE INDEX IF NOT EXISTS idx_events_type ON events(event_type)")
            c.commit()

    def write(self, evt: dict) -> None:
        with closing(sqlite3.connect(self.path)) as c:
            c.execute(
                "INSERT OR IGNORE INTO events "
                "(event_id, ts, player_id, session_id, event_type, tale_id, turn_no, payload) "
                "VALUES (?,?,?,?,?,?,?,?)",
                (evt["event_id"], evt["ts"], evt["player_id"], evt["session_id"],
                 evt["event_type"], evt["tale_id"], evt["turn_no"], json.dumps(evt["payload"])),
            )
            c.commit()


class _SupabaseWriter:
    """POST one row to the PostgREST endpoint. The service key stays server-side only."""

    def __init__(self, base_url: str, key: str) -> None:
        self.endpoint = base_url.rstrip("/") + "/rest/v1/events"
        self._headers = {
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal,resolution=ignore-duplicates",
        }

    def write(self, evt: dict) -> None:
        data = json.dumps(evt).encode("utf-8")
        req = urllib.request.Request(self.endpoint, data=data, method="POST", headers=self._headers)
        with urllib.request.urlopen(req, timeout=_HTTP_TIMEOUT) as resp:
            resp.read()


def _make_writer():
    if not settings.analytics_enabled:
        return None
    if settings.supabase_url and settings.supabase_service_key:
        log.info("analytics: Supabase backend")
        return _SupabaseWriter(settings.supabase_url, settings.supabase_service_key)
    if settings.analytics_db:
        log.info("analytics: local SQLite backend (%s)", settings.analytics_db)
        return _SqliteWriter(settings.analytics_db)
    return None  # disabled — no backend configured


# --- Async telemetry pump ---------------------------------------------------
class _Telemetry:
    def __init__(self) -> None:
        self._q: queue.Queue = queue.Queue(maxsize=_QUEUE_MAX)
        self._writer = None
        self._started = False
        self._lock = threading.Lock()
        self._seen: set[str] = set()          # sessions we've already emitted session_start for
        self._seen_lock = threading.Lock()

    def _ensure_started(self) -> None:
        if self._started:
            return
        with self._lock:
            if self._started:
                return
            try:
                self._writer = _make_writer()
            except Exception as e:            # bad config / unwritable path — stay disabled
                log.debug("analytics init failed: %s", e)
                self._writer = None
            if self._writer is not None:
                threading.Thread(target=self._run, name="katha-analytics", daemon=True).start()
            self._started = True

    def first_seen(self, session_id: str) -> bool:
        """True exactly once per session_id per process — used to fire session_start."""
        with self._seen_lock:
            if session_id in self._seen:
                return False
            self._seen.add(session_id)
            return True

    def emit(self, event_type: str, *, session_id: str = "", player_id: str = "",
             tale_id: str = "", turn_no: int = 0, **payload) -> None:
        self._ensure_started()
        if self._writer is None:
            return
        evt = {
            "event_id": uuid.uuid4().hex,
            "ts": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "session_id": session_id or "",
            "player_id": player_id or "",
            "tale_id": tale_id or "",
            "turn_no": int(turn_no or 0),
            "payload": {k: v for k, v in payload.items() if v is not None},
        }
        try:
            self._q.put_nowait(evt)
        except queue.Full:
            log.debug("analytics queue full; dropping %s", event_type)

    def _run(self) -> None:
        while True:
            evt = self._q.get()
            try:
                self._writer.write(evt)
            except Exception as e:
                log.debug("analytics write failed (%s): %s", evt.get("event_type"), e)
            finally:
                self._q.task_done()

    def flush(self, timeout: float = 2.0) -> None:
        """Best-effort drain for short-lived processes (demo/CLI). Never raises."""
        if self._writer is None:
            return
        deadline = time.monotonic() + timeout
        while not self._q.empty() and time.monotonic() < deadline:
            time.sleep(0.02)


_tel = _Telemetry()


def emit(event_type: str, **kwargs) -> None:
    """Fire-and-forget. Any error here is swallowed so a turn can never fail on telemetry."""
    try:
        _tel.emit(event_type, **kwargs)
    except Exception:  # pragma: no cover - defensive; emit must never raise into a turn
        pass


def first_seen(session_id: str) -> bool:
    try:
        return _tel.first_seen(session_id)
    except Exception:  # pragma: no cover
        return False


def flush(timeout: float = 2.0) -> None:
    try:
        _tel.flush(timeout)
    except Exception:  # pragma: no cover
        pass


atexit.register(flush)


# ---------------------------------------------------------------------------
# Supabase table (run once in the SQL editor):
#
#   create table if not exists public.events (
#     event_id   text primary key,
#     ts         timestamptz not null default now(),
#     player_id  text,
#     session_id text,
#     event_type text,
#     tale_id    text,
#     turn_no    int,
#     payload    jsonb
#   );
#   create index if not exists idx_events_ts   on public.events (ts);
#   create index if not exists idx_events_type on public.events (event_type);
#   -- Writes come from the server using the service key, which bypasses RLS.
#   -- Leave RLS enabled with no public policy so the anon key cannot read/write.
#   alter table public.events enable row level security;
# ---------------------------------------------------------------------------
