"""Public turn API: request in, SceneRender out.

This is what both the FastAPI route and the offline demo call.
"""
from __future__ import annotations

import logging
import threading
import time

from . import content  # noqa: F401  (import side-effect: loads canon into the vector store)
from .agents.graph import run_graph
from .agents.nodes import Deps
from .config import settings
from .content.tales import TALES
from .llm import get_provider
from .models import SceneRender, TurnRequest, TurnState
from .rag.knowledge_state import engine as knowledge_engine
from .store import SceneRuntime, store

log = logging.getLogger("katha")

MAX_INPUT_CHARS = 2000   # reject absurd input (abuse / runaway LLM cost)

# Per-session locks: serialize turns for the SAME session (so concurrent requests can't
# corrupt one session's state), while different sessions still run in parallel.
_locks: dict[str, threading.Lock] = {}
_locks_guard = threading.Lock()


def _session_lock(session_id: str) -> threading.Lock:
    with _locks_guard:
        return _locks.setdefault(session_id, threading.Lock())


def _orchestrate(state: TurnState, deps: Deps) -> TurnState:
    if settings.orchestrator == "langgraph":
        from .agents.langgraph_graph import run_langgraph
        return run_langgraph(state, deps)
    return run_graph(state, deps)


def run_turn(request: TurnRequest) -> SceneRender:
    # Input-size cap (defensive): truncate rather than fail.
    if request.player_input and len(request.player_input) > MAX_INPUT_CHARS:
        request.player_input = request.player_input[:MAX_INPUT_CHARS]

    with _session_lock(request.session_id):
        t0 = time.perf_counter()

        s = store.get(request.session_id)

        if request.player_input == "__refresh__":
            from .agents.nodes import refresh_render
            render = refresh_render(request.session_id, request.language or "en", get_provider())
            from dataclasses import asdict
            s.last_render = asdict(render)
            s.language = request.language or "en"
            store.save(request.session_id)
            return render

        # Tale selection / season progression: when the client names a known tale and it
        # differs from the one in progress, start that tale fresh (resets the scene runtime).
        # Empty or repeated scene_id keeps the current tale mid-play.
        if request.scene_id in TALES:
            scene = s.scene
            if scene.tale_id != request.scene_id:
                s.scene = SceneRuntime(tale_id=request.scene_id)

        state = TurnState(request=request, scene_id=request.scene_id)
        deps = Deps(provider=get_provider(), knowledge=knowledge_engine)
        state = _orchestrate(state, deps)
        assert state.render is not None

        from dataclasses import asdict
        s.last_render = asdict(state.render)
        s.language = request.language or "en"

        store.save(request.session_id)   # persist progress (no-op for the in-memory store)

        ms = int((time.perf_counter() - t0) * 1000)
        m = state.render.meta
        log.info("turn sid=%s scene=%s intent=%s fallback=%s %dms",
                 request.session_id, request.scene_id or m.get("background", "-"),
                 m.get("intent", "-"), state.render.fallback_used, ms)
        return state.render
