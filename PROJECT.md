# Katha — Master Reference

> **Read this file first. It is the single source of truth.** Everything else in `docs/` is
> deep-dive reference — open a specific doc only when you need that topic. Last updated 2026-06-19.

---

## 1. What it is (30 seconds)

**Katha** is an AI-powered interactive **visual novel**. Each character is an independent AI agent
with persistent memory and an **isolated knowledge state** (they only know what they witnessed) —
this information-asymmetry engine is the core IP and differentiator. Voice-first, built for Android
(Play Store), by **Arrya Thakur** (solo; SRM Chennai CS '27).

**Why it exists:** (1) a real, shipped portfolio piece for GenAI/Applied-AI roles (RAG,
multi-agent, voice, fine-tuning); (2) possible VC pitch if retention is strong.

**Phasing (important):** Launch on **Phase 1 = Vikram aur Betaal** (low-risk folklore; its
moral-riddle structure *is* the gameplay). **Phase 2 = Mahabharata** is the marquee arc, unlocked
only after graduation criteria (advisory board, proven retention, hardened moderation). The engine
is content-agnostic, so Phase-2 design is preserved, not wasted.

---

## 2. Run it (no installs, no API keys)

```bash
cd backend
python -m app.selftest      # 33 checks (incl. the leak guarantees) — must say ALL PASS
python -m app.demo          # play the whole arc in the terminal
python -m app.webserver     # ▶ PLAY IN BROWSER at http://127.0.0.1:8000
```

Mobile app (Expo): `cd frontend && npm start` → scan QR with **Expo Go on a real phone**
(auto-detects the backend). *Note: the API-36 emulator crashes Expo Go — use a real phone.*

---

## 3. Current state (what's actually built ✅ vs not ⬜)

| Area | State | Notes |
|---|---|---|
| Turn engine + agent graph | ✅ | `backend/app/agents/` — real **LangGraph** (+ stdlib runner fallback) |
| Knowledge-state engine (core IP) | ✅ | `rag/knowledge_state.py` — leak-proof, test-verified |
| 3-layer RAG + semantic embeddings | ✅ | lexical default; `KATHA_EMBEDDINGS=ollama` for real semantic |
| Real LLM generation | ✅ free/local | Ollama (hermes3) for off-script convo; authored beats stay fixed |
| Moderation (3-layer) | ✅ | 12/12 red-team caught, 12/12 benign allowed |
| Persistence | ✅ | SQLite (`DATABASE_URL=sqlite:///katha.db`); survives restarts |
| Content | ✅ | Prologue + 5 tales + trust-gated branching climax |
| Web client (playable) | ✅ | `app/web/index.html` over stdlib server; browser TTS voice |
| Mobile app (Expo) | ✅ runs / 🟡 polish | builds + reaches backend on a real device; voice via `expo-speech` |
| Drop-in art slots | ✅ wired / ⬜ art | `/assets/*` served; **real images not generated yet** |
| Voice — Sarvam TTS (prod) | 🟡 | provider built + `/tts` endpoint, key-gated; STT not wired |
| Cloud LLM (Gemini/Claude) | 🟡 | provider-swappable; stub until a key is set |
| Art, fine-tuning, accounts, launch | ⬜ | Phase C/D |

**The whole stack runs free + local today** (mock or Ollama). Swap to paid Claude/Gemini/Sarvam/
Pinecone/Postgres before launch — all behind interfaces, one env var each.

---

## 4. Config switches (env vars)

| Var | Default | Options |
|---|---|---|
| `KATHA_LLM_PROVIDER` | `mock` | `ollama` (free local), `gemini` |
| `KATHA_EMBEDDINGS` | `lexical` | `ollama` (needs `ollama pull nomic-embed-text`) |
| `KATHA_ORCHESTRATOR` | `simple` | `langgraph` |
| `DATABASE_URL` | (in-memory) | `sqlite:///katha.db` |
| `SARVAM_API_KEY` / `GEMINI_API_KEY` | (unset) | enable prod voice / cloud LLM |

See `backend/.env.example`.

---

## 5. Repo map

```
PROJECT.md            ← you are here (master reference)
backend/
  app/
    engine.py         run_turn(request) -> SceneRender  (the public API; logging, locks, input cap)
    models.py         TurnState, WorldEvent(known_to), SceneRender, ...
    store.py          in-memory session state  | persist.py = SQLite version
    config.py         all env/secrets
    llm/              provider-swappable: mock · ollama · gemini  (+ shared routing.py)
    rag/              vector_store · embeddings · knowledge_state (CORE IP)
    agents/           nodes.py (the 6 graph nodes) · graph.py (stdlib) · langgraph_graph.py (prod)
    moderation/       classifier.py (input) · validator.py (output)
    voice/            sarvam.py (TTS) · profiles.py (per-character voices)
    content/          tales.py (Prologue+5 tales+climax) · betaal_prompt.py
    web/index.html    playable browser client
    api.py            FastAPI (prod)  | webserver.py = stdlib (zero-install demo)
    demo.py · selftest.py · tests/
  requirements.txt · .env.example · README.md
frontend/             Expo/React Native app (App.tsx, src/{screens,components,api,config,theme})
data/
  raw/SOURCES.md      source provenance/licensing
  processed/eval/     leak · canon · red_team · false_positive  (.jsonl quality gates)
assets/               drop generated art here (backgrounds/, characters/) — see docs/14
docs/                 design + reference suite (index below) — read only when needed
```

---

## 6. Docs index (open only the one you need)

| Doc | When to open it |
|---|---|
| `00-research-and-market` | market, comps (Mythik), regulation, pitch framing |
| `01-architecture` | the engine: graph, 3-layer RAG, knowledge-state, cost/latency (design target) |
| `02-data-pipeline` | source-text sourcing (Ganguli/BORI), chunking — **Phase 2** |
| `03-npc-prompts` | Karna/Krishna/etc. character bibles — **Phase 2** |
| `04-cultural-fidelity` | the reverence rules + advisory board (the #1 risk) |
| `05-phasing-roadmap` | why Phase 1 first + Phase-2 graduation criteria |
| `06-phase1-vikram-betaal` | **the current product**: world, loop, Betaal/Vikramaditya |
| `07-moderation-and-safety` | the 3-layer guardrails + red-team |
| `08-legal-and-compliance` | Online Gaming Act 2025/Rules 2026, DPDP, ToS |
| `09-build-plan` | milestone plan (M0–M4 done; M5 voice, M6 art, M7 launch) |
| `10-business-and-pitch` | monetization, unit economics, funding path |
| `11-phase1-content-tales-and-betaal` | Betaal's prompt + Tale 1 worked example |
| `12-resume-mapping` | **skill → proof → résumé bullet** (Arrya's CV evidence) |
| `13-phase1-tales-2-4-and-meta-arc` | tales 2–5 + Prologue + the conspiracy meta-arc |
| `14-art-direction-and-prompts` | art direction + **copy-paste image-gen prompts** + asset spec |

---

## 7. Known issues / gotchas
- **Expo Go crashes on the API-36 emulator** (bundled reanimated `ClassCastException`) — an
  environment bug, not our code. Test the mobile app on a **real phone** or a dev build.
- **Local Ollama (hermes3 8B) embellishes** — never leaks (guarantee holds), but prose is rough;
  frontier model fixes it. Build on Ollama → swap before launch.
- **Real art not generated yet** — slots are wired; produce images per `docs/14`, drop in `assets/`.
- **doc-02 text-ingestion pipeline not run** — canon is hand-authored tale facts (fine for MVP).
- **Research figures** in doc 00 are point-in-time / partly secondary sources — re-verify before a pitch.

---

## 8. What's next (roadmap)
- **Phase C — experience:** generate **art** (biggest visual leap, needs your image-gen account) ·
  **Sarvam voice** (free credits) · mobile UI polish.
- **Phase D — ship:** accounts, analytics/retention, the pre-launch **hardening pass** (rate-limit,
  observability), legal docs, Play Store.
- **Then Phase 2 (Mahabharata)** once graduation criteria are met.

Details: `docs/09-build-plan.md`. Original founder vision: `HANDOFF.md` (historical).
Persistent context lives in Claude memory at `…/c--Katha/memory/`.
