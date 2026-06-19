# Katha — Phase 1 Content: Tales 2–4 + the Meta-Arc

> Authored to the template established in [11-phase1-content-tales-and-betaal.md](11-phase1-content-tales-and-betaal.md) Part C
> (scene → beats → lean-in → riddle → branches → state). These are design drafts to encode
> as data in `backend/app/content/tales.py` (the Transposed Heads is already encoded there).
> **Accuracy:** verify resolutions vs Ryder's *Twenty-Two Goblins* / Forbes and log in
> `data/raw/SOURCES.md` before finalizing. Folklore has variants; adapt to the moral, faithfully.

---

## Prologue — Why the King Walks into the Dark  *(the arc's cold-open)*

> The frame story: the canonical reason the king goes to fetch the corpse. Grounded in the
> *Kathāsaritsāgara* (Somadeva) / *Vetāla­pañcaviṃśati* and the popular Vikram–Betaal. This is
> the first thing a new player sees — and it secretly plants the conspiracy that the meta-arc
> (below) pays off. Encoded in `tales.py` as the `prologue` scene (kind="prologue").

- **scene_id:** `betaal.prologue` · **setting:** the court of Ujjain (day) → the great
  cremation ground at night. · **voiced by:** the narrator/Sutradhar (Betaal appears only at the end).

### The canonical reason (sourced)
A mendicant, **Kshantishila** ("of patient virtue" — a name whose irony Betaal will later relish),
a yogi of grave bearing, comes to King **Vikramaditya's** court day after day and, asking nothing,
places a single fruit in the king's hand. The king passes each to his treasurer. One day a palace
monkey snatches a fruit; it breaks open and a **priceless jewel** rolls out — and the treasury
reveals that *every* fruit held one. The king asks why he is so honoured. Kshantishila asks his
return-favor: on the **14th night of the dark fortnight**, the king must come **alone** to the
burning-ground beyond the city, to the lone **śiṃśapā tree** where a corpse hangs, and bear it to
him — for a rite that will win him a power that comes but once in an age (*vetāla-siddhi*, mastery
over the spirit in the corpse). The king, who by his nature never refuses a sincere request and
does not fear the dark, agrees. He goes alone, cuts down the corpse — and **Betaal wakes on his
shoulder** and proposes the game. *(Kshantishila's hidden intent: to sacrifice the king to
complete the rite — withheld here, revealed at the climax.)*

### Beats (narrator)
1. **Court:** for many days the silent yogi gives the gracious king a daily fruit.
2. **The reveal:** the monkey, the shattered fruit, the jewel; the treasury opened — a fortune
   given daily, and nothing asked. *"What manner of man gives a kingdom's ransom and asks nothing?"*
3. **The request:** Kshantishila's favor — the 14th night, the śiṃśapā tree, the corpse, the rite.

### Lean-in: question Kshantishila before you answer (the conspiracy, seeded by the engine)
The mendicant is a mini-agent. He will speak of the **fruits** and the **request** (witnessed
facts). His **true intent** is a fact `characters_present: []` — retrievable by *no one* — so when
the king presses him on the rite's purpose, he can only **deflect piously**: the engine *cannot*
surface what he will not confess. (Betaal, omniscient over the frame, knows it — and saves it for
the climax.) This is the information-asymmetry system planting the whole season's dread in the
opening scene, for free.

### The player's stance (a choice that matters at the climax)
The king *will* accept (canon) — but **how** sets a `mendicant_suspicion` flag that changes the
finale ([meta-arc](#the-meta-arc--the-mendicants-conspiracy) climax / trust gate):
- **(A) Trusting** — "A king's word is his bond; I think no ill of a generous man." → *low* suspicion.
- **(B) Wary** — "A gift without reason is a debt in disguise; I will watch this holy man." → *high* suspicion.
- **(C) Probing** — "First tell me plainly to what end this rite." (Kshantishila deflects; the king
  lets it pass, his word half-given.) → *medium*.

Each leads into the same night-journey narration: the king walks alone through the burning-ground,
cuts the corpse from the śiṃśapā, and Betaal wakes, laughs, and states the rule (*answer my riddle
or your head bursts; answer and I fly back*) — flowing straight into **Tale 1: The Transposed
Heads**. The opening stance is recalled at the climax: the wary king is vindicated; the trusting
king is the one Betaal must work hardest to save.

---

## Tale 2 — The Four Brahmins and the Lion

- **tale_id:** `four-brahmins-lion` · **scene:** a moonlit clearing, scattered bones, a banyan.
- **Theme:** knowledge without judgment (a parable that reads, uncannily, like an AI-safety fable).

### Beats (Betaal)
> "Four brahmins, learned past sense, crossed a forest and found the bleached bones of a lion.
> 'Behold,' said the first, 'a chance to show what our years of study are worth.' One drew the
> scattered bones into a skeleton. The second clothed it in flesh and hide. The third filled it
> with blood and breath's vessels. And the fourth raised his hand to give it *life*. 'Stop —'
> said a fifth, a plain man who had merely followed them, 'it is a *lion*.' They laughed at him.
> He climbed a tree. The fourth spoke the word of life... and the lion rose, and ate the three
> who had made it, while the plain man watched from the branches."

### Lean-in mini-agents (witnessed-bounded)
- **The Tree-Climber** (the cautious one): witnessed everything; knows *why* he doubted.
  `unknown` for anything after he fled the scene mentally — but he saw it all from the tree.
- **The First Brahmin** (skeleton-maker): present for the making; **cannot** speak to what the
  plain man was thinking (`characters_present` excludes the climber's private reasoning).

### Riddle
> "Three men of great learning lie in a lion's belly, little king. Tell me — which of them was
> the greatest *fool*?"

### Choices & branches
- **(A) The fourth** — who gave it life *knowing* it was a lion. ← *canonical*
  > "Just so. Knowledge is a sword; the fourth swung it with his eyes open and his sense shut.
  > Learning that will not pause to ask *should I* is the most dangerous thing in any age."
  `trust +`, memory: "values judgment over raw capability — wary of power used without a pause."
- **(B) All three equally** — they built toward it together.
  > "A fair severity. Each laid a stone in the road to their own grave. Yet one still might have
  > stopped at the last step and did not — the hand that acts last owns the deed. Half-right,
  > which from you I will take." `trust +small`.
- **(C) The tree-climber** — the coward who didn't stop them.
  > "Ha! You'd blame the one man who lived? Careful, king — a world that mocks the cautious for
  > cowardice is a world that keeps reviving lions. Wrong, by the old reckoning — but you've a
  > king's taste for action, I'll grant." `trust 0`, memory: "prizes action; suspicious of caution."

---

## Tale 3 — The Three Suitors of the Dead Maiden

- **tale_id:** `three-suitors` · **scene:** a riverbank ghat at night, a cold pyre, jasmine.
- **Theme:** desert and identity — the "obvious" answer is wrong for a subtle, cultural reason.

### Beats (Betaal)
> "A merchant's daughter, lovely beyond saying, was loved by three men, and she could wed but
> one. Before any could win her, a serpent took her life. The first, mad with grief, built her
> funeral pyre and gave her ashes to the river. The second gathered what ashes remained and made
> of them a shrine, and lived beside it, eating nothing the world offered. The third wandered to
> a sage, learned a word of power, returned, and from the kept ashes *raised her, living, whole*.
> And all three claimed her — the one who burned her, the one who kept her, the one who raised her."

### Lean-in mini-agents
- **The Ash-Keeper:** witnessed his own vigil; speaks of devotion as *being*, not deed.
- **The Reviver:** witnessed the sage and the mantra; **cannot** speak to the maiden's heart
  (she never chose; `characters_present` excludes her preference — there is no such fact to leak).
- **The Maiden** (after revival): knows she *died* and *woke*; **cannot** say who loved her
  truest — she witnessed none of their grief.

### Riddle
> "Three men, one woman, and death undone. Tell me, just king — *whose wife is she now*?"

### Choices & branches
- **(A) The ash-keeper** ← *canonical*
  > "Yes — and here the clever stumble. The one who *raised* her acted as a *father* gives life;
  > the one who *burned* her did a *son's* last duty. By their own deeds they became her parent
  > and her child — and only the one who simply *stayed*, asking nothing, remained a husband.
  > Love that demands no credit. You saw it." `trust ++`, memory: "sees love as constancy, not grand acts."
- **(B) The reviver** — he gave her life again; surely he earns her.
  > "The obvious crown — and the wrong head. To give life is a father's gift, not a husband's.
  > He made himself her parent and argued himself out of her bed. The tale is crueller and
  > cleverer than it looks, little king." `trust 0`.
- **(C) Let the maiden choose** — she is not a prize to be awarded.
  > "*Now* you sound like a king worth the name — though the old judges would say you dodged
  > their question. Still: a man who remembers the woman is a person, not a purse, will rule
  > better than one who answers riddles cleanly. I'll allow it." `trust +`, memory: "grants agency; resists treating people as objects."

---

## Tale 4 — Viravara, the Loyal Servant  *(place late: the heaviest, and the bridge to Phase 2)*

- **tale_id:** `viravara` · **scene:** a palace gate at the dead of night, a weeping unseen woman.
- **Theme:** loyalty vs. morality — how far may duty go? Direct rhyme with Karna ([03](03-npc-prompts.md)).

### Beats (Betaal)
> "Viravara took service with a king and was paid a fortune to, it seemed, do nothing. One night
> a woman wept in the dark — the kingdom's own Fortune, who foretold the king would die within
> days unless a life were freely given to the Goddess. Viravara went home, woke his son, his
> wife. The boy *offered his own neck* that the king might live; the wife would follow her child;
> Viravara would follow them all, and then fall on his own sword for his lord. The king, who had
> crept out and watched it all from the shadows, could not bear what his service had cost."

### Lean-in mini-agents
- **Viravara:** witnessed the weeping Fortune and his family's consent; speaks of duty as a debt
  beyond price. **Cannot** speak the king's private anguish (he didn't see the king watching).
- **The Son:** witnessed his own choice; **cannot** know whether the king deserved it — that is
  not his to judge, and he never saw the king.

### Riddle (two-stage — note the deliberate openness)
> "A servant who would spend his son, his wife, and himself for a master who asked nothing of
> him. Tell me, king — *whose act was the noblest*? And quieter, where your skull can hear it:
> *was such loyalty right at all*?"

### Choices & branches  *(versions of the tale differ; the tension is the lesson, not a clean key)*
- **(A) The son** — he gave the most, having lived the least.
  > "The young throat offered first and freest — yes, many a judge has crowned him. To give a
  > whole unlived life... there is a terrible purity in it." `trust +`.
- **(B) The king** — noblest for being unwilling to be served at such a price. ← *frequent canonical lean*
  > "Ah. You honour the one who *refused the gift*. A throne that will not climb over the bodies
  > of the loyal is a rare throne. The old tellers often judged the same — a king who counts his
  > servants' lives dearer than his own." `trust ++`, memory: "weighs a leader by what he refuses to spend — power as restraint."
- **(C) Loyalty this total is *not* right** — no master is owed a man's children.
  > *(grave, the mischief gone)* "...You may be the first king to say it to me plainly. Hold that
  > thought, little king. There are tales coming — older, bloodier than this folk-fire — where a
  > great man gives such loyalty to an unworthy lord, and the whole world burns for it. I wonder
  > what you will say to *him*." `trust ++`, memory: "questions loyalty owed to the undeserving — primed for the Mahabharata (Karna)."
  > *(This line is the explicit thematic bridge to Phase 2; see [05](05-phasing-roadmap.md) §5.)*

---

## Tale 5 — The Child Who Laughed at Death  *(THE HOOK — placed LAST; leads into the climax)*

- **tale_id:** `child-who-laughed` · **scene:** a torchlit sacrificial court at the edge of
  dawn — a bare stone slab, marigolds, a raised blade.
- **Theme:** the powerful owe protection to the helpless; betrayal by one's own guardians is the
  deepest wrong. Tonal note: **darker — keep atmospheric, never graphic (13+)**; the horror is
  moral, not gore. Confirm resolution vs Ryder/Forbes.

### Beats (Betaal)
> *(grave from the first word — none of the usual mischief)* "One more, little king, before the
> night gives you up. A king once sought a power that demanded a price: a boy without blemish —
> beautiful, brave, whole — offered freely to the Goddess. No noble would give a son, so heralds
> went out with gold. And a brahmin and his wife, who had not eaten in days, who had nothing in
> the world but one child... took the gold. They led him themselves to the altar. The king
> raised the sword. And the boy — this is the thing I have carried a long time — the boy looked
> slowly round at them all... and *laughed*. A clear, ringing laugh. Then he bared his throat."

### Lean-in mini-agents
- **The Boy:** witnessed his parents take the gold and the king lift the blade; will state those
  facts plainly, but turns the *why* back on the asker — "ask the living why, my lord; I am
  busy dying." (He won't hand you the riddle's answer.)
- **The Brahmin Father:** witnessed the bargain and his own shame; **cannot** speak the meaning
  of the laugh — he saw it, but not the mind behind it (`characters_present` excludes the boy's
  thought).

### Riddle
> "The blade above his throat, his own mother's gold still warm in the priest's hand — and he
> *laughed*. Tell me, just king, and tell me true: **why did the child laugh?**"

### Choices & branches
- **(A) Because every protector had become a destroyer** — parents, king, all who should have
  shielded him held a blade instead; he laughed at a world turned upside down. ← *canonical*
  > *(grave, with deep respect)* "Yes. A babe is kept by its mother, a child by its king, all
  > souls by the gods. His mother sold him; his king lifted the knife; the gods watched. Where,
  > in all that courtyard, was a single guardian left? He laughed because every hand meant to
  > shield him had turned to steel. ...You understood him, little king. Hold that close — you
  > will need it before this night is done." `trust ++`, memory: "grasps that the powerful owe
  > protection to the helpless; betrayal by guardians is the deepest wrong." → primes the climax.
- **(B) Because he was brave / a holy soul unafraid, welcoming release.**
  > "A gentle reading, and not a foolish one — some children do meet death like saints. But this
  > laugh was not peace; it was an indictment. He did not rise above the world — he saw it
  > plainly and named it. Half-true, king." `trust +`.
- **(C) Because he saw the sheer absurdity of it — madness, or a height beyond fear.**
  > "Madness, you say? It is always easier to call a thing madness than to admit it is an
  > accusation we have earned. He was the sanest soul in that courtyard. Wrong, I think — but you
  > flinched from the cruelty of the true answer, and that flinch is its own small mercy."
  > `trust 0/+`, memory: "looks away from hard truths about power — merciful but evasive."

### Transition into the climax
On finishing tale 5 (Betaal now at or near peak trust), he turns the tale on the king himself —
the hook:
> *"You asked me why a child laughs as his guardians betray him. Now answer this, while your
> skull still sits on your shoulders: a holy man sent you — a king — into a field of the dead to
> carry a corpse on your own back. Have you truly never wondered **why**?"*

---

## The Meta-Arc — the Mendicant's Conspiracy

A thread that runs *between* the tales and climaxes after them — turning a riddle anthology into
a story with stakes, and giving Betaal a real relationship to earn.

### The truth (known to Betaal from turn one; revealed only as trust rises)
The mendicant who sent the king to fetch the corpse is a **tantrik sorcerer**. Delivering Betaal
lets him complete a rite for great occult power — and the rite's final offering is **the king
himself**: once the king bows before the assembled circle, the sorcerer means to behead him.
Betaal knows. At first he doesn't care — kings come and go. But a worthy mind is rarer than a
king, and as the king proves himself, Betaal decides this one should *live*.

### Beats, gated by trust (docs/01 §4 discretion)
- **Low trust (early tales):** only atmosphere — Betaal needles, "the mendicant chose *you* for
  this errand; did you never wonder *why* a holy man needs a king to carry his corpse?"
- **Rising trust:** a fragment — "When you deliver me, he will ask you to do a small thing. A
  courtesy. Refuse nothing he asks tonight and you may not see the dawn." (A `reveal` payload on a
  high-trust turn — the engine already supports `NpcDraft.reveal`.)
- **High trust (after the tale set):** the full warning — *"He will ask you to bow full-length
  before the circle. Do not. Tell him a king bows to no one and ask **him** to show you how it is
  done — and when he lowers his head, end it. I have watched a hundred kings die for politeness. I
  would not watch you."*

### The climax (a final, weightier choice)
At the cremation ground's heart, the sorcerer waits. The player faces a last decision that pays
off everything:
- **Heed Betaal** (earned only at sufficient trust — the relationship *mechanically* matters):
  ask the sorcerer to demonstrate the prostration → turn the trap → the king lives, and Betaal,
  freed of his tree at last, departs with something like respect.
- **Ignore / distrust Betaal:** a darker ending — a narrow escape or a somber "what might have
  been," seeded for replay.
- **Trust gate:** if the player spent the season being cruel or contemptuous (low trust, strikes),
  Betaal gives the warning *grudgingly or not at all* — the season's relationship has consequences.

### Implemented in the engine (`tales.py` CLIMAX + `nodes.py`)
- **Scene** `climax` (kind="climax"), reached via `scene_id="climax"` after Tale 5.
- **Warning fullness = trust tier** earned across the tales: `high` (trust ≥ 18) → full warning +
  the prostration ruse; `mid` (≥ 6) → a terse "turn the trap yourself"; `low` (< 6, or ≥ 3
  strikes) → a cold, minimal warning. The prologue `mendicant_suspicion` flag adds the opening aside.
- **Final choice → outcome:** A *ask him to demonstrate, then strike* → `king_triumphant`
  (best; emperor of the age, Betaal departs with respect — and a Book-2 hook); B *refuse and face
  him* → `just_but_empty` (lives, but the power escapes); C *bow* → `narrow_escape` (at high trust
  Betaal saves you; at low trust, a harrowing near-death). Ending text is tier-aware.
- Synthesizer returns `meta.season_complete`, `meta.outcome`, `meta.climax_tier`.
- Verified by `test_full_arc_triumphant` (trust 31 → high → triumphant) and
  `test_climax_low_trust_dark` (trust 0 → low → narrow escape).

### Why this matters
- Converts the anthology into a **season with a payoff** → retention + a reason to finish all tales.
- Makes the **trust/memory system mechanically decisive**, not flavor — the strongest possible
  demo of "the AI character's relationship with you changes the outcome" ([00](00-research-and-market.md) §3.1).
- Gives a natural **season boundary** for monetization ([10](10-business-and-pitch.md)) and a clean hook into Phase 2.

---

## Encoding checklist (to add to `tales.py`, matching the Transposed Heads schema)
For each of tales 2–5: `canon_facts[]` (with correct `characters_present` for the leak guarantee),
`beats[]`, `mini_agents{}` (bible + `answer_intro` + `unknown`), `riddle`, `choices[]`,
`canonical`, `reactions{}`. Then add eval rows ([data/processed/eval](../data/processed/eval)) per tale, and a
`meta_arc` module for the trust-gated reveals + climax. The Transposed Heads in `tales.py` is the
reference implementation.
