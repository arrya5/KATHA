# Katha — Backend

AI interactive visual novel engine. **Phase 1 content: Vikram aur Betaal.**
The engine is content-agnostic; the Mahabharata is Phase 2. See the
[root README](../README.md) and the [technical writeup](../docs/blog/leak-proof-agents.md)
for the architecture and the knowledge-isolation design.

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

## Voice — hear Betaal speak (Sarvam Bulbul v3)

The web client speaks every character's dialogue. Two modes:

### Free — browser speech (no setup)
Flip the **🔊 Voice** toggle in the browser. Uses the browser's built-in `SpeechSynthesis`
with per-character pitch/rate hints. Works offline, sounds generic.

### Production — authentic Indian voices (Sarvam Bulbul v3)

1. **Get a free API key** at [dashboard.sarvam.ai](https://dashboard.sarvam.ai)
   (free credits on signup; no card required for development).

2. **Set the key** — either in `backend/.env` (recommended):
   ```
   SARVAM_API_KEY=your_key_here
   ```
   or inline:
   ```bash
   SARVAM_API_KEY=your_key_here python -m app.webserver
   ```

3. **Start the server** and open the browser at `http://127.0.0.1:8000`.
   The **🔊 Voice** toggle now shows **🔊 Sarvam** when active and plays real Indian voices.

4. **Verify** it's working:
   ```bash
   # Check that tts_enabled is true
   curl http://127.0.0.1:8000/season
   # → {"order": [...], "tts_enabled": true}

   # Synthesise a test line directly
   curl -X POST http://127.0.0.1:8000/tts \
     -H "Content-Type: application/json" \
     -d '{"text": "Sunte hain, raja?", "voice_profile": "betaal_sonorous"}' | python -c "import json,sys; d=json.load(sys.stdin); print('OK, audio bytes:', len(d['audio'] or ''))"
   ```

### Per-character voice design (`app/voice/profiles.py`)

Each character is mapped to a distinct [Bulbul v3](https://docs.sarvam.ai) speaker with tuned
`pace` (speed) and `temperature` (expressiveness):

| Character | Speaker | Why |
|---|---|---|
| **Betaal** | `kabir` | Deep, resonant, theatrical — sounds ancient and mischievous |
| **Vikramaditya** | `rahul` | Measured, commanding — a just king |
| **Narrator** | `aditya` | Clear, articulate — clean storytelling voice |
| **Kshantishila** | `manan` | Smooth, persuasive — perfect oiliness for the mendicant |
| **Grave female** (Madanasundari in grief) | `roopa` | Deep female, sorrowful |
| **Soft female** (Madanasundari calm) | `priya` | Warm, gentle |
| **Child** | `ashutosh` | Lightest male voice |
| **Broken/grief** (Viravara) | `dev` | Strained, weighted |

Betaal's pace is set to `0.82` (deliberately slow, dramatic) with `temperature: 1.3`
(high expressiveness). Add or tune profiles in `profiles.py` — no code change elsewhere needed.

### How the audio pipeline works

```
/tts endpoint  →  sarvam.synthesize(text, profile, language)
               →  POST api.sarvam.ai/text-to-speech
                    body: {text, speaker, model:"bulbul:v3",
                           target_language_code:"hi-IN",
                           properties: {pace, temperature}}
               →  base64 WAV  →  cached in _CACHE[text, profile, lang]
               →  client: AudioContext.decodeAudioData → play
```

No key or failure → `/tts` returns `null` → client falls back to browser speech silently.
TTS results are cached in-process (same line/profile/language = one API call ever).

### STT (voice *input*) — next step
Sarvam Saarika STT is architecturally wired in `config.py` (`sarvam_stt_url`). The
`/stt` endpoint and frontend microphone capture are the next voice milestone.


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
- **Voice:** attach Sarvam STT/TTS at `api.py`.
