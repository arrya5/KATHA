# Katha — Résumé / Portfolio Mapping

> Katha's first purpose (HANDOFF "Why This Exists"): fill the gaps in Arrya's résumé for
> **GenAI / Applied AI Engineer** roles with a real, shipped system — RAG, multi-agent,
> fine-tuning, voice AI. This doc tracks **skill → proof in the repo → milestone → résumé
> bullet**, and marks what's *earned now* vs *pending build*, so a bullet is only claimed once
> the code backs it. Career files stay in `C:\Career`; this is the mapping, not the résumé.

Legend: ✅ earned (code exists & runs) · 🟡 partial (scaffold/stub) · ⬜ pending build.

---

## 1. Skill coverage

| Target skill | Status | Proof in this repo | Milestone |
|---|---|---|---|
| **Multi-agent orchestration (LangGraph)** | ✅ | `app/agents/langgraph_graph.py` — real **LangGraph 1.x `StateGraph`** (typed state, named nodes, conditional moderation edge) as the production orchestrator; stdlib runner as zero-install fallback. Full arc verified under both. | M0/M2 ([09](09-build-plan.md)) |
| **Advanced RAG** | ✅ | `app/rag/` — 3-layer retrieval + the **knowledge-state engine** (witnessed-canon + `known_to` filters); provider-agnostic vector store | M1 |
| **Semantic retrieval / embeddings** | ✅ | `app/rag/embeddings.py` — real embeddings (Ollama, free local) + cosine vector store, lexical fallback; verified meaning-based retrieval | M1 |
| **Novel system design (the differentiator)** | ✅ | Information-asymmetry / knowledge-state engine; proven by passing leak tests (incl. prompt-level: a real model never *sees* unwitnessed facts) | M0–M2 |
| **LLM safety / guardrails / red-teaming** | ✅ | `app/moderation/` 3-layer defense; jailbreak/break-character deflection; eval sets **12/12 red-team caught + 12/12 benign allowed** | M3 |
| **Eval-driven development** | ✅ | `app/selftest.py` (**33 checks**), `tests/test_engine.py`, `data/processed/eval/*.jsonl` | always-on |
| **Prompt engineering** | ✅ | `app/content/betaal_prompt.py` + dynamic context assembly that resists injection | M2 |
| **Provider-swappable LLM integration** | ✅ | `app/llm/` interface + `MockProvider` + **`OllamaProvider` (real local generation, verified live)** + `GeminiProvider` stub | M2 |
| **Persistence / state management** | ✅ | `app/persist.py` — SQLite session store; progress survives restarts (verified across two processes) | M2/M7 |
| **Backend / API engineering** | ✅ | `app/api.py` (FastAPI: `/turn`, `/season`, CORS, graceful errors) + `app/webserver.py` (stdlib, zero-install demo) | M7 |
| **Voice AI (TTS / STT)** | 🟡 | **TTS built**: browser speech (free) + Sarvam Bulbul provider + `/tts` + per-character voice profiles (key-gated). STT (Saarika) pending. | M5 |
| **Fine-tuning (LoRA)** | ⬜ | LoRA-on-Llama plan + breakeven trigger ([01](01-architecture.md) §7.1) | M8 |
| **Cost/latency optimization** | 🟡 | budget + levers designed ([01](01-architecture.md) §7); caching/tiering to implement | M7/M8 |
| **Mobile (React Native/Expo)** | ⬜ | `frontend/` (VN client) | M6 |
| **Shipped to production / Play Store** | ⬜ | deploy + soft launch | M7/M8 |

You already have **✅ on the four hardest-to-fake bullets** (multi-agent, advanced RAG, a
genuinely novel mechanism, and safety/evals) after Milestone 0–2 — that's the spine of a strong
Applied-AI profile. Voice and fine-tuning are the remaining marquee adds.

---

## 2. Draft résumé bullets (drop into `C:\Career\resume.tex`, tune later)

**Earned now (✅) — backed by running code in this repo:**
- Built a **multi-agent narrative engine with LangGraph** (a `StateGraph` of narrator-router +
  character agents + moderation/validation nodes over a typed turn-state, with conditional routing)
  for an AI interactive visual novel grounded in Indian folklore.
- Designed a **knowledge-state RAG system** giving each AI character an *isolated, witnessed-only*
  view of world state — provably preventing information leakage (100% pass on automated
  leak-tests), creating authentic dramatic irony.
- Implemented a **3-layer RAG** pipeline (curated public-domain canon + per-session world events
  + per-agent memory) with **real semantic embeddings** (cosine retrieval) and a lexical fallback.
- Built a **3-layer content-moderation/guardrail stack** (input classifier, in-character
  deflection, output validator) hardened against jailbreaks and break-character attacks —
  **12/12 red-team attacks caught, 12/12 benign inputs allowed**.
- Practiced **eval-driven development**: 33 automated checks incl. structural leak tests,
  canon-consistency, and red-team/false-positive eval sets run as CI gates.
- Engineered a **provider-swappable LLM abstraction** (offline mock + **real local Ollama** +
  Gemini), so the system runs and is fully testable with no API keys.
- Added **SQLite persistence** so player progress (trust, memory, dharma, scene) survives
  restarts; designed for a clean swap to Postgres.

**Pending build (claim once shipped):**
- Integrated **Sarvam AI STT/TTS** for voice-first play in Hindi/English with per-character voice
  profiles. *(M5)*
- **Fine-tuned Llama 3.1 8B (LoRA)** on a character-dialogue corpus to improve voice consistency
  and cut per-turn inference cost. *(M8)*
- Shipped a **React Native (Expo)** visual-novel client and deployed the FastAPI backend; soft-
  launched on the Play Store with retention instrumentation. *(M6–M8)*

> Quantify before sending: turns/session, retrieval recall@k, leak-test pass rate, latency,
> cost/turn, retention. Real numbers beat adjectives ([10](10-business-and-pitch.md) §4).

---

## 3. How to talk about it (interview framing)
- **Lead with the novel bit:** the knowledge-state / information-asymmetry engine. It's the part
  most candidates can't claim and it shows systems thinking, not just API-calling.
- **Show the evals.** "I treat leak-prevention as a structural guarantee with automated tests" is
  a senior-sounding sentence for a new grad.
- **The phasing story** ([05](05-phasing-roadmap.md)) demonstrates product judgment and risk management — rare and valued.

---

## 4. Keep this current
Update the Status column as milestones land ([09](09-build-plan.md)). When a ⬜ becomes ✅, move its bullet
from "pending" to "earned" and add the metric.
