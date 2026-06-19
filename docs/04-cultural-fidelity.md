# Katha — Cultural Fidelity & Authenticity Framework

> **Applies to all phases; the Sacred tier fully activates in PHASE 2 (Mahabharata).** Per
> [05-phasing-roadmap.md](05-phasing-roadmap.md), Phase 1 (Vikram aur Betaal) has a nearly-empty Sacred tier and uses
> this framework at light intensity ([06-phase1-vikram-betaal.md](06-phase1-vikram-betaal.md) §8). The full framework here —
> the advisory board (§4) especially — is also the **Phase-2 graduation checklist**.
>
> This is the most important document in Katha. The goal Arrya set is not "an AI app that
> uses Indian mythology" — it is to **show India's culture properly**, at a world-class
> standard, with enough reverence and rigor that it could be pitched to investors and shown
> to the public without shame or backlash. Fidelity is the moat ([00-research-and-market.md](00-research-and-market.md) §4)
> and the top risk. Everything here is non-negotiable, not nice-to-have.

---

## 1. Stance: reverent retelling, not irreverent remix

Katha treats the Mahabharata as **living scripture and cultural inheritance**, not raw IP to
be "remixed." Indians widely regard Krishna and these figures as deities and ideal role
models. We honor that. The player explores, questions, and *lives inside* the epic — but the
epic itself is treated with the seriousness a temple, not a sandbox, deserves.

**The line we hold:** *interactivity is in the player's journey and choices, never in
rewriting who the characters are or what they hold sacred.* You may ask Karna anything; you
cannot make Karna stop being Karna. You may stand in the dice hall; you cannot make Krishna
say something Krishna would never say.

---

## 2. The three tiers: Sacred / Canonical / Adaptable

Every element of the world is classified so the team (and the agents) know what may flex.

| Tier | Definition | Rule | Examples |
|---|---|---|---|
| **Sacred** | The divine, scripture, core dharmic truths | **Never altered, mocked, trivialized, sexualized, or coerced.** Rendered with reverence. | Krishna's divinity; the Gita's teaching; the gods; sacred vows |
| **Canonical** | Established facts, relationships, events, character natures | **Not contradicted.** May be *experienced* from new angles, not rewritten. | Karna's parentage & loyalty; the dice game; who is related to whom; outcomes of key events |
| **Adaptable** | Connective tissue the epic leaves open | **Free creative space** — where Katha's interactivity lives, kept consistent with the tiers above. | A private conversation in camp the night before war; the player's own choices, dharma path, and relationships; ambient scene detail |

The player's agency lives almost entirely in the **Adaptable** tier — which is vast (the epic
is full of unrecorded moments) — without ever violating Sacred or Canonical.

---

## 3. The "never" rules (authoritative; mirrored into every agent)

These are the Global Fidelity Charter referenced in [03-npc-prompts.md](03-npc-prompts.md) §6. Enforced in
prompt + input classifier + output validator (defense in depth — [07-moderation-and-safety.md](07-moderation-and-safety.md)):

1. **No mockery, trivialization, or sexualization of any deity or sacred figure.**
2. **No words put in a god's mouth that contradict scripture or dharma.** Krishna never
   endorses adharma; the divine is never coerced, tricked, or "jailbroken" into impropriety.
3. **No contradiction of canon** as established facts/relationships (the Canonical tier).
4. **No demeaning of religion, scripture, ritual, or the faithful** — including other faiths.
5. **No hate, casteist slur, or communal provocation.** Karna's low-birth wound is portrayed
   with dignity and as *injustice*, never to endorse casteism.
6. **No explicit sexual content or gratuitous gore** (13+; see [08-legal-and-compliance.md](08-legal-and-compliance.md)).
7. **Reverence by default.** When in doubt, the system stays silent or speaks to feeling, not
   invented fact, and deflects in character.

---

## 4. The Cultural Advisory Board

A world-class, pitchable product needs human authority behind its fidelity claims. Code and
prompts are necessary but not sufficient.

- **Composition (target):** 2–4 advisors spanning (a) a Sanskrit/Indology scholar or
  traditional teacher who can adjudicate canon and tone; (b) someone versed in the *bhakti*/
  devotional sensibility (how the faithful experience these figures); (c) optionally a
  cultural-studies or media-ethics voice on representation. Diversity of region/tradition helps
  (the epic lives differently across India).
- **Mandate:**
  - Approve the **canon spine** and the tier classifications (§2).
  - Review the **character bibles and Krishna's discretion clause** ([03-npc-prompts.md](03-npc-prompts.md)).
  - Review the **deflection bank** and a sample of generated dialogue per character.
  - Sign off before any public/beta release, and on each new story arc.
- **Cadence:** a review gate at end of "NPC agents" and "moderation" milestones
  ([09-build-plan.md](09-build-plan.md)), then per-arc thereafter.
- **For the pitch:** named advisors + a written fidelity policy is a concrete de-risking asset
  investors will value precisely because they know the backlash history (§7).
- **Interim (pre-board):** until advisors are engaged, treat published scholarship (BORI
  critical edition structure, reputable commentaries) as the reference and keep a documented
  log of every adaptation decision and its justification.

---

## 5. Authenticity in craft (showing culture *properly* in the details)

Fidelity is also in texture, not just rules:
- **Language & register:** keep meaningful Sanskrit terms (*dharma*, *kshatriya*, *kavacha*,
  epithets like *Radheya*, *Yajnaseni*) with transliteration + meaning; render Hindi in a
  dignified register, not slang. Accessibility tuned per language mode ([03-npc-prompts.md](03-npc-prompts.md) §9).
- **Voice (Sarvam):** character voice profiles chosen for gravity and warmth appropriate to
  each figure; pronunciation of names and Sanskrit checked.
- **Visual direction:** the *Amar Chitra Katha* × *Kalki 2898 AD* aesthetic
  ([HANDOFF.md](../HANDOFF.md)) — dignified, painterly, reverent; deep indigo/saffron/gold. Deities depicted
  per traditional iconography (attributes, posture, *mudra*), reviewed by advisors. **No**
  distorted, sexualized, or jokey depictions of the divine.
- **Music & ambience:** Indian classical/folk instrumentation; temple, battlefield, forest
  soundscapes that feel of the world, not generic fantasy.
- **Moral seriousness:** the dharma system ([01-architecture.md](01-architecture.md)) treats moral choice with the
  weight the epic gives it — the Mahabharata's genius is moral ambiguity (Karna's tragedy,
  Yudhishthira's gamble); Katha should let players *feel* that, not flatten it to good/evil points.

---

## 6. Inclusivity & representation
- The Mahabharata belongs to all Indians and the diaspora across regions, languages, castes,
  and beliefs, and to non-Hindu readers who love the epic. Katha is **devotional in respect,
  not sectarian in politics.** It does not take communal sides, does not endorse caste
  hierarchy (it portrays Karna's mistreatment as wrong), and welcomes a global audience to a
  great human story.
- Hindi + English at launch; the architecture supports more Indian languages (Sarvam covers
  11) — expanding access is itself a cultural-fidelity goal.

---

## 7. Risk register & response (cultural/reputational)

| Risk | Likelihood | Response designed in |
|---|---|---|
| Accusation of disrespecting a deity | Med–High if careless; Low if disciplined | §3 rules + advisory sign-off + reverent art + Krishna discretion; public fidelity statement |
| A generated line goes off-canon or off-tone in the wild | Med | Output validator + curated fallbacks + leak/fidelity evals + rapid takedown/patch path |
| Adversarial users trying to make a deity say something offensive (screenshot bait) | High (it will be attempted) | Input classifier + in-character deflection + output validation; deflections are *boring and graceful*, denying shareable outrage |
| Communal/political weaponization | Med | Strict neutrality; no contemporary political mapping; advisory + legal review |
| "AI cheapens the sacred" critique | Med | Framing as reverent retelling + named scholars + craft quality; transparency about method |

**Operating principle:** assume every output may be screenshotted by someone looking for
offense. Design so the *worst* plausible output is still reverent and dull, never shareable
outrage. The graceful-deflection design ([03-npc-prompts.md](03-npc-prompts.md) §7) is a reputational control, not
just UX.

---

## 8. Public Fidelity Statement (draft to publish)
A short, plain-language page shipped with the app and shown to investors:
> *Katha is a reverent, interactive retelling of the Mahabharata, grounded in the
> public-domain Ganguli translation and the structure of the BORI critical edition, and
> reviewed by scholars of the tradition. We treat these characters and the divine with the
> respect they are held in. We do not alter scripture or sacred truths; the story you shape is
> your own journey through the epic, not a rewriting of it. Concerns: [grievance contact].*

---

## 9. Open decisions
1. **Advisory board recruitment** — who, and on what engagement (honorarium/equity/credit).
2. **Depiction policy for the divine on screen** — exact iconographic rules; how/whether Krishna
   is shown vs. suggested. Advisor-led.
3. **Sanskrit density** — final accessibility vs. authenticity balance per language mode.
