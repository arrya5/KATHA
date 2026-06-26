# Katha — Design Suite Index

This folder contains 15 deep-dive design documents written alongside the build. Each covers one vertical of the system in detail. Open only the one you need; [PROJECT.md](../PROJECT.md) is the master reference for day-to-day orientation.

| Doc | Title | What it covers |
|---|---|---|
| [`00-research-and-market.md`](00-research-and-market.md) | Research & Market Analysis | Competitive landscape (Mythik and others), market sizing, regulation (Online Gaming Act 2025, DPDP), and the investment thesis for interactive vs. passive Indian mythology |
| [`01-architecture.md`](01-architecture.md) | Technical Architecture | The 6-node turn graph, 3-layer RAG design, knowledge-state engine schema, provider-swappable LLM interface, cost and latency targets |
| [`02-data-pipeline.md`](02-data-pipeline.md) | Data Pipeline | Source-text sourcing strategy (Ganguli/BORI translations), chunking and embedding pipeline, provenance tracking — primarily a Phase 2 concern |
| [`03-npc-prompts.md`](03-npc-prompts.md) | NPC Character Bibles | Phase 2 character bibles: Karna, Krishna, Draupadi, and others — voice, knowledge boundaries, and dharma stance |
| [`04-cultural-fidelity.md`](04-cultural-fidelity.md) | Cultural Fidelity & Authenticity Framework | The reverence rules, Sacred/Sensitive/Neutral tier classification, advisory board structure, and the non-negotiable principles that govern every output |
| [`05-phasing-roadmap.md`](05-phasing-roadmap.md) | Phasing Roadmap | Why Phase 1 (Vikram aur Betaal) ships first, the Phase 2 (Mahabharata) graduation checklist, and the content-agnostic engine design that bridges them |
| [`06-phase1-vikram-betaal.md`](06-phase1-vikram-betaal.md) | Phase 1 — Vikram aur Betaal | The current product: world-building, gameplay loop, Betaal and Vikramaditya character design, riddle-and-moral structure |
| [`07-moderation-and-safety.md`](07-moderation-and-safety.md) | Moderation & Safety | The 3-layer defense-in-depth system (input classifier → output validator → authored fallback), threat model, red-team methodology, and eval results |
| [`08-legal-and-compliance.md`](08-legal-and-compliance.md) | Legal & Compliance | Online Gaming Act 2025 / Rules 2026, DPDP Act requirements, terms of service obligations, and the compliance checklist for launch |
| [`09-build-plan.md`](09-build-plan.md) | Build Plan | Milestone-by-milestone plan (M0–M4 done; M5 voice, M6 art, M7 launch), acceptance criteria, and dependency map |
| [`10-business-and-pitch.md`](10-business-and-pitch.md) | Business & Pitch | Monetization model, unit economics, the funding path, and pitch narrative |
| [`11-phase1-content-tales-and-betaal.md`](11-phase1-content-tales-and-betaal.md) | Phase 1 Content — Tales & Betaal | Betaal's system prompt and the Tale 1 worked example with dialogue, world-state writes, and branching logic |
| [`12-resume-mapping.md`](12-resume-mapping.md) | Resume Mapping | Skill-to-proof-to-resume-bullet mapping — each engineering decision linked to a concrete artefact for portfolio or job applications |
| [`13-phase1-tales-2-4-and-meta-arc.md`](13-phase1-tales-2-4-and-meta-arc.md) | Phase 1 Content — Tales 2–5 & Meta-arc | Tales 2 through 5, the Prologue, and the conspiracy meta-arc that ties the full story arc together |
| [`14-art-direction-and-prompts.md`](14-art-direction-and-prompts.md) | Art Direction & Prompts | Visual art direction (style, palette, character and scene guidelines), copy-paste image-generation prompts, and the asset specification |

---

Technical blog: [`blog/leak-proof-agents.md`](blog/leak-proof-agents.md) — deep-dive writeup on the witness-gate mechanism and how to make multi-agent information asymmetry structurally leak-proof.

Media assets (demo GIF, screenshots): [`assets/README.md`](assets/README.md)
