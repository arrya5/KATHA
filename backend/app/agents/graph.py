"""The turn graph runner (docs/01 sec 2.3).

Sequential mirror of the LangGraph graph:
  moderation -> (block/deflect ? deflection : narrator -> agent -> world_state
                 -> validator -> synthesizer)
Swap this for a LangGraph StateGraph (same nodes) when checkpointing/persistence is
needed; the node functions are already LangGraph-shaped.
"""
from __future__ import annotations

from ..models import TurnState, Verdict
from . import nodes


def run_graph(state: TurnState, deps: "nodes.Deps") -> TurnState:
    state = nodes.moderation_node(state, deps)

    if state.moderation.verdict in (Verdict.BLOCK, Verdict.DEFLECT):
        return nodes.deflection_render(state)

    state = nodes.narrator_node(state, deps)
    state = nodes.agent_node(state, deps)
    state = nodes.world_state_node(state, deps)
    state = nodes.validator_node(state, deps)
    state = nodes.synthesizer_node(state, deps)
    return state
