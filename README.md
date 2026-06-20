# Katha 📖✨

> **AI-Powered Interactive Visual Novels in Indian Mythology**
> 
> *Live inside the epic, instead of just reading it.*

---

## 1. The Vision

**Katha** is a voice-first, AI-powered interactive visual novel engine designed for Android. 

### Core IP: The Information-Asymmetry Engine
In Katha, every character is an independent AI agent with persistent memory and an **isolated knowledge state**. An agent only knows what they have witnessed, heard, or were told directly. This structural information-asymmetry drives gameplay: you must investigate, build trust, and query NPCs who hold different pieces of the puzzle.

### Release Phasing
1. **Phase 1: Vikram aur Betaal** (Current Focus)
   - A low-risk folklore setting that serves as the perfect tutorial. The riddle-and-moral structure of the Baital Pachisi is mapped directly into gameplay loops.
2. **Phase 2: Mahabharata** (Marquee Arc)
   - A massive branching narrative unlocked after Phase 1 matures, ensuring high cultural fidelity and refined moderation before handling major sacred narratives.

---

## 2. Directory Structure

This repository is structured for modularity and clean separation between backend and frontend.

```
Katha/
├── backend/            # Python core engine & API
│   ├── app/            # LangGraph orchestrator, RAG, and endpoints
│   └── tests/          # Robust test coverage (leak-testing, simulation)
├── frontend/           # Expo (React Native) Android/iOS app
│   ├── App.tsx         # Mobile entry point
│   └── src/            # Theme, screens, components, and API integration
├── docs/               # 15 deep-dive design documents (00 to 14)
├── data/               # Raw sources (provenance) & evaluation gates
└── assets/             # Drop-in slots for background & character art
```

---

## 3. Quick Start

You can run Katha completely free and offline with zero local setup besides Python, or spin up the full mobile Expo stack.

### Option A: The Zero-Dependency Terminal & Web Play (Recommended First)
Play the game immediately in your terminal or browser with **no installations** and **no API keys**.

```bash
cd backend

# 1. Run the self-test (33 checks verifying the knowledge-state isolation)
python -m app.selftest

# 2. Play the full story arc inside your terminal
python -m app.demo

# 3. Play the interactive visual novel in your browser (HTTP client)
python -m app.webserver
# ▶ Open http://127.0.0.1:8000 in your browser
```

### Option B: The Mobile App (Expo Go)
Run the React Native Expo app on your phone.

```bash
# 1. Start the backend server (FastAPI/stdlib webserver)
cd backend
python -m app.webserver

# 2. Start the Expo packager
cd ../frontend
npm install
npm start
# ▶ Scan the QR code using the Expo Go app on your physical device
```
*Note: Make sure your phone and computer are on the same Wi-Fi network. The Expo configuration will auto-detect your computer's LAN IP and link up with the backend.*

---

## 4. Configuration & Env Switches

The backend is fully swappable and offline-first by default. To unlock advanced features, copy `backend/.env.example` to `backend/.env` and set the following:

| Env Variable | Default | Options | What it does |
|---|---|---|---|
| `KATHA_LLM_PROVIDER` | `mock` | `ollama`, `gemini` | Switches from scripted lines to real LLM-improvisation. |
| `KATHA_EMBEDDINGS` | `lexical` | `ollama` | Enables local semantic query search (requires `nomic-embed-text`). |
| `KATHA_ORCHESTRATOR` | `simple` | `langgraph` | Swaps the stdlib runner for production LangGraph orchestrator. |
| `DATABASE_URL` | (in-memory) | `sqlite:///katha.db` | Persists session, trust, flags, and player progress. |
| `SARVAM_API_KEY` | (unset) | Your API Key | Enables high-quality Indian TTS voices via Sarvam AI. |
| `GEMINI_API_KEY` | (unset) | Your API Key | Enables production-grade LLM generation. |

---

## 5. Guide to Deep-Dive Docs

The `docs/` folder contains comprehensive documentation from regulatory compliance to prompt engineering.

* **Architecture**: [`01-architecture.md`](docs/01-architecture.md) — Multi-agent state machine, 3-layer RAG.
* **Cultural Fidelity**: [`04-cultural-fidelity.md`](docs/04-cultural-fidelity.md) — Sensitivity protocols, advisory board framework.
* **Roadmap & Plan**: [`05-phasing-roadmap.md`](docs/05-phasing-roadmap.md) & [`09-build-plan.md`](docs/09-build-plan.md) — The milestone phases.
* **Character Bibles**: [`03-npc-prompts.md`](docs/03-npc-prompts.md) & [`11-phase1-content-tales-and-betaal.md`](docs/11-phase1-content-tales-and-betaal.md).
* **Legal & Compliance**: [`08-legal-and-compliance.md`](docs/08-legal-and-compliance.md) — Online Gaming Act 2025 and DPDP compliance.
* **Art Direction**: [`14-art-direction-and-prompts.md`](docs/14-art-direction-and-prompts.md) — Prompt guidelines for visual styles.

---

## 6. Collaboration Guidelines for the Team

Welcome to the team! Here is how we keep the codebase clean and solid:

1. **Keep the Self-Test Green**: Always run `python -m app.selftest` before pushing any changes. It guarantees the core game engine, state validation, and RAG leakage protection are functional.
2. **Branching Strategy**: 
   - Work on feature branches (`feature/your-feature-name`).
   - Open a Pull Request (PR) to `main` for code reviews.
3. **No Hardcoded Secrets**: Never check in keys or `.env` files. Access secrets exclusively via `backend/app/config.py`.
4. **Offline Fallback Guarantee**: Any external service failure (LLM provider down, voice provider down, vector store error) must catch exceptions gracefully and fall back to the offline mock/lexical versions so the game remains fully playable.
