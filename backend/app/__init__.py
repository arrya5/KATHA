"""Katha backend — AI interactive visual novel engine.

Phase 1 content: Vikram aur Betaal (see docs/06, docs/11).
The engine is content-agnostic (docs/01); Phase 2 swaps in the Mahabharata.

The CORE of this package (models, rag, agents, llm.mock, engine) runs offline with
the standard library only, so the knowledge-state guarantees and a full turn can be
demonstrated and tested without any API keys. The production swaps (LangGraph,
ChromaDB/Pinecone, Gemini, Sarvam) are documented stubs in their respective modules.
"""

__version__ = "0.1.0"
