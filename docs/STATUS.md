# Katha — Implementation Status

> **The single source of truth for what is actually built**, as opposed to designed/planned.
> The numbered docs (00–13) are the *design + plan*; this file tracks the *code*.
> Last updated: 2026-06-17.
>
> Legend: ✅ built & verified · 🟡 partial / scaffolded · ⬜ designed, not built.

---

## How to run / verify (no installs, no API keys)
```bash
cd backend
python -m app.selftest      # 33 checks — ALL PASS (incl. the leak guarantees)
python -m app.demo          # play the whole arc in the terminal
python -m app.webserver     # play in a browser at http://127.0.0.1:8000
```
Optional real-AI (free, local — needs Ollama):
```bash
KATHA_LLM_PROVIDER=ollama KATHA_EMBEDDINGS=ollama \
DATABASE_URL=sqlite:///katha.db KATHA_ORCHESTRATOR=langgraph \
python -m app.webserver
```

---

## Built & verified ✅

| Area | What exists | Where |
|---|---|---|
| **Turn engine** | content-agnostic graph: moderation → narrator → agent → world-state → validator → synthesizer | `app/engine.py`, `app/agents/` |
| **Orchestrator (real LangGraph)** | LangGraph 1.2.5 `StateGraph` (typed state, conditional moderation edge) **+** stdlib runner fallback; full arc passes under both | `app/agents/langgraph_graph.py`, `graph.py` |
| **Knowledge-state engine (core IP)** | `known_to` event filter + witnessed-canon filter; bounds the prompt so even a real model can't leak | `app/rag/knowledge_state.py` |
| **3-layer RAG** | L1 canon + L2 world events + L3 per-agent memory | `app/rag/`, `app/store.py` |
| **Semantic retrieval** | real embeddings (Ollama, free local) + cosine vector store; lexical fallback; verified meaning-based match | `app/rag/embeddings.py`, `vector_store.py` |
| **Real LLM generation** | Ollama provider (hermes3) for off-script conversation; authored narrative stays pristine; fallback on failure | `app/llm/ollama.py`, `agents/nodes.py` |
| **Provider abstraction** | mock (offline) · ollama (real local) · gemini (cloud stub) | `app/llm/` |
| **Moderation (3-layer)** | classifier (self-harm/hate/sexual/jailbreak/abuse) + in-character deflection + output validator; 12/12 red-team caught, 12/12 benign allowed | `app/moderation/`, `data/processed/eval/` |
| **Persistence** | SQLite session store; progress survives restarts (verified across 2 processes) | `app/persist.py` |
| **Content** | Prologue (Kshantishila frame) + 5 tales + trust-gated branching climax; mendicant-suspicion flag | `app/content/tales.py`, `betaal_prompt.py` |
| **Web UI** | playable visual-novel client (scene, typewriter, choices, HUD) over a stdlib server | `app/web/index.html`, `app/webserver.py` |
| **HTTP API** | FastAPI `/turn`, `/season`, `/health`, CORS, graceful errors | `app/api.py` |
| **Tests/evals** | 33 self-tests + pytest wrapper + 4 eval sets | `app/selftest.py`, `tests/`, `data/processed/eval/` |

---

## Partial / scaffolded 🟡

| Area | State |
|---|---|
| **Voice — TTS** | The web client **speaks dialogue now** via the browser's built-in speech (free, no key). Sarvam Bulbul provider + `/tts` endpoint + per-character voice profiles are built and key-gated (`SARVAM_API_KEY`) but untested without a key. **STT (voice input) not yet wired.** | `app/voice/`, `app/web/index.html` |
| **Mobile app (Expo)** | Full RN/Expo scaffold written (`frontend/`) — **not yet compiled/run on a device** (needs `npm install && npm start` + backend running). |
| **Gemini provider** | Wired but untested; needs `GEMINI_API_KEY` + `pip install google-generativeai`; default model `gemini-1.5-pro` should be updated to a current model. |
| **Cost/latency budget** | Designed (doc 01 §7); not yet measured on a real model. |

---

## Designed, not built ⬜

- **Voice — STT (Sarvam Saarika / browser SpeechRecognition)** — voice *input* not yet wired (TTS output is done; see Partial). (Phase C / M5)
- **Art & sound assets** — **drop-in slots are wired** (`/assets/backgrounds/*`, `/assets/characters/*`;
  client uses real art if present, else procedural gradients + glyphs). The actual painted
  backgrounds/portraits are **not generated yet** — produce via Midjourney/Flux/Nano Banana from
  the prompt pack in [14-art-direction-and-prompts.md](14-art-direction-and-prompts.md) and drop into `assets/`. (Phase C / M6)
- **Doc-02 text-ingestion pipeline** — chunking/embedding the *full* Baital Pachisi has **not** been run; current canon is hand-authored tale facts (sufficient for the MVP). The Mahabharata (Ganguli) corpus is Phase 2.
- **Accounts, analytics/retention instrumentation, monetization, Play Store** — none yet. (Phase D / M7–M8)
- **Fine-tuning (LoRA)** — planned optimization, not started. (M8)
- **Phase 2 (Mahabharata)** — fully designed (docs 02–04), held until graduation criteria ([05](05-phasing-roadmap.md) §4).

---

## Known limitations / caveats
- **Small local model embellishes.** hermes3 (8B) can invent minor details; it never leaks the
  *secret* (guarantee holds), and prose quality jumps on a frontier model. Build on Ollama → swap
  to Claude/Gemini before launch.
- **Lexical retrieval is a stand-in** when embeddings are off (default); semantic mode (Ollama)
  fixes relevance. Production swaps to Chroma/Pinecone.
- **Content accuracy pending review.** Tale resolutions (esp. Tale 5 and Viravara variants) need a
  final check vs Ryder/Forbes before public launch — flagged in docs 11/13 and `data/raw/SOURCES.md`.
- **Research figures are point-in-time** and partly from secondary sources — re-verify before any
  pitch (doc 00).

---

## Provider/mode switches (env)
| Var | Default | Options |
|---|---|---|
| `KATHA_LLM_PROVIDER` | `mock` | `ollama`, `gemini` |
| `KATHA_EMBEDDINGS` | `lexical` | `ollama` |
| `KATHA_ORCHESTRATOR` | `simple` | `langgraph` |
| `DATABASE_URL` | (in-memory) | `sqlite:///katha.db`, `postgresql://…` |

See `backend/.env.example` and `backend/README.md`.
