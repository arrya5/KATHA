# Katha — Backend

AI interactive visual novel engine. **Phase 1 content: Vikram aur Betaal** (see
[../docs/06-phase1-vikram-betaal.md](../docs/06-phase1-vikram-betaal.md) and
[../docs/11-phase1-content-tales-and-betaal.md](../docs/11-phase1-content-tales-and-betaal.md)).
The engine is content-agnostic ([../docs/01-architecture.md](../docs/01-architecture.md)); the Mahabharata
is Phase 2 ([../docs/05-phasing-roadmap.md](../docs/05-phasing-roadmap.md)).

## Run it offline — no installs, no API keys

The core runs on the Python standard library alone.

```bash
cd backend
python -m app.webserver   # ▶ PLAY IN A BROWSER at http://127.0.0.1:8000 (no installs)
python -m app.selftest    # 22 checks incl. leak guarantees + the full-arc climax
python -m app.demo        # play the whole arc in the terminal (Prologue → 5 tales → Climax)
```

`app.webserver` is a standard-library HTTP server that wraps the same `run_turn()` the FastAPI
app uses, and serves the visual-novel client in `app/web/` — the fastest way to actually play.

## What's here (maps to docs/01)

```
app/
├── engine.py            # run_turn(request) -> SceneRender  (the public API)
├── models.py            # TurnState, WorldEvent(known_to), SceneRender, ...
├── store.py             # in-memory session state (stands in for the Postgres schema)
├── config.py            # all secrets via env; offline by default
├── llm/                 # provider-swappable: mock (offline) | gemini (stub)
├── rag/
│   ├── vector_store.py  # in-memory lexical store (swap: Chroma/Pinecone)
│   └── knowledge_state.py  # THE CORE IP: known_to + witnessed-canon filters
├── content/             # Betaal's system prompt + the tales (docs/11)
├── agents/              # turn-graph nodes + runner (LangGraph-shaped)
├── moderation/          # input classifier + output validator (docs/07)
├── api.py               # FastAPI /turn  (needs `pip install -r requirements.txt`)
├── demo.py / selftest.py
```

## Run the HTTP server (needs deps)

```bash
pip install -r requirements.txt
uvicorn app.api:app --reload
# POST /turn  {"session_id":"s1","player_input":"begin"}
```

## Turn on REAL AI (characters actually improvise)

The engine is provider-swappable (`app/llm/`). The default `mock` returns authored lines;
two real options need **no rewrite**, just an env var:

```bash
# A) Local & FREE — no API key. Needs Ollama running with a model pulled.
ollama serve            # if not already running
ollama pull hermes3
KATHA_LLM_PROVIDER=ollama KATHA_OLLAMA_MODEL=hermes3 python -m app.webserver

# B) Cloud — paid, higher quality (set the key first)
KATHA_LLM_PROVIDER=gemini GEMINI_API_KEY=... python -m app.webserver
```

Only **conversation** is generated (free-text smalltalk with Betaal + investigating tale
characters); the authored narrative beats/riddles/reactions stay pristine. Generation is
grounded in the **knowledge-state context** — a character's prompt only ever contains what it
witnessed, so even a real model cannot leak (verified by `test_prompt_context_witnessed_only`).
Any generation failure falls back to the authored line, so the game never breaks.

> Note: small local models (hermes3 ≈ 8B) may embellish or sound less polished — judge the
> *mechanics* here; prose quality jumps on a frontier model. Plan: build/test on Ollama (free),
> swap to a paid model right before launch.

### Real SEMANTIC retrieval (free, local)

By default retrieval is lexical (token overlap). For meaning-based retrieval — so investigating
a character matches intent, not keywords — turn on local embeddings:

```bash
ollama pull nomic-embed-text
KATHA_EMBEDDINGS=ollama python -m app.webserver
```

It falls back to lexical automatically if the embed model isn't available, so it never breaks.
Production swap: ChromaDB/Pinecone (which bundle their own embeddings) behind the same
`vector_store` API. The knowledge-state **witnessed-only filter still applies**, so semantic
retrieval is bounded the same way — no leaks.

## Voice (hear Betaal speak)

The web client speaks the dialogue. **Free, no key:** flip the 🔊 toggle in the browser — it uses
your browser's built-in speech, with per-character pitch/rate. **Production (Indian voices):**
```bash
SARVAM_API_KEY=... python -m app.webserver   # client now plays Sarvam Bulbul audio instead
```
Per-character voices in `app/voice/profiles.py`; Sarvam Bulbul provider in `app/voice/sarvam.py`
(`/tts` endpoint, cached). No key → `/tts` returns null → client falls back to browser speech.
Voice *input* (Sarvam Saarika STT) is the next voice step.

## Persistence (progress survives restarts)

In-memory by default. To persist (sessions, trust, dharma, flags, events, memories):
```bash
DATABASE_URL=sqlite:///katha.db python -m app.webserver
```
Standard-library SQLite (`app/persist.py`) — no install. Each session is one JSON blob;
the normalized Postgres schema (docs/01 §5) is the production target. Verified by
`test_persistence` (state survives a fresh process).

## Going to production (documented swaps, no rewrites)
- **LLM:** `KATHA_LLM_PROVIDER=gemini` + `GEMINI_API_KEY` (or `=ollama` for free local; add a provider in `app/llm/`).
- **Vectors:** `KATHA_VECTOR_STORE=chroma|pinecone` behind `vector_store.py`'s API.
- **DB:** `DATABASE_URL=sqlite:///…` works now; `postgresql://…` via SQLAlchemy for scale (reimplement `app/persist.py`).
- **Orchestration:** real **LangGraph** `StateGraph` is wired (`agents/langgraph_graph.py`) and
  is the production orchestrator — enable with `KATHA_ORCHESTRATOR=langgraph`. The stdlib runner
  (`agents/graph.py`) remains the zero-install default for the offline demo. Same nodes back both;
  verified the full arc passes under each.
- **API:** `app/api.py` (FastAPI, CORS, graceful errors) is the production surface; `app/webserver.py` is the zero-install demo.
- **Voice:** attach Sarvam STT/TTS at `api.py` (docs/01 sec 6).

See [../docs/09-build-plan.md](../docs/09-build-plan.md) for the milestone sequence.
