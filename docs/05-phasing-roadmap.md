# Katha — Phasing Roadmap & Launch Strategy

> **Read this right after [HANDOFF.md](../HANDOFF.md).** It defines the single most important strategic
> decision in the project: *what Katha launches with, and in what order.*
>
> Decision date: 2026-06-15.

---

## 1. The decision

**Katha does not launch on the Mahabharata.** It launches on **Vikram aur Betaal**
(the *Baital Pachisi* / *Vetala Panchavimshati*), and graduates to the Mahabharata as a
later, marquee arc once the engine, audience, craft, and cultural-review process are proven.

| | **Phase 1 — Vikram aur Betaal** | **Phase 2 — Mahabharata** |
|---|---|---|
| Material | Folk frame-tales (legend) | Sacred epic (worshipped figures) |
| Backlash risk | **Low** | **High** (the central risk — [04-cultural-fidelity.md](04-cultural-fidelity.md)) |
| Role | Prove the engine + build audience + craft + ops | The "earned," premium, mature arc |
| Status | **Build first** | Designed (docs 02–04), held until graduation |

---

## 2. Why this is the right call

1. **It removes the make-or-break risk from launch.** The #1 threat to Katha is religious
   sensitivity ([00-research-and-market.md](00-research-and-market.md) §4): a single bad line attributed to a deity can end
   the project. Vikramaditya is a *legendary king*, not a worshipped god — the "sacred tier"
   ([04-cultural-fidelity.md](04-cultural-fidelity.md) §2) is nearly empty in Phase 1.
2. **Nothing is wasted.** Katha's actual invention is the *engine* — the LangGraph graph, the
   3-layer RAG, the knowledge-state/asymmetry system, moderation, voice, VN presentation
   ([01-architecture.md](01-architecture.md)). It is **content-agnostic**. Phase 1 instantiates it on safe content;
   Phase 2 swaps the content in. Docs 02/03/04 (Mahabharata sourcing, character bibles,
   fidelity rules) become Phase-2 assets, ready to deploy.
3. **The structure fits the engine perfectly.** *Baital Pachisi* is literally a moral-dilemma
   loop: each tale ends in a judgment the king must make. That *is* Katha's dharma/choice
   system — gameplay, not bolted on. See [06-phase1-vikram-betaal.md](06-phase1-vikram-betaal.md).
4. **It de-risks the pitch.** "We sequenced into the sacred material deliberately, after
   proving retention and assembling a cultural advisory board" is a stronger investor story
   than "we bet everything on not offending anyone on day one."
5. **It builds the moral muscle for Phase 2.** Players (and the system) practice exactly the
   kind of dharma judgment the Mahabharata is about — a thematic bridge, not a detour.

---

## 3. What transfers vs. what's Phase-specific

| Doc / asset | Transfers as-is | Phase-specific |
|---|---|---|
| [01-architecture.md](01-architecture.md) — engine, graph, 3-layer RAG, knowledge-state | ✅ entirely | — |
| [02-data-pipeline.md](02-data-pipeline.md) — chunking/embedding/eval pipeline | ✅ the *method* | Mahabharata sourcing = Phase 2; Phase-1 sourcing in doc 06 |
| [03-npc-prompts.md](03-npc-prompts.md) — prompt-assembly model + narrator | ✅ the *framework* | Karna/Krishna/Draupadi/Arjuna bibles = Phase 2; Betaal/Vikramaditya = doc 06 |
| [04-cultural-fidelity.md](04-cultural-fidelity.md) — tiers, never-rules, advisory | ✅ the *framework* (lighter intensity in P1) | Sacred-tier rules fully activate in Phase 2 |
| 07 moderation, 08 legal, 09 build, 10 business | ✅ Phase-1-first, Phase-2-aware | — |

So docs 02–04 are not "rewritten" for Phase 1 — they are the **Phase-2 playbook**, already
done. Phase 1 reuses their *methods* on safe content (doc 06).

---

## 4. Graduation criteria — when does Phase 2 (Mahabharata) unlock?

Phase 2 begins only when **all** of these are true. This list is the contract that keeps the
sacred arc from shipping before Katha has earned it.

**Product & engagement**
- [ ] A live Phase-1 product with real users and a credible retention curve (target: day-7 retention healthy enough to justify investment — define the number with real data, see [10-business-and-pitch.md](10-business-and-pitch.md)).
- [ ] Voice + visual-novel craft at a quality bar we're proud to show publicly.

**Engine reliability (the safety-critical guarantees)**
- [ ] Knowledge-leak eval passing ~100% in production ([02-data-pipeline.md](02-data-pipeline.md) §6).
- [ ] Canon-consistency + fidelity evals passing at target ([04-cultural-fidelity.md](04-cultural-fidelity.md)).
- [ ] Output validator + curated fallbacks proven against adversarial users in the wild ([07-moderation-and-safety.md](07-moderation-and-safety.md)).
- [ ] Low fallback/hallucination rate under real traffic.

**Cultural & legal readiness**
- [ ] **Cultural Advisory Board engaged and signed off** on the Mahabharata canon spine, character bibles, Krishna's discretion clause, and the deflection bank ([04-cultural-fidelity.md](04-cultural-fidelity.md) §4).
- [ ] Public Fidelity Statement published and tested ([04-cultural-fidelity.md](04-cultural-fidelity.md) §8).
- [ ] Legal review against the Online Gaming Act 2025 / Rules 2026 and DPDP ([08-legal-and-compliance.md](08-legal-and-compliance.md)).
- [ ] A rapid takedown/patch path for any flagged line, tested.

**Organizational**
- [ ] Enough operational maturity (monitoring, on-call, comms plan) to respond to a controversy within hours, not days.

Until every box is checked, Phase 2 stays in the vault.

---

## 5. The bridge: how Phase 1 leads into Phase 2

- **Thematic:** both are about *dharma* and hard moral judgment. Phase-1 players arrive at
  Phase 2 already fluent in the choice system.
- **Narrative bridge (optional):** late Phase-1 arcs can let Betaal tell a tale drawn from the
  *periphery* of the epic (a minor, non-sacred episode) to test audience appetite and tone
  before committing to the core.
- **Trust transfer:** a beloved, reverent Phase-1 product earns the benefit of the doubt that a
  cold Mahabharata launch never would.
- **Same characters of craft:** voice profiles, art pipeline, dharma scoring, memory — all
  carry forward.

---

## 6. Roadmap at a glance

```
Phase 0  Engine spine        → LangGraph graph + 3-layer RAG + knowledge-state, content-agnostic
Phase 1  Vikram aur Betaal   → first playable arc(s), voice + VN, soft launch, retention data
            │  (prove engine, build audience, assemble advisory board, harden moderation)
            ▼  [graduation criteria §4 met]
Phase 2  Mahabharata         → marquee arc: Night Before Kurukshetra, then Dice Game, Karna's Crossroads
Phase 3+ Expansion           → Ramayana, regional epics, history (Chanakya), original worlds
```

Detailed milestones (engine → Phase 1 → graduation) are in [09-build-plan.md](09-build-plan.md).

---

## 7. Open decisions
1. **How many Phase-1 tales before soft launch** — recommend a tight, fully-authored,
   advisor-spot-checked set (3–5 tales) over a thin 25. Quality gate, not volume. (doc 06/09)
2. **Whether to A/B the epic-periphery bridge tale** in late Phase 1 before committing to Phase 2.
3. **Naming** — is "Katha" the umbrella brand across phases, with Vikram aur Betaal as the first
   "season/book"? (Recommended: yes — Katha = the platform; each epic is a Book.)
