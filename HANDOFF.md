# Katha — AI Interactive Mythology App
## Handoff Document (read this at the start of every new session)

---

> ## ⚠️ Read the `docs/` suite — this HANDOFF is the vision; the docs are the plan
>
> Since this HANDOFF was written, the project was researched in depth and two decisions changed
> the plan. **Read [docs/05-phasing-roadmap.md](docs/05-phasing-roadmap.md) first**, then the rest:
>
> 1. **Phased launch.** Katha does **not** launch on the Mahabharata (its religious sensitivity
>    is a make-or-break risk). **Phase 1 = Vikram aur Betaal** (folklore; its moral-riddle
>    structure *is* the choice engine). **Phase 2 = Mahabharata** as the marquee arc, unlocked by
>    explicit graduation criteria. The engine is content-agnostic, so the Mahabharata design
>    below is preserved as the Phase-2 playbook (docs 02–04).
> 2. **Regulation updated.** "IT Rules 2021" is outdated for games — see the
>    Online Gaming Act 2025 / Rules 2026 in [docs/08-legal-and-compliance.md](docs/08-legal-and-compliance.md).
>
> **Doc suite** (▶ **[STATUS — what's actually built](docs/STATUS.md)** ◀ read this for current state):
> [00 Research & Market](docs/00-research-and-market.md) ·
> [01 Architecture](docs/01-architecture.md) ·
> [02 Data Pipeline](docs/02-data-pipeline.md) ·
> [03 NPC Prompts (Phase 2)](docs/03-npc-prompts.md) ·
> [04 Cultural Fidelity](docs/04-cultural-fidelity.md) ·
> [05 Phasing Roadmap](docs/05-phasing-roadmap.md) ·
> [06 Phase 1: Vikram aur Betaal](docs/06-phase1-vikram-betaal.md) ·
> [07 Moderation & Safety](docs/07-moderation-and-safety.md) ·
> [08 Legal & Compliance](docs/08-legal-and-compliance.md) ·
> [09 Build Plan](docs/09-build-plan.md) ·
> [10 Business & Pitch](docs/10-business-and-pitch.md) ·
> [11 Phase-1 Content & Betaal](docs/11-phase1-content-tales-and-betaal.md) ·
> [12 Résumé Mapping](docs/12-resume-mapping.md) ·
> [13 Tales 2–4 & Meta-Arc](docs/13-phase1-tales-2-4-and-meta-arc.md)
>
> **Code — it's playable, with real AI.** A runnable engine + UI exist. The full Phase-1 arc
> (Prologue → 5 tales → trust-gated Climax) runs **offline with no API keys, no installs**:
> - **Play in a browser:** `cd backend && python -m app.webserver` → http://127.0.0.1:8000
> - **Terminal playthrough:** `python -m app.demo` · **Tests:** `python -m app.selftest` (33 checks pass)
> - **Mobile app (Play Store target):** Expo/React Native scaffold in [frontend/](frontend/) (`npm install && npm start`).
>
> Engine: knowledge-state RAG, **real LangGraph 1.x** agent graph (`KATHA_ORCHESTRATOR=langgraph`;
> stdlib runner is the zero-install default), hardened 3-layer moderation, memory, branching finale.
> **Real AI on the free/local path:** Ollama provider (`KATHA_LLM_PROVIDER=ollama`) for in-character
> generation + semantic embeddings (`KATHA_EMBEDDINGS=ollama`); **SQLite persistence**
> (`DATABASE_URL=sqlite:///katha.db`) so progress survives restarts. All swap to Claude/Gemini/
> Pinecone/Postgres before launch. **Current build state: [docs/STATUS.md](docs/STATUS.md).**
> Content in `backend/app/content/`. See [backend/README.md](backend/README.md) and [frontend/README.md](frontend/README.md).

---

## What Katha Is

An AI-powered interactive fiction app set in Indian mythology. Users don't read the Mahabharata — they live inside it. Every character (Karna, Krishna, Draupadi, Arjuna) is an independent AI agent with their own personality, persistent memory of past conversations, and their own knowledge state (they only know what they were present for). Story shifts based on player choices and moral decisions. Voice-first in Hindi and English via Sarvam AI.

**This is not a chatbot. It is a visual novel with AI NPCs.**

The format: full-screen cinematic scene backgrounds (AI-generated art), character portrait standing on screen, dialogue panel at the bottom with typewriter animation, voice toggle for Sarvam TTS. Think Genshin Impact story mode or Fate/Stay Night but AI-generative and Indian.

**Market validation:** Mythik raised $20M at a $50M valuation doing AI Indian mythology *videos* (passive content). Katha is the interactive layer nobody has built.

---

## Why This Exists (Career Context)

Builder: **Arrya Thakur**, 3rd year B.Tech CS at SRM Chennai (CGPA 8.5, graduating 2027). Building Katha to:
1. Fill gaps in his portfolio for GenAI/Applied AI Engineer roles (RAG, fine-tuning, multi-agent, voice AI)
2. Potentially grow into a real company if retention data is strong post-launch
3. Deploy on Play Store — real users, not a demo

Career folder is separate: `C:\Career` (resume, cold emails, job search). This folder is Katha only.

---

## Full Technical Architecture

### Stack
- **Frontend:** React Native + Expo (Arrya knows React)
- **Backend:** FastAPI (already his stack)
- **Agent Orchestration:** LangGraph 1.0
- **Primary LLM:** Gemini API (long context)
- **Fine-tune target:** LoRA on Llama 3.1 8B (Mahabharata dialogue corpus)
- **Vector DB:** ChromaDB (dev) → Pinecone (prod)
- **STT:** Sarvam AI Saarika (Hindi + Hinglish + English, 22 Indian languages)
- **TTS:** Sarvam AI Bulbul V3 (30+ Indian voices, character-specific profiles)
- **DB:** SQLite (dev) → PostgreSQL (prod)
- **Deployment:** Render (backend), Play Store (app)

### Folder Structure
```
C:\Katha\
├── HANDOFF.md                  ← this file
├── backend\
│   └── app\
│       ├── agents\             ← LangGraph nodes (narrator, karna, krishna, etc.)
│       ├── rag\                ← RAG pipeline (mythology, world state, memory)
│       ├── api\                ← FastAPI endpoints
│       ├── moderation\         ← 3-layer content moderation
│       ├── models.py           ← Pydantic schemas
│       ├── database.py         ← SQLAlchemy setup
│       └── main.py             ← FastAPI app entry
├── frontend\                   ← React Native + Expo app
├── data\
│   ├── raw\                    ← Ganguli translation (download from Internet Archive)
│   └── processed\             ← chunked + embedded chunks
├── assets\
│   ├── backgrounds\            ← scene art (Midjourney/Flux generated)
│   ├── characters\             ← NPC portraits × 3 expressions each
│   └── ui\                     ← borders, frames, UI elements
└── docs\                       ← numbered design suite (00–10); start at 05 (phasing)
```

---

## Core Technical Concepts

### 3-Layer RAG

**Layer 1 — Mythology RAG** (one-time setup)
- Source: Kisari Mohan Ganguli translation, full public domain text, download from archive.org
- Chunking: by speaker turn + scene context (NOT naive sentence splitting — legal/mythology text breaks across naive chunks)
- Metadata per chunk: parva_name, chapter, speaker, characters_present
- Purpose: NPC agents query this to stay grounded in source text

**Layer 2 — World State RAG** (runtime, per session)
- Every player action and story event vectorized and stored
- Each event has `known_to` field (array of NPC IDs who witnessed it)
- NPC agents only retrieve events they were present for — this creates authentic dramatic irony
- This is the information asymmetry system (Karna doesn't know he's Kunti's son until revealed)

**Layer 3 — Personal Memory RAG** (runtime, per NPC)
- After every conversation turn, summarize + vectorize + store per NPC
- When player talks to Karna again → retrieve top-5 relevant past memories
- Each NPC's memory is isolated from others

### LangGraph Multi-Agent System

```
Player Input → Narrator Agent (orchestrator)
                    ↓
        [Routes to active NPC agents]
                    ↓
    Karna / Krishna / Draupadi / Arjuna nodes (parallel)
                    ↓
        World State Updater
                    ↓
        Response Synthesizer → Output
```

**Narrator Agent:** Maintains story arc, decides which NPCs are active, generates scene descriptions, ensures pacing.

**NPC Agents:** Each has system prompt defining personality + speech patterns + current knowledge state + hard content rules. Never break character. Deflect inappropriate inputs IN CHARACTER (Karna: "That is not the way of a warrior").

### Database Schema (key tables)
- `players` — device_id, language, dharma_score, strike_count
- `sessions` — player_id, entry_point, current_scene, chapter
- `world_events` — description, embedding, known_to[], session_id
- `npc_memory` — npc_id, memory_text, embedding, session_id
- `relationships` — session_id, npc_id, trust_score (-100 to +100)
- `dharma_log` — choice_description, dharma_delta, npc_context
- `knowledge_states` — session_id, npc_id, known_event_ids[]

### Content Moderation (3 layers)
1. **Input Classifier:** Gemini safety filters + custom "religious figure disrespect" classifier before any agent sees the input
2. **In-Character Deflection:** NPC system prompts with graceful in-character refusal (maintains immersion, never breaks to "I'm an AI")
3. **Output Validator:** Check generated content before display; regenerate if flagged; serve pre-written fallback if still fails

**Strike system:** 1st flag = silent log + deflection, 2nd = soft warning, 3rd = session ends + 24hr cooldown

**Legal:** Terms of Service prohibiting religious disrespect, age gate (13+), grievance contact, no verbatim conversation storage (only vectorized summaries). **Note:** governing regime is now the Online Gaming Act 2025 / Rules 2026 + DPDP 2023 (Katha = permitted "online social game") — see [docs/08-legal-and-compliance.md](docs/08-legal-and-compliance.md).

---

## Story Entry Points

> **These are PHASE 2 (Mahabharata).** Phase 1 launches on Vikram aur Betaal — see
> [docs/06-phase1-vikram-betaal.md](docs/06-phase1-vikram-betaal.md). The entries below are the marquee arcs unlocked at graduation
> ([docs/05-phasing-roadmap.md](docs/05-phasing-roadmap.md)).

**Entry 1 — Night Before Kurukshetra (first Phase-2 arc)**
Player is in Pandava camp, night before the war. Walk through the camp speaking with each warrior. Arjuna's doubt, Bhima's rage, Yudhishthira's guilt, Krishna's resolve, Draupadi's silence. Each conversation changes relationships heading into war.

**Entry 2 — The Dice Game** (V1)
Play as Yudhishthira making the choice, or as Draupadi witnessing. Immediate moral stakes.

**Entry 3 — Karna at the Crossroads** (V1)
Witness Karna's choice when Indra takes his armor. Then Kunti arrives. Player choices affect whether Karna's identity surfaces in their version.

---

## NPC Profiles

**Karna:** Loyal to Duryodhana above all — the only man who gave him dignity. Deep personal honor code (never refuses a genuine request, never strikes from behind). Suppressed grief about low birth. Formal, measured speech. Calls player "traveler" until trust is earned. Addresses Arjuna as equal-but-enemy.

**Krishna:** Divine but present. Gentle humor that masks cosmic weight. Asks questions more than gives answers. Knows everything but reveals only what's necessary. Omniscient system prompt: he knows all knowledge states but acts within what he "chooses to reveal."

**Draupadi:** Fire, not tragedy. Fiercely intelligent. Does not suffer fools. Her humiliation at the dice game is the wound that drives everything — she will not let anyone forget. Speaks directly. Expects directness back.

**Arjuna:** Conflict made flesh — supreme warrior who questions whether to fight. Deeply loyal to Krishna but capable of doubt. Less formal than Karna, more emotionally accessible. Responds to questions about duty with vulnerability.

---

## Visual Direction

- **Format:** Visual novel — full-screen background art + character portrait + dialogue panel at bottom
- **Art style:** Semi-realistic painted, cinematic (NOT anime, not photorealistic). Amar Chitra Katha meets Kalki 2898 AD aesthetic.
- **Palette:** Deep indigo/navy backgrounds, amber/saffron character lighting, gold (#C9A84C) UI accents
- **Generate assets with:** Midjourney v7 or Flux.1 (prompt templates in docs/architecture.md once written)
- **Character portraits:** 3 expressions each (neutral, intense, emotional) — use ControlNet for consistency
- **Sound:** Ambient audio per scene (battlefield wind, temple bells, forest night) + Sarvam TTS voice per character

---

## MVP Build Order

> **Superseded by the milestone-based plan in [docs/09-build-plan.md](docs/09-build-plan.md).** Timeline is no longer
> a constraint (quality is), and the build is Phase-1-first. The 8-week table below is kept only
> as the original intent. The real plan: Engine spine → Vikram-Betaal data → first playable tale
> → moderation hardening → launch set → voice → VN frontend → soft launch → iterate to retention,
> with eval gates between each. Each milestone advances only when its exit criteria are met.

<details><summary>Original 8-week table (superseded)</summary>

| Week | Focus | Deliverable |
|------|-------|-------------|
| 1 | RAG Foundation | Mahabharata text chunked + indexed in ChromaDB, retrieval tested |
| 2 | Database + World State | PostgreSQL schema live, world event logging + knowledge state filtering working |
| 3 | NPC Agents | 4 NPC system prompts + personal memory RAG, each tested in isolation |
| 4 | Narrator + Full Graph | Complete LangGraph graph wired, end-to-end conversation tested |
| 5 | Content Moderation | All 3 layers live, adversarial testing done |
| 6 | FastAPI + Voice | All endpoints + Sarvam AI STT/TTS integrated |
| 7 | React Native Frontend | Scene backgrounds, character portraits, dialogue panel, animations |
| 8 | Polish + Play Store | Art assets generated, sound integrated, beta tested, submitted |

</details>

---

## Monetization (decide before launch)
- No ads (ruins immersion entirely)
- Model: **subscription ₹99/month** or **story packs ₹299 per arc**
- Recommendation: launch free for first story arc (Night Before Kurukshetra), charge for subsequent arcs

---

## Company Potential
If day-7 retention > 20% after launch: consider pre-seed raise (₹1-2 Cr from Indian angels is very achievable for this story). Expansion path: Mahabharata → Ramayana → regional epics → modern India settings. Global diaspora market (30M+ Indians abroad) is high-spend segment.

Comparable: Mythik (passive video) = $50M valuation. Interactive > passive historically.

Decision point: at 1,000 users with real retention data, choose between job offer (GenAI engineer) vs raise and go all-in.

---

## Key Contacts / Resources
- Sarvam AI API docs: docs.sarvam.ai
- Ganguli Mahabharata: archive.org/details/TheMahabharataOfKrishna-dwaipayanaVyasa
- LangGraph docs: langchain-ai.github.io/langgraph
- Arrya's GitHub: github.com/arrya5
- Career folder: C:\Career (resume.tex, cold emails — separate from this project)
