"""Production orchestrator: a real LangGraph StateGraph (docs/01 sec 2).

Mirrors the stdlib runner in graph.py but uses LangGraph 1.x — the industry-standard
agent-orchestration framework — for the turn graph: typed state, named nodes, and a
conditional edge (moderation short-circuit). The same node functions back both runners,
so this is a true drop-in (selected via KATHA_ORCHESTRATOR=langgraph).

Our TurnState is carried in a single LangGraph channel ("state", last-write-wins), so the
existing node logic is reused verbatim. Durable resume is handled by our SQLite persistence
(app/persist.py); a LangGraph checkpointer can be added here if per-node resume is needed.
"""
from __future__ import annotations

from typing import TypedDict

from langgraph.graph import END, StateGraph

from ..models import TurnState, Verdict
from . import nodes


class GraphState(TypedDict):
    state: TurnState


def _build(deps: "nodes.Deps"):
    def wrap(fn):                      # node takes (state, deps)
        def _node(g: GraphState) -> GraphState:
            return {"state": fn(g["state"], deps)}
        return _node

    def wrap_nodeps(fn):               # node takes (state) only
        def _node(g: GraphState) -> GraphState:
            return {"state": fn(g["state"])}
        return _node

    sg = StateGraph(GraphState)
    sg.add_node("moderation", wrap(nodes.moderation_node))
    sg.add_node("deflect", wrap_nodeps(nodes.deflection_render))
    sg.add_node("narrator", wrap(nodes.narrator_node))
    sg.add_node("agent", wrap(nodes.agent_node))
    sg.add_node("world_state", wrap(nodes.world_state_node))
    sg.add_node("validator", wrap(nodes.validator_node))
    sg.add_node("synthesizer", wrap(nodes.synthesizer_node))

    sg.set_entry_point("moderation")

    def after_moderation(g: GraphState) -> str:
        v = g["state"].moderation.verdict
        return "deflect" if v in (Verdict.BLOCK, Verdict.DEFLECT) else "narrator"

    sg.add_conditional_edges("moderation", after_moderation,
                             {"deflect": "deflect", "narrator": "narrator"})
    sg.add_edge("deflect", END)
    sg.add_edge("narrator", "agent")
    sg.add_edge("agent", "world_state")
    sg.add_edge("world_state", "validator")
    sg.add_edge("validator", "synthesizer")
    sg.add_edge("synthesizer", END)
    return sg.compile()


_compiled: dict[str, object] = {}   # cache compiled graph per provider


def run_langgraph(state: TurnState, deps: "nodes.Deps") -> TurnState:
    key = getattr(deps.provider, "name", "default")
    app = _compiled.get(key)
    if app is None:
        app = _build(deps)
        _compiled[key] = app
    out = app.invoke({"state": state})
    return out["state"]
