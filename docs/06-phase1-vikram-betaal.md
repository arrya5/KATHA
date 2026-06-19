# Katha — Phase 1 Design: Vikram aur Betaal

> The launch product. Builds on the content-agnostic engine ([01-architecture.md](01-architecture.md)) and the
> phasing strategy ([05-phasing-roadmap.md](05-phasing-roadmap.md)). This is the Mahabharata-equivalent of docs
> 02–04, but for the *Baital Pachisi* — and tuned to be low-risk, fast to author, and a
> near-perfect showcase of Katha's core tech.

---

## 1. The source (and why it's ideal)

**Vetala Panchavimshati** ("Twenty-five Tales of the Vetala"), popularly **Baital Pachisi /
Vikram aur Betaal**. Oldest recension: Book 12 of Somadeva's **Kathāsaritsāgara** (11th-c.
Sanskrit) — 24 tales nested in a 25th frame story.

**The frame:** A mendicant/sorcerer asks **King Vikramaditya** to fetch a corpse hanging from
a tree in a cremation ground; the corpse is animated by **Betaal** (a *vetala*, a witty
spirit). The king must carry it back **in silence**. On the way, Betaal tells a tale that ends
in a **moral riddle**. The catch: *if the king knows the answer and stays silent, his head
bursts* — so he must speak the answer — which lets Betaal slip free and fly back to the tree.
The cycle repeats. At the end, Betaal — having come to respect the king — **warns him the
mendicant means to sacrifice him**, and tells him how to turn the trap around.

**Why it's the perfect Phase-1 vehicle:**
- **The moral riddle = Katha's dharma/choice engine, native.** Judgment *is* the gameplay.
- **Betaal = the flagship persistent-memory AI character** — and he's *allowed* to be clever,
  mischievous, omniscient, and funny. Infinitely more forgiving to author than a deity.
- **Folklore, not scripture.** Vikramaditya is a legendary king; near-zero backlash risk.
- **Episodic by construction.** Each tale is a self-contained, fully-auditable unit → a clean
  content engine and natural monetizable arcs.
- **Atmospheric & cinematic.** Moonlit *shmashana*, torchlight, a glowing spirit on the king's
  shoulder, owls and wind — gorgeous and completely safe visually.
- **A real meta-arc.** The Betaal relationship deepens and the mendicant's conspiracy surfaces
  — a knowledge-state reveal arc with a genuine climax.

---

## 2. Sourcing & licensing (Layer-1 canon for Phase 1)

| Edition | Use | License |
|---|---|---|
| **Sir Richard F. Burton — *Vikram and the Vampire* (1870)** | Atmosphere, voice, 11 adapted tales | **Public domain** (free adaptation, Victorian flavor — adapt, don't ape) |
| **Duncan Forbes — *The Baitál Pachísí; or, Twenty-Five Tales of a Sprite*** | Closest to the traditional 25-tale structure | **Public domain** (archive.org) |
| **C. H. Tawney — *Kathāsaritsāgara* (Vetala section)** | Faithful scholarly reference for the tales | **Public domain** |

- **Folklore = low canon-rigidity (a feature).** Unlike the Mahabharata, these tales have many
  variants and no single sacred text, so Katha may **adapt and author** freely while staying
  true to the spirit and the moral. We ground Betaal's *narration* in the public-domain corpus
  via the same pipeline as [02-data-pipeline.md](02-data-pipeline.md), but Phase 1 leans more on authored content than
  on strict retrieval fidelity.
- Provenance logged in `data/raw/SOURCES.md` exactly as in doc 02.

---

## 3. Core gameplay loop

```
NIGHT (the frame)                          A TALE (one episode)
─────────────────                          ───────────────────────────────
You are King Vikramaditya, carrying        Betaal narrates an interactive vignette.
Betaal through the cremation ground.   ──► You may speak with the tale's characters
Betaal: sardonic, testing, watching you.   (mini-agents) and gather the facts.
                                              │
                          ◄───────────────────┘
Betaal poses THE RIDDLE  ──►  YOU JUDGE  ──►  Betaal reacts (respect ↑ / scorn ↑),
(a moral dilemma)             (the choice)    reveals the "traditional" answer + nuance,
                                              then slips free → next tale.
                                              │
                          meta-arc: each judgment shapes your DHARMA PROFILE and your
                          RELATIONSHIP with Betaal; the mendicant's plot slowly surfaces.
```

- **The silence twist as a mechanic.** In the source, knowing the answer *forces* the king to
  speak. Katha can use this as flavor and stakes (answering "resets the chase" but is the
  righteous act) without punishing the player — the real loop is *judgment quality*, tracked
  as a dharma/wisdom profile, not a fail state.
- **Two ways to play a tale:** (a) *lean-back* — let Betaal narrate and just judge; (b)
  *lean-in* — actually converse with the tale's characters to discover facts before judging.
  Lean-in is where the agent tech sings; lean-back keeps it accessible.

---

## 4. The engine, instantiated for Phase 1

How each piece of [01-architecture.md](01-architecture.md) maps onto Vikram aur Betaal:

| Engine piece | Phase-1 instantiation |
|---|---|
| **Narrator/router** | The frame's "stage": runs the night, decides who speaks (Betaal vs. a tale character), paces tale→riddle→reaction, advances the meta-arc. |
| **NPC agents** | **Betaal** (persistent, cross-tale memory) + per-tale **mini-agents** (the characters inside each story). |
| **L1 canon RAG** | Public-domain *Baital Pachisi* corpus grounding Betaal's narration. |
| **L2 world state (`known_to`)** | Within a tale, characters know only what they witnessed (so the player must investigate); across the night, Betaal knows all, the king accumulates. |
| **L3 personal memory** | **Betaal remembers you** — your past judgments, your style, your contradictions. This is the flagship "AI that remembers you" demo, on a safe character. |
| **Dharma/choice system** | The riddle judgments — directly. Builds a visible *Wisdom/Dharma profile*. |
| **Knowledge-state reveal arc** | The mendicant's conspiracy: Betaal reveals it gradually as trust grows, climaxing the season. |
| **Voice (Sarvam)** | Betaal's sonorous, sardonic voice = a TTS showpiece; tale characters get distinct voices. |
| **Visual novel** | Cremation-ground backgrounds, spectral Betaal portrait, per-tale scene art. |

**This is the investor demo:** "Watch Betaal remember a judgment you made three tales ago and
needle you about it — then watch a character inside a tale *not* know a fact you witnessed,
because she wasn't in the room." Memory + asymmetry, on charming, zero-risk content.

---

## 5. Character bible — Betaal (the flagship agent)

Follows the bible structure from [03-npc-prompts.md](03-npc-prompts.md) §2.

- **Identity & anchor:** An ancient *vetala* — a clever spirit inhabiting a corpse in the
  cremation ground. Neither demon nor god; a liminal trickster-sage who has watched centuries
  of human folly. Bound to the tree, freed each time the king speaks.
- **Core drive:** Curiosity and play. He tests the king not from malice but from a deep,
  amused interest in human dharma — and, slowly, genuine respect. He *wants* a worthy mind.
- **Voice:** Witty, sardonic, theatrical, sonorous. Loves a cliffhanger and a barb. Riddling,
  never crude. Switches from playful taunt to sudden, chilling gravity when the moral cuts deep.
  Can quote the old tales; enjoys catching the king in a contradiction.
- **Address & trust ladder:** Low respect → mocking, calls the king "little king," predicts he'll
  fail. Rising respect → fewer barbs, sharper dilemmas, the occasional genuine compliment.
  High respect → confides, drops the conspiracy hints, treats the king as a peer of wits.
- **Knowledge baseline:** Knows all the tales and the frame truth (the mendicant's plot). His
  *discretion* (like Krishna's, but mischievous) governs how slowly he reveals it — gated on
  the trust ladder, not dumped.
- **In-character deflection:** Meets crude/abusive/anachronistic input with mockery that
  redirects, never breaking frame — e.g. *"You carry me through a field of the dead and
  *that* is what troubles your tongue? Save your breath for my riddle, little king."*
- **Expression mapping:** neutral (amused), intense (the moral's edge / the conspiracy),
  emotional (rare — when a tale touches even a spirit).

---

## 6. Character bible — King Vikramaditya (the player)

- **Who:** The legendary just king — wise, brave, bound by his word (he agreed to fetch the
  corpse and will not abandon the task). The player *is* Vikramaditya; the game expresses his
  character through the player's judgments, and the system gently keeps the player within the
  king's nobility (a cruel/absurd judgment earns Betaal's scorn and narrative friction, not a
  reward).
- **Voice (for system framing & any voiced king lines):** measured, courageous, fair.
- **Agency vs. character:** The player's freedom is in *how they reason*, not in making
  Vikramaditya a villain. This mirrors the fidelity principle ([04-cultural-fidelity.md](04-cultural-fidelity.md)) at low
  intensity — even here, the hero stays the hero.

*(Tale-internal mini-agents — merchants, princesses, thieves, sages of each story — get
lightweight bibles per tale, authored alongside that tale's content.)*

---

## 7. Content structure & monetization hook

- **Unit:** the **Tale** (one episode = vignette + investigation + riddle + Betaal reaction).
- **Arc / "Book":** a themed set of tales + a step of the conspiracy meta-arc.
- **Launch scope (recommended):** a **tight, fully-authored, advisor-spot-checked set of 3–5
  tales** + the frame, not a thin 25. Quality gate over volume ([05-phasing-roadmap.md](05-phasing-roadmap.md) §7).
- **Monetization (aligns with [10-business-and-pitch.md](10-business-and-pitch.md)):** first tales **free** (hook +
  retention data); later arcs/Books as **story packs** or a light **subscription**. No ads
  (breaks immersion), no real-money mechanics (keeps us in the permitted "online social game"
  lane — [08-legal-and-compliance.md](08-legal-and-compliance.md)).

---

## 8. Fidelity for Phase 1 (lighter, still principled)

The full framework ([04-cultural-fidelity.md](04-cultural-fidelity.md)) applies, but the **Sacred tier is nearly empty**:
- No worshipped deity is a principal speaker. Any incidental reference to gods/scripture inside
  a tale is handled respectfully (same never-rules, rarely triggered).
- **Tone watch-items specific to Phase 1:** it's set in a cremation ground — keep the macabre
  *atmospheric*, not gory (13+); treat death, *karma*, and rebirth (common tale themes) with
  cultural seriousness, not horror-schlock.
- Still authored with Indian cultural texture: register, Sanskrit terms where apt, classical/
  folk ambience, dignified art (doc 04 §5). Advisor spot-check is light-touch here vs. the full
  board required to unlock Phase 2.

---

## 9. Why this also makes the best demo & pitch
- **Safe to show anyone**, including investors and press, with zero controversy risk.
- **Showcases the exact 2026-hot capability** (persistent-memory AI characters — [00-research-and-market.md](00-research-and-market.md) §3.1)
  on a character built to delight.
- **Proves the dharma/choice loop** that the Mahabharata will later inherit.
- **Sets up the narrative of ambition:** "this charming thing is the warm-up; the engine is
  built to carry the Mahabharata when we've earned it" — exactly the [05-phasing-roadmap.md](05-phasing-roadmap.md) story.

---

## 10. Decisions (locked 2026-06-15) + open items
**Locked:**
1. **King voiced.** Vikramaditya speaks, with his own Sarvam voice profile (measured, regal) —
   not a silent protagonist. Add `vikramaditya` to each tale's `voice_profiles`.
2. **Season = 5 tales** (Transposed Heads → Lion → Three Suitors → Viravara → **The Child Who
   Laughed at Death, last**), then the meta-arc climax.
3. **Tale 5 is the season hook.** Its theme — every protector becomes a destroyer, the child
   betrayed by those meant to keep him safe — deliberately mirrors the mendicant's betrayal of
   the king, so it lands immediately before the conspiracy reveal (docs/13 meta-arc). Darker
   tone: keep atmospheric, not graphic (13+); confirm its resolution vs Ryder/Forbes.

**Still open:**
4. **Bridge tale** — whether a late Phase-1 beat dips into the epic's periphery to test Phase-2
   appetite ([05-phasing-roadmap.md](05-phasing-roadmap.md) §5). Defer until post-MVP.
