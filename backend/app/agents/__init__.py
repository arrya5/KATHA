"""The turn graph (docs/01 sec 2).

Implemented here as discrete node functions over a typed TurnState plus a tiny
sequential runner (graph.py). This mirrors LangGraph's model exactly (typed state,
named nodes, conditional routing) so migrating to LangGraph 1.0 is a wrapping exercise,
not a rewrite — done at the milestone where checkpointing/persistence is needed.
"""
