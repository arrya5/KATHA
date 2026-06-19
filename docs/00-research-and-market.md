# Katha — Research & Market Analysis

> Companion to [HANDOFF.md](../HANDOFF.md). This document grounds the project in the
> 2026 competitive, market, and regulatory landscape. Everything downstream
> (architecture, business model, pitch) references the findings here.
>
> **Last researched:** June 2026. Re-verify all figures before any investor conversation.
>
> **Phasing note:** the Mahabharata framing below is the long-term vision. Katha *launches* on
> the lower-risk **Vikram aur Betaal** and graduates to the Mahabharata — see
> [05-phasing-roadmap.md](05-phasing-roadmap.md). The market thesis (interactive > passive Indian mythology) holds for both.

---

## 1. One-line thesis

> **Mythik proved investors will pay for AI-generated Indian mythology. Mythik built
> *passive* video. Katha builds the *interactive* layer — a voice-first visual novel
> where every character is a living AI agent. Interactive has historically out-valued
> passive, and nobody has built it for Indian epics.**

---

## 2. The market is real, and it is moving

### 2.1 Direct validation — Mythik
- Founded **2025** by **Jason Kothari**. Converts Indian mythology / history / folklore
  into AI-generated **short-form video** (10–12 min episodes) — *passive* content.
- Funding to date ≈ **$20M**: ~$15M (May 2025, Bitkraft, Visceral Capital, others) +
  **$5M at a $50M+ valuation** (backers incl. Harsh Jain/Dream11, Blume Founders' Fund,
  Rajat Gupta, Bharti Mittal Family Office, Point72's Ishan Sinha).
- **Read for Katha:** Tier-1 capital believes "AI + Indian mythology + global diaspora"
  is a venture-scale category. Mythik is the *category proof*, not a competitor — they
  do lean-back video; Katha does lean-in play. Their existence de-risks the pitch's
  hardest question ("is this a real market?").

### 2.2 Category sizing (corroborating, not precise — cite carefully)
- **Visual novel games:** ~$9.4B (2025) → ~$21.8B (2034), ~9.8% CAGR.
- **Interactive fiction:** ~$4.3B (2025) → ~$7.8B (2032), ~12% CAGR.
- **India gaming:** ~20% of the *global* gamer base; ~82% of Indian gamers report
  interest in mythology-based games — large latent demand against near-zero serious supply.
- Treat these as directional. For a pitch, build a **bottom-up** model from Katha's own
  funnel (see [10-business-and-pitch.md](10-business-and-pitch.md)); use top-down only as a sanity ceiling.

### 2.3 The supply gap (the actual opportunity)
~82% interest, almost no serious supply. The reason is not technical — it is **risk
aversion**: studios fear religious/political backlash (see §4). That gap is Katha's
opening *and* its central execution challenge. The moat is being the team willing and
able to do mythology **respectfully at production quality** — a cultural/ops moat,
not just a tech one.

---

## 3. Competitive landscape

### 3.1 Global AI interactive fiction
| Product | What it is | Gap Katha exploits |
|---|---|---|
| **AI Dungeon** | Open-ended AI text adventure | No structure, no canon, no art/voice, no culture |
| **NovelAI** | Prose-quality AI writing/RP | Authoring tool, not a directed experience |
| **Character.AI** | 1:1 AI character chat | Chatbots, not a *world*; no shared canon or scenes |
| **Hidden Door** | Structured narrative RPG over licensed IP | Closest in *form*; Western IP, text-led, not voice-first or Indian |
| **Jenova / Dunia / DreamGen / FableAI** | New AI-RP/story engines | Generic; no cultural depth, no curated canon |

**The 2026 trend that matters:** persistent NPC memory / long-term relationships is now
the headline feature buyers care about. Katha's **3-layer RAG + per-NPC isolated
knowledge state** is exactly this, taken further than anyone (information *asymmetry*,
not just memory). This is the technical wedge — see [01-architecture.md](01-architecture.md).

### 3.2 Indian-mythology media
- **Mythik** — passive AI video (above).
- **Amar Chitra Katha** — the visual canon of Indian mythology for 3 generations; the
  art-direction north star (see [HANDOFF.md](../HANDOFF.md) → Visual Direction), and a possible licensing/partner conversation.
- **AAA/indie India games** (e.g. mythology-themed titles covered by ThePrint) — mostly
  action games that *borrow* aesthetics; none are character-driven, dialogue-first, or AI-generative.

### 3.3 Positioning statement
> *Katha is to the Mahabharata what a AAA story-mode RPG is to a film — except the
> characters are real AI agents who remember you and only know what they witnessed.
> Genshin/Fate-style presentation, Character.AI-grade agents, grounded in a curated
> public-domain canon, voice-first in Indian languages.*

**Whitespace = (Indian epic canon) × (AI agents w/ knowledge asymmetry) × (voice-first VN presentation).** No competitor occupies the intersection.

---

## 4. The central risk: cultural & religious sensitivity

This is the single most important strategic fact about Katha. It gets its own doc
([04-cultural-fidelity.md](04-cultural-fidelity.md)); summarized here because it shapes everything.

- Indians widely regard these figures as **living deities and ideal role models**, not
  literary characters. Krishna in particular is God, not an NPC to be "prompted."
- Precedent: the India–Japan **Ramayan: The Legend of Prince Rama** anime drew protests
  from VHP/RSS. Studios cite real fear of bans, protests, even physical risk.
- Some studios (e.g. Ogre Head Studio) deliberately **decouple from religion** and use
  mythology only as flavor. Katha cannot — fidelity *is* the product.

**Implication:** Katha must over-invest in authenticity and reverence as a first-class
discipline: curated canon, a cultural/scholarly advisory board, hard "never" rules in
every agent, reverent treatment of the divine, and a transparent fidelity policy. Done
right, this converts the risk into the moat (the reason no one else ships).

---

## 5. Regulatory reality (India, current as of 2026)

The HANDOFF's "IT Rules 2021" framing is **out of date** for games.

- **Promotion and Regulation of Online Gaming Act, 2025** (enacted Aug 2025) +
  **Online Gaming Rules, 2026** (in force **1 May 2026**), enforced by a new
  **Online Gaming Authority of India (OGAI)**.
- The Act bans **online money games**; it **permits** "online social games" and e-sports
  (e-sports requires registration). **Katha is an online social/story game** — in the
  permitted lane, with no real-money mechanic. This is favorable, *provided* monetization
  stays subscription/content-pack (no wagering, no loot-box-as-gambling).
- Still applies: **DPDP Act 2023** (data protection, incl. minors), grievance/IG
  obligations, age-appropriate design. Detailed in [08-legal-and-compliance.md](08-legal-and-compliance.md).

**Pitch implication:** Katha sits in the *encouraged* "Indian culture / social gaming"
bucket the government has publicly championed — a tailwind, not a headwind, if positioned
as cultural-heritage edutainment rather than "gaming."

---

## 6. Technology stack — viability check (2026)

| Layer | Choice | 2026 status |
|---|---|---|
| Orchestration | **LangGraph 1.0** | Production-grade; native checkpointing/persistence, parallel + hierarchical + conditional routing. Fits the multi-agent graph exactly. |
| Voice (STT/TTS) | **Sarvam AI** (Saarika STT, Bulbul v3 TTS) | Live, India-sovereign; 11 Indian languages, 30+ voices. Pricing ≈ STT ₹30/hr, TTS ₹15–30/10K chars, translation ₹20/10K chars; ₹1,000 free credits. 2–3× cheaper than global, better Indian accents. Cost model in [01-architecture.md](01-architecture.md) §cost. |
| Primary LLM | Gemini (long context) | Fine for narrator/long-context grounding. **Decision needed:** confirm Gemini vs a Claude/long-context alternative for the reasoning-heavy narrator. Keep provider-swappable. |
| Character model | LoRA on Llama 3.1 8B (dialogue corpus) | Optional V1+ optimization; not MVP-critical. Use prompt-engineered frontier model first, fine-tune only if voice consistency/cost demands it. |
| Vector DB | ChromaDB → Pinecone | Standard; fine. |
| App / API | React Native + Expo / FastAPI | Standard; fine. |

No blockers. The hard parts are **knowledge-state correctness** and **cultural fidelity**, not infrastructure.

---

## 7. Funding & founder context (for the pitch path)

- India gaming funding **+73.8% in 2026 vs 2025**; investor confidence returning.
- Relevant early-stage routes: **Indian Angel Network, LetsVenture, Mumbai Angels,
  Chennai Angels** (Arrya is Chennai-based — a warm local network), plus **Startup India
  Seed Fund Scheme (SISFS)** — *non-dilutive* grant capital well-suited to a student founder.
- Active mythology/gaming angels exist (e.g. Anupam Mittal; several Mythik backers).
- **Sequencing:** ship → get real day-7 retention → then raise. A working, reverent,
  retentive Katha with even a few thousand engaged users is a far stronger pitch than a deck.

---

## 8. Key open decisions (resolved or flagged in later docs)

1. **Source text strategy** — Ganguli (public domain) as corpus; BORI Critical Edition +
   Debroy as non-redistributed canonical reference → [02-data-pipeline.md](02-data-pipeline.md).
2. **Narrator LLM provider** — confirm Gemini vs alternative; keep swappable → [01-architecture.md](01-architecture.md).
3. **Cultural advisory** — who reviews canon & tone before launch → [04-cultural-fidelity.md](04-cultural-fidelity.md).
4. **Monetization** — free first arc, paid arcs vs subscription → [10-business-and-pitch.md](10-business-and-pitch.md).

---

## Sources

- [Sarvam AI — API pricing](https://www.sarvam.ai/api-pricing) · [Sarvam AI 2026 guide (Distk)](https://distk.in/blog/how-to-use-sarvam-ai-2026.html) · [Sarvam AI (Wikipedia)](https://en.wikipedia.org/wiki/Sarvam_AI)
- [Mythik raises $5M at $50M+ valuation (Inc42)](https://inc42.com/buzz/ai-entertainment-startup-mythik-raises-5-mn-at-50-mn-valuation/) · [Venture Intelligence](https://news.ventureintelligence.com/private-equity/indian-mythology-focused-entertainment-startup-mythik-raises-$5-m-at-$50-m-valuation) · [Indian Startup News](https://indianstartupnews.com/funding/jason-kotharis-mediatech-startup-mythik-raises-5-million-at-over-50-million-valuation-11857954)
- [AI Dungeon alternatives 2026 (Dunia)](https://dunia.gg/blog/alternative-to-ai-dungeon) · [Compare AI Dungeon alternatives 2026 (Exeleon)](https://exeleonmagazine.com/compare-ai-dungeon-alternatives-2026/)
- [Ganguli vs Debroy / BORI critical edition (Quora)](https://www.quora.com/Which-Mahabharata-is-better-Kisari-Mohan-Ganguly-or-Mahabharata-translated-by-Bibek-Debroy) · [Kisari Mohan Ganguli (Wikipedia)](https://en.wikipedia.org/wiki/Kisari_Mohan_Ganguli)
- [LangGraph 1.0 vs LangChain 1.0 (ClickIT)](https://www.clickittech.com/ai/langchain-1-0-vs-langgraph-1-0/) · [LangGraph in production (AlphaBold)](https://www.alphabold.com/langgraph-agents-in-production/)
- [Indian mythology in video games (ThePrint)](https://theprint.in/ground-reports/indian-video-games-finally-bring-mythology-into-storyline-taking-it-to-aaa-level/2839208/) · [Adapting Indian mythology for games (Medium)](https://medium.com/@sharath.ravi/unlocking-the-epic-adapting-indian-mythology-for-video-games-f578f2d45159)
- [Promotion & Regulation of Online Gaming Rules, 2026 (PIB)](https://www.pib.gov.in/PressReleasePage.aspx?PRID=2254606&reg=3&lang=1) · [Decoding the 2026 framework (Conventus Law)](https://conventuslaw.com/report/the-promotion-and-regulation-of-online-gaming-rules-2026-decoding-indias-new-regulatory-framework-for-online-gaming/) · [Online Gaming Act 2025 (Wikipedia)](https://en.wikipedia.org/wiki/Promotion_and_Regulation_of_Online_Gaming_Act,_2025)
- [Gaming investors in India (Shizune)](https://shizune.co/investors/gaming-investors-india) · [Startup India Seed Fund Scheme](https://seedfund.startupindia.gov.in/)
