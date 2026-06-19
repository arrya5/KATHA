# Katha — Data Pipeline & Source-Text Strategy

> Companion to [01-architecture.md](01-architecture.md) (Layer-1 canon) and
> [04-cultural-fidelity.md](04-cultural-fidelity.md). This doc decides *which* Mahabharata Katha is
> grounded in, how the text becomes retrievable chunks, and how we keep it both legally
> clean and scholarly defensible.

---

## 1. The sourcing problem (and the decision)

There is no single "the Mahabharata." For a world-class, defensible product we must be
explicit about which text we ground on and why.

| Edition | What it is | License | Scholarly standing |
|---|---|---|---|
| **Kisari Mohan Ganguli** (1883–96) | First complete English prose translation; follows the Northern recension / Vulgate (Neelkantha commentary) | **Public domain** | Foundational, but pre-critical; archaic English |
| **BORI Critical Edition** (Pune) | Reconstructed text from 1,259 manuscripts over ~5 decades; reconciles N & S recensions | Sanskrit text is the scholarly standard; the *edition* is a BORI work | **Gold standard** |
| **Bibek Debroy** (10-vol) | Modern English translation *of* the BORI critical edition | **Copyrighted** (Penguin) | Best modern English; cannot be redistributed/embedded |
| **M. N. Dutt** (1895–1905) | Another complete early English translation | Public domain | Secondary check |

### 1.1 Decision (recommended)
1. **Ground the retrievable corpus (Layer 1) on Ganguli.** It is the only *complete*
   public-domain English text — we can legally chunk, embed, store, and quote it.
2. **Use the BORI Critical Edition as the canonical *spine*.** Its parva/sub-parva/chapter
   structure and its judgments on what is core vs. interpolation are *facts/scholarship*,
   usable as a reference layer (we cite structure; we don't copy Debroy's prose).
3. **Use Debroy + Dutt as human reference only** for the team/advisors to resolve
   ambiguities — **never** ingested or quoted in the product.
4. **Sanskrit anchor terms** (names, epithets, key shlokas already in public domain like the
   Gita within the Bhishma Parva) may be surfaced for flavor with transliteration + meaning.

> **Why this matters for the pitch and for fidelity:** "We ground on the public-domain
> Ganguli text, structured against the BORI critical edition, reviewed by Sanskrit-literate
> advisors" is a sentence that survives both a lawyer and a scholar. "We scraped some
> Mahabharata summaries" does not. See [04-cultural-fidelity.md](04-cultural-fidelity.md).

### 1.2 Provenance & licensing hygiene
- Record source, edition, archive URL, and retrieval date for every ingested file in
  `data/raw/SOURCES.md`. Ganguli is public domain; still document it.
- Keep a clear wall: redistributed corpus = Ganguli (+ Dutt if needed) only. Copyrighted
  translations live *outside* the repo, in the team's reference shelf.

---

## 2. Acquisition

- **Primary:** Ganguli translation, full text — archive.org
  (`archive.org/details/TheMahabharataOfKrishna-dwaipayanaVyasa`) and the
  sacred-texts.com HTML as a cross-check for OCR errors.
- Download into `data/raw/ganguli/` as one file per parva (18 parvas).
- **Validate** against a known table of contents (18 parvas, expected chapter counts) so we
  catch missing/duplicated sections before chunking.

---

## 3. The chunking strategy (this is where most projects fail)

Naive fixed-size or sentence splitting destroys mythological text: a single moral exchange
or a speaker's turn breaks across chunks, and retrieval returns half a thought. Katha chunks
**by dramatic unit**.

### 3.1 Unit of chunking = *speaker turn within a scene*
A chunk is one continuous utterance/narration unit, bounded by speaker change or scene shift,
with a soft cap (~512–1,024 tokens) and overlap only *within* a scene (never across scenes).

### 3.2 Pipeline
```
raw parva text
  └─► structural parse        → parva / chapter (section) boundaries
        └─► dialogue parse     → detect "X said:" / narration spans  (Ganguli marks speakers)
              └─► scene tagging → group consecutive turns sharing setting/participants
                    └─► chunk   → 1 chunk per speaker-turn (or coherent narration span)
                          └─► metadata enrich
                                └─► embed + index (canon collection)
```

### 3.3 Metadata schema per chunk
```json
{
  "chunk_id": "udyoga.142.karna.003",
  "parva": "Udyoga Parva",
  "parva_no": 5,
  "chapter": 142,
  "scene_id": "kunti-approaches-karna",
  "speaker": "Karna",
  "characters_present": ["Karna", "Kunti", "Surya"],
  "addressed_to": ["Kunti"],
  "themes": ["identity", "loyalty", "dharma", "fate"],
  "text": "....",
  "source": "Ganguli",
  "bori_ref": "5.144 (crit. ed.)",
  "is_dialogue": true
}
```
- `characters_present` and `scene_id` feed the **knowledge-state engine** ([01-architecture.md](01-architecture.md) §4):
  they let us seed who-knew-what baselines and filter what an NPC may cite.
- `themes[]` enables thematic retrieval ("what does Karna say about loyalty?") beyond keyword.
- `bori_ref` is the critical-edition cross-reference (structure only).

### 3.4 Extraction approach
- Ganguli reliably marks speakers ("Vaisampayana said", "Karna said"). Parse these with
  rules first; use an LLM pass only to (a) tag `scene_id`/`characters_present`/`themes`
  where rules are ambiguous, and (b) flag suspected interpolations vs BORI core.
- Every LLM-enriched field is **spot-checked by a human/advisor** for the MVP scenes
  (Night Before Kurukshetra and the V1 entry points) — small enough to fully audit.

---

## 4. Embedding & indexing

- **Embedding model:** choose a model strong on (a) proper nouns and (b) optionally
  multilingual (so Hindi queries hit English canon). Candidates: a current multilingual
  embedding model; benchmark recall on a hand-built Mahabharata Q→chunk eval set before committing.
- **Hybrid retrieval:** dense + BM25/keyword, then re-rank — mythology is proper-noun heavy
  and pure-vector misses exact names/epithets.
- **Collections:** `canon` (L1, static), `world_events` (L2, per session), `npc_memory`
  (L3, per NPC/session). Dev: ChromaDB. Prod: Pinecone (or pgvector at small scale).
- **Versioning:** stamp the corpus with `corpus_version` so retrieval quality regressions
  are attributable to a re-chunk/re-embed.

---

## 5. Retrieval contract (what the agents get)

For an NPC turn, the knowledge-state engine asks for:
```
canon:    top-k from `canon` filtered by metadata the NPC may know (scene/character compatible)
events:   from `world_events` WHERE npc ∈ known_to AND session_id = :sid
memory:   from `npc_memory`  WHERE npc_id = :npc AND session_id = :sid
```
k≈4–6 canon, top-5 memories, all witnessed events relevant to the query. Token-budgeted so
the prompt stays within latency/cost targets ([01-architecture.md](01-architecture.md) §7).

---

## 6. Evaluation sets (build these early — they are quality gates)

1. **Retrieval eval** — ~100 hand-written `(question → expected chunk(s))` pairs across the
   MVP scenes. Track recall@k; gate corpus changes on it.
2. **Canon-consistency eval** — assertions of fact ("Karna does NOT know Kunti is his
   mother before the Udyoga reveal") the system must respect.
3. **Knowledge-leak eval** — adversarial prompts trying to make an NPC reveal an unwitnessed
   fact; must pass 100% (it's a structural guarantee — see [01-architecture.md](01-architecture.md) §3.4).
4. **Fidelity eval** — advisor-reviewed: does the retrieved+generated answer match canon and
   tone? ([04-cultural-fidelity.md](04-cultural-fidelity.md))

---

## 7. Directory layout
```
data/
├── raw/
│   ├── SOURCES.md            ← provenance, license, retrieval dates
│   └── ganguli/              ← 18 parva text files (public domain)
├── processed/
│   ├── chunks.jsonl          ← chunk text + metadata
│   ├── corpus_version.json   ← version stamp + counts
│   └── eval/                 ← retrieval / consistency / leak eval sets
└── (embeddings live in the vector DB, referenced by chunk_id)
```

---

## 8. Open decisions
1. **Embedding model** — multilingual vs English-only + translate-query; decide on eval recall.
2. **Interpolation policy** — do we exclude passages BORI marks as late interpolations, or
   keep+flag them? (Affects which "facts" NPCs treat as canon.) Default: keep + flag, prefer core.
3. **Scope of corpus for MVP** — ingest only the parvas covering the MVP/V1 entry points first
   (Udyoga, Bhishma, Sabha) for a tight, fully-audited corpus; expand later.
