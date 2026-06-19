"""3-layer RAG (docs/01 sec 3, docs/02).

L1 canon  -> vector_store collection `canon`
L2 events -> SessionStore.events, filtered by known_to (knowledge_state)
L3 memory -> SessionStore.memories, per npc (knowledge_state)
"""
