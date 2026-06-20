# Katha — Build Plan (Milestone-Based)

> Replaces the fixed 8-week table in [HANDOFF.md](../HANDOFF.md). Timeline is explicitly **not** a
> constraint — quality is. So this plan is **milestone- and quality-gate-based**, not
> calendar-based: each milestone ends with concrete exit criteria, and you do not advance until
> they're met. Phase-1-first ([05-phasing-roadmap.md](05-phasing-roadmap.md)).
>
> **Progress (detail in [PROJECT.md](../PROJECT.md)):** Milestones **0–4 are DONE** — engine spine,
> Vikram-Betaal data/agents, playable tales, moderation hardening, and content breadth (Prologue
> + 5 tales + trust-gated climax) — **plus** SQLite persistence and a real LangGraph orchestrator
> (ahead of plan). **Remaining:** M5 voice (Sarvam), M6 art + Expo polish, M7 launch, M8 retention.
> Note: the doc-02 *text-ingestion* pipeline (chunking the full Baital Pachisi) is not yet run —
> current canon is hand-authored tale facts, which is sufficient for the MVP.

---

## 0. Sequencing philosophy
- **Engine before content.** Build the content-agnostic spine first; then pour Vikram aur Betaal
  into it; then (after graduation) the Mahabharata.
- **Vertical slice early.** Get *one* tale playable end-to-end (text → agent → choice → memory)
  before breadth. A thin full loop beats a deep half-loop.
- **Evals are gates, not chores.** The leak/fidelity/false-positive evals ([02](02-data-pipeline.md) §6,
  [07](07-moderation-and-safety.md) §4) decide whether a milestone is "done."
- **Voice & art are polish layers** over a working text loop — not prerequisites for proving the engine.

---

## Milestone 0 — Engine spine (content-agnostic)
**Goal:** the LangGraph turn graph runs end-to-end on a *toy* scene.
- LangGraph graph wired: Input-Moderation → Narrator → NPC node(s) → World-State Updater →
  Output-Validator → Synthesizer, with checkpointing ([01-architecture.md](01-architecture.md) §2).
- `TurnState` schema; Postgres/SQLite schema ([01-architecture.md](01-architecture.md) §5); vector DB (ChromaDB) up.
- 3-layer RAG plumbed with placeholder content; **knowledge-state engine** enforcing the
  `known_to` filter ([01-architecture.md](01-architecture.md) §4).
- Provider-swappable LLM interface.
- **Exit criteria:** a scripted turn flows through every node; a placeholder NPC cannot retrieve
  an event it didn't witness (first **leak test** passes); turn trace/observability working.

## Milestone 1 — Data & retrieval (Vikram aur Betaal corpus)
**Goal:** Betaal can be grounded in real source text.
- Ingest public-domain *Baital Pachisi* (Forbes/Burton/Tawney) via the doc-02 pipeline; chunk by
  dramatic unit; metadata enriched ([02-data-pipeline.md](02-data-pipeline.md), [06-phase1-vikram-betaal.md](06-phase1-vikram-betaal.md) §2).
- Embeddings + hybrid retrieval; **retrieval eval set** built and passing target recall@k.
- **Exit criteria:** retrieval returns the right tale/chunk for a hand-built eval set; corpus
  versioned.

## Milestone 2 — First playable tale (vertical slice)
**Goal:** one complete tale, text-only, end to end.
- **Betaal agent** authored ([06-phase1-vikram-betaal.md](06-phase1-vikram-betaal.md) §5): voice, trust ladder, discretion,
  deflection bank. Narrator paces tale → riddle → reaction.
- One tale fully authored, incl. its mini-agents and the **moral-riddle/dharma choice**; choice
  updates the **dharma/wisdom profile** and **Betaal's memory of you** (L3).
- **Exit criteria:** a player can play the tale, make the judgment, and on a *second* tale Betaal
  references the first (memory works); canon-consistency + leak evals pass.

## Milestone 3 — Moderation & safety hardening
**Goal:** safe under abuse, before any external eyes.
- All 3 layers live ([07-moderation-and-safety.md](07-moderation-and-safety.md)); strike system; deflection bank; output
  validator + fallbacks.
- Red-team suite + **false-positive eval**; jailbreak/prompt-injection tests.
- **Exit criteria:** red-team, leak, and false-positive suites pass target thresholds; worst
  outputs are reverent/boring, not shareable.

## Milestone 4 — Content breadth (the launch set)
**Goal:** a tight, high-quality launch arc.
- Author **3–5 sharp tales** + the conspiracy meta-arc beats ([06-phase1-vikram-betaal.md](06-phase1-vikram-betaal.md) §7); each
  advisor-spot-checked for tone.
- Lean-in investigation path (talk to tale characters) working for each tale.
- **Exit criteria:** launch set fully playable, evals green per tale, meta-arc climax in place.

## Milestone 5 — Voice (Sarvam)
**Goal:** voice-first, the showcase modality.
- Saarika STT (Hindi/Hinglish/English) on input; Bulbul v3 TTS with **per-character voice
  profiles** ([01-architecture.md](01-architecture.md) §6); streaming + TTS caching.
- **Exit criteria:** Betaal *sounds* like Betaal; latency within budget ([01-architecture.md](01-architecture.md) §7.2);
  voice toggle degrades gracefully to text.

## Milestone 6 — Frontend / visual novel
**Goal:** the cinematic VN client.
- React Native + Expo: scene backgrounds, Betaal portrait (3 expressions), dialogue panel with
  typewriter, choice UI, voice toggle, dharma/wisdom profile screen.
- Art pipeline: cremation-ground + per-tale backgrounds, Betaal portrait set ([HANDOFF.md](../HANDOFF.md) visual
  direction); ambient soundscapes.
- **Exit criteria:** the launch set is playable as a polished VN on a device; art/tone reviewed.

## Milestone 7 — Soft launch & instrumentation
**Goal:** real users, real retention data.
- FastAPI endpoints hardened; Render deploy; analytics (retention, turns/session, voice usage,
  fallback/deflection rates — [01-architecture.md](01-architecture.md) §9); cost dashboard.
- Legal docs shipped ([08-legal-and-compliance.md](08-legal-and-compliance.md) §6 Phase-1 checklist).
- Closed beta → soft launch on Play Store.
- **Exit criteria:** stable under real traffic; day-1/7 retention measured; unit-cost per session known.

## Milestone 8 — Iterate to retention target
**Goal:** earn the right to scale (and to Phase 2).
- Tune tales, Betaal, pacing, monetization against real funnel data ([10-business-and-pitch.md](10-business-and-pitch.md)).
- Decide LoRA fine-tune trigger ([01-architecture.md](01-architecture.md) §7.1) if NPC-gen cost/voice-consistency demands.
- **Exit criteria:** a retention curve worth investing behind; Phase-2 **graduation criteria**
  ([05-phasing-roadmap.md](05-phasing-roadmap.md) §4) being actively checked off.

---

## Phase 2 milestones (held until graduation)
9. Mahabharata corpus (Ganguli) via the same pipeline → 10. Karna/Krishna/Draupadi/Arjuna agents
+ Cultural Advisory sign-off → 11. "Night Before Kurukshetra" arc → 12. Heightened moderation +
incident-response rehearsal → 13. Phase-2 launch. (Designs already in docs 02–04.)

---

## Always-on workstreams (parallel to all milestones)
- **Evals & red-team** maintained and run in CI (the real definition of "done").
- **Cultural review** — light-touch in Phase 1; board engaged *during* Phase 1 to be ready for Phase 2.
- **Cost/latency budget** tracked per milestone, not discovered at the bill.
- **Observability** — every turn traceable.

---

## Critical-path risks & mitigations
| Risk | Mitigation |
|---|---|
| Knowledge-state correctness is subtly wrong | Leak eval from Milestone 0; it's a gate, not a finale |
| Betaal's voice feels generic | Voice-consistency eval; author deflection bank early; LoRA only if needed |
| Scope creep (chasing all 25 tales) | Launch on 3–5 great tales; breadth is post-retention |
| Cost per turn too high | Tiered models + caching + async from day one ([01-architecture.md](01-architecture.md) §7) |
| Art bottleneck stalls everything | Text loop proves the engine without art; art is a parallel polish layer |
