# Katha — Business Model & Pitch

> Companion to [00-research-and-market.md](00-research-and-market.md) (market evidence) and [05-phasing-roadmap.md](05-phasing-roadmap.md)
> (the de-risking story investors will like). Numbers here are **frameworks to fill with real
> data**, not claims — never pitch a fabricated metric. Build bottom-up from Katha's own funnel.

---

## 1. The narrative (how to tell the story)

> **Mythik raised ~$20M proving people want AI-generated Indian mythology — as passive video.
> Katha builds the interactive layer: a voice-first visual novel where every character is a
> living AI agent who remembers you and only knows what they witnessed. We launch on
> low-risk folklore (Vikram aur Betaal) to prove the engine and earn an audience, then bring
> the Mahabharata as the marquee arc. Interactive has always out-valued passive — and nobody
> has built it for India's epics.**

Three beats investors remember:
1. **Proven appetite** — Mythik ([00-research-and-market.md](00-research-and-market.md) §2.1) de-risks "is this a market?"
2. **A real wedge** — persistent-memory AI characters + *knowledge asymmetry* is the 2026-hot
   capability ([00-research-and-market.md](00-research-and-market.md) §3.1), taken further than anyone.
3. **Disciplined de-risking** — we sequence into the sacred material instead of betting the
   company on day-one offense ([05-phasing-roadmap.md](05-phasing-roadmap.md)). Maturity, not recklessness.

---

## 2. Monetization

- **No ads** — they destroy immersion (and risk the kid-data line under DPDP).
- **No real-money mechanics** — keeps Katha in the permitted "online social game" lane
  ([08-legal-and-compliance.md](08-legal-and-compliance.md) §1.1). This is a hard design rule, not a preference.
- **Free first** — the first tales (Phase 1) / first arc are free: maximize top-of-funnel and,
  crucially, **retention data** — the asset that unlocks fundraising.
- **Then paid, two candidate models (test both):**
  - **Story packs** — buy an arc/"Book" (e.g. ₹X per arc). Aligns price with delivered content;
    good for a story product.
  - **Subscription** — monthly (e.g. ₹99) for all content + new tales. Better LTV if cadence is high.
- **Recommendation:** launch free → introduce **story packs** first (lower commitment for a new
  brand) → layer subscription once there's a content cadence worth subscribing to.
- **Diaspora premium tier** later — the 30M+ Indians abroad are a high-ARPU segment ([00](00-research-and-market.md) §7 / HANDOFF).

---

## 3. Unit economics (the framework to fill in)

Build this bottom-up once models are chosen ([01-architecture.md](01-architecture.md) §7):

```
cost/session   = avg turns/session × cost/turn         (LLM + embeddings + vector + STT/TTS)
ARPU           = paid-conversion % × price (pack/sub)
contribution   = ARPU − cost/session − payment/store fees
LoRA breakeven = volume where self-hosted NPC-gen < API NPC-gen  → collapses dominant cost
```

- **Cost levers already designed in:** tiered models, aggressive caching (TTS per line-hash,
  canon per scene), async non-blocking work, optional LoRA at volume ([01-architecture.md](01-architecture.md) §7.1).
- **Sarvam economics help:** STT ≈ ₹30/hr, TTS ≈ ₹15–30/10K chars — 2–3× cheaper than global
  ([00-research-and-market.md](00-research-and-market.md) §6).
- **Target:** know cost/session before scaling spend; show a path to healthy contribution margin.

---

## 4. Metrics that matter (and that you'll be asked for)
- **Retention:** day-1 / day-7 / day-30. **Day-7 is the headline.** A credible D7 curve is the
  single most persuasive asset — more than any TAM slide.
- **Engagement:** turns/session, session length, tales completed, % using voice.
- **Monetization:** free→paid conversion, ARPU, LTV, payback.
- **Quality/trust:** fallback rate, deflection rate, leak-eval pass — proof the engine is safe
  to scale (and to take to Phase 2).
- **The asymmetry demo metric:** % of players who notice/comment that Betaal "remembers" them —
  a leading indicator of the magic working.

---

## 5. Market sizing (do it honestly)
- **Bottom-up first:** reachable Indian + diaspora story-game players × realistic paid
  conversion × price → SOM. This is what a good investor trusts.
- **Top-down as ceiling only:** visual-novel ~$9.4B→$21.8B; interactive fiction ~$4.3B→$7.8B;
  India = ~20% of global gamers; ~82% want mythology games ([00-research-and-market.md](00-research-and-market.md) §2.2). Cite as
  context, not as your number.
- **Comp:** Mythik at ~$50M valuation on *passive* video; interactive historically out-values passive.

---

## 6. Competition & moat (the slide they'll push on)
- **Direct:** none at the intersection (Indian epic canon × memory+asymmetry AI agents ×
  voice-first VN) — [00-research-and-market.md](00-research-and-market.md) §3.
- **Adjacent:** Character.AI (chat, no world/canon), Hidden Door (Western IP, text), Mythik
  (passive video). Each misses a different axis.
- **Moat = the hard, compounding things:**
  1. **Cultural credibility & process** — advisory board, fidelity track record, the willingness
     and ability to do sacred material *respectfully*. The reason others don't ship.
  2. **The knowledge-asymmetry engine** — genuinely hard to build correctly (leak-proof).
  3. **A curated, grounded canon + authored content** — not generic open-ended RP.
  4. **Voice-first in Indian languages** — Sarvam-grade localization most won't match.
  5. **Phase sequencing as IP** — a repeatable "epic → interactive arc" playbook (Mahabharata →
     Ramayana → regional → history → original worlds).

---

## 7. Funding path (for a student founder in Chennai)
- **Sequence:** ship Phase 1 → real D7 retention → *then* raise. A working, reverent, retentive
  product beats a deck ([00-research-and-market.md](00-research-and-market.md) §7).
- **Non-dilutive first:** **Startup India Seed Fund Scheme (SISFS)**, university/SRM incubation,
  relevant grants — extend runway without giving away equity early.
- **Angels/seed:** Indian Angel Network, LetsVenture, Mumbai Angels, **Chennai Angels** (local),
  plus gaming-active angels (e.g. Anupam Mittal; several Mythik backers). Gaming funding in India
  is **+73.8% YoY in 2026** — a favorable window.
- **Incubators/accelerators:** target ones with gaming/consumer/AI focus and Indian-market reach.
- **Tailwind:** government has publicly encouraged games rooted in Indian culture/heritage — Katha
  is squarely in that bucket ([00-research-and-market.md](00-research-and-market.md) §5).

---

## 8. The ask & use of funds (template — fill at raise time)
- **Stage:** pre-seed/seed after Phase-1 retention proof.
- **Use of funds:** content production (tales/arcs + art/voice), the LoRA/inference cost
  optimization, the Cultural Advisory Board for Phase 2, and the Mahabharata build.
- **Milestone the raise buys:** "from a retentive Phase-1 product to a launched, advisor-blessed
  Mahabharata arc" — i.e., funding the graduation ([05-phasing-roadmap.md](05-phasing-roadmap.md) §4).

---

## 9. Risks (name them before they ask)
| Risk | Honest answer |
|---|---|
| Cultural/religious backlash | De-risked by phasing + advisory + reverence + moderation ([04](04-cultural-fidelity.md), [05](05-phasing-roadmap.md), [07](07-moderation-and-safety.md)) |
| AI cost per turn | Designed-in levers + LoRA at volume; we track cost/session ([01](01-architecture.md) §7) |
| Retention unproven | Exactly why we launch Phase 1 first and raise on real data |
| Solo founder | Phasing keeps scope sane; advisory + early hires fill gaps; SISFS extends runway |
| Platform/LLM dependency | Provider-swappable engine ([01](01-architecture.md) §0) |

---

## 10. Open decisions
1. **Price points** — ₹ for story pack vs subscription; test in Phase 1.
2. **When to raise** — which retention number triggers the conversation ([05](05-phasing-roadmap.md) §4).
3. **Entity/incorporation timing** — gates SISFS/angel eligibility ([08](08-legal-and-compliance.md) §7).
4. **Brand architecture** — "Katha" platform with each epic as a "Book" (recommended).
