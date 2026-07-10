"""Turn the raw event log into the numbers you can quote in an interview.

    python -m app.stats            # human-readable summary
    python -m app.stats --json     # machine-readable (for a dashboard / README badge)

Reads from whichever analytics backend is configured (see analytics.py / config.py):
  * Supabase  — SUPABASE_URL + SUPABASE_SERVICE_KEY
  * SQLite    — KATHA_ANALYTICS_DB
It computes everything from the append-only `events` table, so the numbers are derived,
never hand-maintained. Nothing here writes; it is read-only.
"""
from __future__ import annotations

import json
import sqlite3
import urllib.parse
import urllib.request
from collections import Counter
from contextlib import closing

from .config import settings

_HTTP_TIMEOUT = 30


# --- Load every event, backend-agnostic ------------------------------------
def _load_sqlite(path: str) -> list[dict]:
    with closing(sqlite3.connect(path)) as c:
        c.row_factory = sqlite3.Row
        rows = c.execute(
            "SELECT event_id, ts, player_id, session_id, event_type, tale_id, turn_no, payload "
            "FROM events"
        ).fetchall()
    out = []
    for r in rows:
        d = dict(r)
        try:
            d["payload"] = json.loads(d["payload"]) if d["payload"] else {}
        except (TypeError, json.JSONDecodeError):
            d["payload"] = {}
        out.append(d)
    return out


def _load_supabase(base_url: str, key: str) -> list[dict]:
    endpoint = base_url.rstrip("/") + "/rest/v1/events"
    headers = {"apikey": key, "Authorization": f"Bearer {key}"}
    out: list[dict] = []
    page, size = 0, 1000
    while True:
        q = urllib.parse.urlencode({"select": "*", "order": "ts.asc"})
        req = urllib.request.Request(f"{endpoint}?{q}", headers={
            **headers, "Range-Unit": "items", "Range": f"{page * size}-{page * size + size - 1}",
        })
        with urllib.request.urlopen(req, timeout=_HTTP_TIMEOUT) as resp:
            batch = json.loads(resp.read() or b"[]")
        out.extend(batch)
        if len(batch) < size:
            break
        page += 1
    return out


def load_events() -> list[dict]:
    if settings.supabase_url and settings.supabase_service_key:
        return _load_supabase(settings.supabase_url, settings.supabase_service_key)
    if settings.analytics_db:
        return _load_sqlite(settings.analytics_db)
    raise SystemExit(
        "No analytics backend configured. Set SUPABASE_URL + SUPABASE_SERVICE_KEY, "
        "or KATHA_ANALYTICS_DB=katha_analytics.db for local capture."
    )


# --- Derive the metrics -----------------------------------------------------
def summarize(events: list[dict]) -> dict:
    players = {e.get("player_id") for e in events if e.get("player_id")}
    sessions = {e.get("session_id") for e in events if e.get("session_id")}

    # A returning player is one seen in more than one session.
    sessions_by_player: dict[str, set] = {}
    for e in events:
        pid, sid = e.get("player_id"), e.get("session_id")
        if pid and sid:
            sessions_by_player.setdefault(pid, set()).add(sid)
    returning = sum(1 for s in sessions_by_player.values() if len(s) > 1)

    turns = [e for e in events if e.get("event_type") == "turn"]
    turns_per_session: Counter = Counter()
    for e in turns:
        turns_per_session[e.get("session_id")] += 1
    counts = sorted(turns_per_session.values())
    median_turns = counts[len(counts) // 2] if counts else 0

    tale_starts = Counter(e.get("tale_id") for e in events if e.get("event_type") == "tale_start")
    tale_completes = Counter(e.get("tale_id") for e in events if e.get("event_type") == "tale_complete")
    season_completes = sum(1 for e in events if e.get("event_type") == "season_complete")

    started_sessions = len({e.get("session_id") for e in events
                            if e.get("event_type") in ("tale_start", "turn")})
    completion_rate = round(season_completes / started_sessions, 3) if started_sessions else 0.0

    intents = Counter(e["payload"].get("intent") for e in turns
                      if isinstance(e.get("payload"), dict) and e["payload"].get("intent"))
    fallback_turns = sum(1 for e in turns
                         if isinstance(e.get("payload"), dict) and e["payload"].get("fallback"))

    return {
        "total_events": len(events),
        "unique_players": len(players),
        "returning_players": returning,
        "total_sessions": len(sessions),
        "total_turns": len(turns),
        "median_turns_per_session": median_turns,
        "tale_starts": dict(tale_starts),
        "tale_completes": dict(tale_completes),
        "season_completes": season_completes,
        "completion_rate": completion_rate,
        "intent_mix": dict(intents),
        "fallback_turns": fallback_turns,
        "first_event": events[0]["ts"] if events else None,
        "last_event": events[-1]["ts"] if events else None,
    }


def _print_human(s: dict) -> None:
    print("\n  KATHA - player analytics")
    print("  " + "-" * 42)
    print(f"  unique players            : {s['unique_players']}")
    print(f"  returning players (>1 run): {s['returning_players']}")
    print(f"  sessions (playthroughs)   : {s['total_sessions']}")
    print(f"  turns played              : {s['total_turns']}")
    print(f"  median turns / session    : {s['median_turns_per_session']}")
    print(f"  season completions        : {s['season_completes']}  "
          f"(rate {s['completion_rate']:.0%})")
    if s["tale_starts"]:
        print("\n  per-tale funnel (started -> completed):")
        for tale, started in s["tale_starts"].items():
            done = s["tale_completes"].get(tale, 0)
            print(f"    {tale:<22} {started:>4} -> {done:>4}")
    if s["intent_mix"]:
        print("\n  intent mix:")
        for k, v in sorted(s["intent_mix"].items(), key=lambda kv: -kv[1]):
            print(f"    {k:<14} {v}")
    span = f"{s['first_event']}  ->  {s['last_event']}" if s["first_event"] else "no events yet"
    print(f"\n  window: {span}\n")


def main() -> None:
    import sys
    events = sorted(load_events(), key=lambda e: e.get("ts") or "")
    s = summarize(events)
    if "--json" in sys.argv:
        print(json.dumps(s, indent=2))
    else:
        _print_human(s)


if __name__ == "__main__":
    main()
