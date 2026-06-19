# Katha — Technical Architecture

> Companion to [HANDOFF.md](../HANDOFF.md) and [00-research-and-market.md](00-research-and-market.md).
> This is the system-design source of truth: the agent graph, the 3-layer RAG, the
> knowledge-state engine (Katha's core IP), data schema, and the cost/latency budget.
>
> **Design vs. built.** This doc describes the *target* architecture (content-agnostic, multi-NPC,
> Postgres / Pinecone / Sarvam, LangGraph 1.x). The current Phase-1 build implements the same
> *shapes* with simpler free/local pieces: single-speaker Vikram aur Betaal; **real LangGraph** or
> a stdlib runner; in-memory + **SQLite**; **Ollama** LLM + embeddings (lexical fallback). The
> `TurnState` here is shown multi-NPC (`active_npc_ids`); the Phase-1 code uses a single-speaker
> dataclass. For exactly what's built today, see **[STATUS.md](STATUS.md)**.

---

## 0. Design principles

1. **Knowledge asymmetry is the product.** The hard, defensible thing is that each NPC
   knows *only what they witnessed*. Every design choice serves correctness of that.
2. **Determinism where it matters, generation where it delights.** Canon facts, who-knows-what,
   and dharma scoring are deterministic/stored. Dialogue *phrasing* is generated.
3. **Provider-swappable.** No hard dependency on one LLM vendor; the LLM is an interface.
4. **Grounded, never freelancing.** NPCs answer from retrieved canon + memory, not vibes.
   Ungrounded claims about the epic are a defect, not creativity.
5. **Fail reverent, fail safe.** On any moderation/uncertainty failure, degrade to a
   pre-written in-character line, never to "I'm an AI" or to an unverified claim.

---

## 1. High-level system

```
┌────────────────────────────────────────────────────────────────────┐
│  React Native + Expo app (visual novel client)                     │
│  scene bg · portrait · dialogue panel (typewriter) · voice toggle  │
└───────────────┬───────────────────────────────▲────────────────────┘
                │ POST /turn (text or audio)     │ scene + line + audio
                ▼                                 │
┌────────────────────────────────────────────────────────────────────┐
│  FastAPI gateway                                                    │
│  auth(device) · rate-limit · STT(Sarvam) · TTS(Sarvam) · stream    │
└───────────────┬────────────────────────────────────────────────────┘
                │ TurnRequest
                ▼
┌────────────────────────────────────────────────────────────────────┐
│  LangGraph turn graph (the orchestrator)                           │
│                                                                     │
│   Input Moderation ──► Narrator (router) ──► [active NPC nodes ∥]   │
│        │                     │                      │               │
│        └─ reject ◄───────────┘            World-State Updater       │
│                                                     │               │
│                              Output Validator ◄── Synthesizer       │
└───────────────┬────────────────────────────────────────────────────┘
                │ reads/writes
                ▼
┌──────────────┬──────────────┬──────────────┬──────────────────────┐
│ Postgres     │ Vector DB     │ Knowledge-   │ Asset/CDN            │
│ (game state) │ (3-layer RAG) │ State engine │ (bg, portraits, sfx) │
└──────────────┴──────────────┴──────────────┴──────────────────────┘
```

A **turn** = one player utterance → one or more NPC responses + world updates + scene state.

---

## 2. The LangGraph turn graph

LangGraph 1.0 gives native state persistence (checkpointer), conditional edges, and
parallel fan-out — exactly the primitives we need.

### 2.1 Shared graph state (`TurnState`)
A single typed object threaded through all nodes:

```python
class TurnState(TypedDict):
    session_id: str
    player_input: str            # post-STT text
    language: str                # 'hi' | 'en' | 'hinglish'
    scene_id: str
    active_npc_ids: list[str]    # decided by narrator
    moderation: ModerationResult # verdict + reason + strike delta
    retrievals: dict[str, list]  # per-npc retrieved canon + memory + events
    npc_drafts: dict[str, NpcDraft]   # per-npc generated line (pre-validation)
    world_updates: list[WorldEvent]   # events to persist, with known_to[]
    dharma_delta: int
    final_render: SceneRender    # what the client paints + speaks
    fallback_used: bool
```

### 2.2 Nodes

1. **Input Moderation** (deterministic + classifier) — see [07-moderation-and-safety.md](07-moderation-and-safety.md).
   Verdict ∈ {allow, deflect, block}. On `block`/`deflect`, short-circuit to an
   in-character deflection and skip generation.

2. **Narrator / Router** (LLM, low temperature) — the orchestrator. Inputs: scene,
   recent transcript summary, player input. Outputs (structured):
   - `active_npc_ids` — who, in this scene, would respond (often 1; sometimes 2–3 in a group scene).
   - `scene_directions` — beat/pacing notes, ambient cue, whether to advance the arc.
   - `addressed_to` — which NPC the player is speaking to (disambiguation).
   The narrator never speaks *as* an NPC; it decides structure. It also owns scene/arc
   transitions and "stage directions" (a character entering/leaving).

3. **NPC nodes (parallel fan-out)** — one node per active NPC. Each node:
   - Builds its **retrieval context** via the Knowledge-State engine (§4): canon (Layer 1)
     filtered to what this NPC may reference, this NPC's witnessed events (Layer 2),
     and this NPC's personal memories of the player (Layer 3).
   - Generates a candidate line conditioned on: character bible/system prompt
     ([03-npc-prompts.md](03-npc-prompts.md)) + retrievals + relationship/trust + dharma context.
   - Returns a `NpcDraft` (line + expression tag {neutral|intense|emotional} + optional
     trust/relationship delta + "memory to store").
   NPC nodes are **independent** — Karna's node cannot see Krishna's retrievals. This is
   enforced at the data layer, not by prompt politeness.

4. **World-State Updater** — converts what just happened into `WorldEvent`s, each tagged
   with `known_to[]` = NPCs physically present/aware. Computes `dharma_delta` from any
   player choice. Writes events (Layer 2) and updates relationships/knowledge_states.

5. **Output Validator** — re-checks each NPC draft for canon-consistency and content
   safety (§ moderation layer 3). On failure: one regeneration attempt, then a curated
   fallback line. Sets `fallback_used` for telemetry.

6. **Synthesizer** — orders multi-NPC lines into a coherent beat, attaches scene render
   (background, active portrait + expression, ambient sfx), and returns `SceneRender`.
   TTS is invoked here (or streamed from the gateway) per-line with the character's voice profile.

### 2.3 Routing logic (edges)
- `Moderation.block` → Deflection node → Synthesizer (skip everything else).
- `Narrator` → conditional fan-out to N NPC nodes (parallel) → join.
- Join → World-State Updater → Output Validator → Synthesizer → END.
- Checkpoint after World-State Updater so a failed render can resume without re-spending LLM calls.

---

## 3. The 3-layer RAG (detailed)

| Layer | Scope | Write time | Read time | Store |
|---|---|---|---|---|
| **L1 Mythology** | Global canon (Ganguli corpus) | One-time, offline | Per NPC turn, filtered | Vector DB collection `canon` |
| **L2 World State** | Per session | After every turn | Per NPC, filtered by `known_to` | `world_events` (Postgres + vector) |
| **L3 Personal Memory** | Per NPC per session | After every turn (summarized) | Per NPC, top-k of *that* NPC | `npc_memory` (Postgres + vector) |

### 3.1 Layer 1 — Mythology canon
- Source & chunking strategy live in [02-data-pipeline.md](02-data-pipeline.md). Key point for
  architecture: chunks carry metadata `{parva, chapter, speaker, characters_present, scene_id,
  themes[]}` so retrieval can be filtered (e.g. "Karna may only *cite* canon consistent with
  what his character would know," enforced via metadata + the knowledge-state filter).
- Retrieval: hybrid (dense embeddings + keyword/BM25) — mythology has many proper nouns
  that pure-vector search fumbles. Re-rank top-N to top-k (k≈4–6).

### 3.2 Layer 2 — World state (the asymmetry layer)
- Every `WorldEvent` = `{id, session_id, scene_id, description, embedding, known_to[], turn_no, dharma_relevant}`.
- **`known_to[]` is the crux.** Populated by the World-State Updater from scene presence:
  who was in the room, who was told later, who Krishna (omniscient) may know by narrative
  fiat. A reveal event (e.g. "Kunti tells Karna he is her son") *adds* `karna` to that
  fact's audience and may spawn downstream knowledge changes.
- NPC retrieval over L2 is **always** filtered `WHERE :npc_id = ANY(known_to)`. An NPC can
  never retrieve an event it didn't witness. This is what creates authentic dramatic irony.

### 3.3 Layer 3 — Personal memory
- After each turn, summarize the exchange from that NPC's POV (1–3 sentences, emotionally
  salient), embed, store with `{npc_id, session_id, memory_text, embedding, turn_no, salience}`.
- On the next encounter, retrieve top-k memories for `(npc_id, session_id)` — and optionally
  cross-session if we want NPCs to remember the player across arcs (V1+ feature; gate behind a flag).
- Memory is **isolated per NPC**: Draupadi's memories are never in Arjuna's retrieval set.

### 3.4 Why three layers, not one
Collapsing them loses the asymmetry guarantee. Separation lets us *prove* (in tests) that
an NPC cannot leak unwitnessed facts — the property that makes Katha feel alive. See the
"knowledge-leak test" in [09-build-plan.md](09-build-plan.md).

---

## 4. The Knowledge-State engine (core IP)

A thin service that, given `(npc_id, session_id, scene_id)`, returns the **bounded context**
an NPC is allowed to reason over:

```
context(npc) =
   L1 canon chunks         filtered by metadata compatible with npc's canonical knowledge
 + L2 world events         WHERE npc ∈ known_to
 + L3 personal memories    WHERE npc_id = npc
 + relationship/trust      (player↔npc)
 + dharma context          (recent morally-relevant choices npc is aware of)
 + character bible         (static system prompt)
```

- **Canonical baseline:** each NPC has a baseline of canon they "always knew" (Karna knows
  he was raised by Adhiratha; he does *not* know Kunti is his mother until revealed). Modeled
  as `knowledge_states.known_event_ids[]` seeded at session start from a per-entry-point template.
- **Reveals mutate state, not prompts.** When canon is revealed in-story, we append event ids
  to the NPC's `known_event_ids` and add them to `known_to[]`. The next turn, the NPC *can*
  reason about it. No prompt editing, fully auditable.
- **Krishna special case:** omniscient by canon. His baseline includes (nearly) all events,
  but his system prompt governs *what he chooses to reveal*. Implement as: Krishna's retrieval
  is unfiltered, but a "discretion" instruction + a `revealed_to_player[]` ledger prevent him
  from dumping spoilers. (See [03-npc-prompts.md](03-npc-prompts.md) → Krishna.)

This engine is the thing to demo to investors: "watch Karna *not* know who his mother is, then
watch the reveal change his behavior — deterministically, on replay."

---

## 5. Data schema (Postgres)

Extends HANDOFF's table list with fields the engine needs.

```sql
players(            id, device_id, language, dharma_score, strike_count, created_at )
sessions(          id, player_id, entry_point, current_scene_id, chapter, arc_state, created_at )
world_events(      id, session_id, scene_id, description, embedding_ref,
                   known_to TEXT[], turn_no, dharma_relevant BOOL, created_at )
npc_memory(        id, npc_id, session_id, memory_text, embedding_ref, salience, turn_no )
relationships(     session_id, npc_id, trust_score INT CHECK(-100..100), updated_at )
dharma_log(        id, session_id, choice_description, dharma_delta, npc_context, turn_no )
knowledge_states(  session_id, npc_id, known_event_ids TEXT[], updated_at )
scenes(            id, entry_point, title, background_asset, ambient_sfx, present_npc_ids TEXT[] )
turns(             id, session_id, turn_no, player_input_hash, summary, fallback_used, latency_ms )
```

Notes:
- We store **summaries/hashes**, not verbatim player text (privacy + DPDP; see [08-legal-and-compliance.md](08-legal-and-compliance.md)).
- `embedding_ref` points into the vector DB; Postgres holds structured truth, vector DB holds similarity index.
- Dev: SQLite + ChromaDB. Prod: Postgres (+ pgvector optional) + Pinecone.

---

## 6. Voice pipeline (Sarvam AI)

```
mic ─► [client VAD] ─► /turn(audio) ─► Saarika STT ─► language detect ─► graph
graph ─► line text ─► Bulbul v3 TTS (character voice profile) ─► streamed audio ─► client
```

- **Per-character voice profiles:** map each NPC → a Bulbul voice + pitch/pace style so
  Karna sounds grave, Draupadi sharp, Krishna warm. Cache TTS per `(line_hash, voice)` to
  cut cost and latency on repeated/fallback lines.
- **Hinglish & code-switching:** Saarika handles Hindi/Hinglish/English; narrator stores
  `language` so the whole turn stays in the player's register.
- **Latency:** TTS is the long pole. Stream first sentence's audio while later sentences
  generate; show typewriter text immediately so perceived latency ≈ time-to-first-token.

---

## 7. Cost & latency budget (the question every investor asks)

A fan-out turn is several LLM calls + vector queries + moderation + TTS. We must design to
a budget, not discover it in the bill.

### 7.1 Per-turn cost model (single-NPC turn, order-of-magnitude)
| Component | Calls | Note |
|---|---|---|
| Input moderation | 1 cheap classifier | small model / rules-first |
| Narrator route | 1 LLM (low temp, short) | structured output |
| NPC generation | 1 LLM per active NPC | the main cost |
| Memory summarize | 1 cheap LLM | can batch/async after response |
| Output validate | 1 cheap classifier | rules-first, LLM only on suspicion |
| Embeddings | 2–4 | event + memory + query |
| Vector queries | 3 | L1 + L2 + L3 |
| STT + TTS | per audio | Sarvam: STT ₹30/hr, TTS ₹15–30/10K chars |

**Cost levers (designed in, not bolted on):**
- Tiered models: frontier model only for narrator + NPC generation; cheap/small models for
  moderation, routing fallback, summarization.
- Aggressive caching: TTS per line-hash; canon retrieval per `(scene, npc)`; fallback lines pre-rendered.
- Async the non-blocking work (memory write, embeddings) *after* the response ships.
- Optional **LoRA Llama 3.1 8B** for NPC generation later — self-hosted to collapse the
  dominant per-turn LLM cost once volume justifies GPU spend.

### 7.2 Latency budget (target: < ~2.5s to first spoken word)
| Stage | Target |
|---|---|
| STT (if audio) | ~300–500 ms |
| Moderation + route | ~300 ms (small models, parallel where possible) |
| NPC generation (stream) | first token ~500–800 ms |
| TTS first sentence | ~400–700 ms |
| **Perceived total** | typewriter starts < 1.5 s; voice < 2.5 s |
World updates, memory write, embeddings run **after** the response is shown.

### 7.3 Unit economics sanity (for the deck)
Build the real number bottom-up once models are picked, then show: avg turns/session ×
cost/turn → cost/session → vs ARPU (₹99/mo or ₹299/arc). Target gross margin and the
LoRA-breakeven volume. Placeholder framework in [10-business-and-pitch.md](10-business-and-pitch.md).

---

## 8. Failure modes & guarantees

| Failure | Guarantee / handling |
|---|---|
| LLM returns canon-inconsistent claim | Output Validator catches → 1 regen → curated fallback line |
| Moderation false-positive on a benign line | Deflect in character; never break the fourth wall |
| NPC about to leak unwitnessed fact | Impossible by construction (L2 `known_to` filter); covered by automated leak tests |
| LLM/vendor outage | Provider-swap interface; cached fallback lines keep the scene playable |
| TTS slow/unavailable | Text-only mode; voice toggles off gracefully |
| Cost spike | Per-session turn cap + degrade to cheaper model tier |

---

## 9. Observability
- Trace every turn (LangGraph checkpoints + structured logs): which NPCs fired, retrieval
  hits, moderation verdicts, `fallback_used`, latency per stage, token spend.
- **Fidelity metrics:** canon-consistency pass rate, leak-test pass rate, fallback rate.
- **Engagement metrics:** turns/session, session length, day-1/7/30 retention, voice usage %.
These feed both the build (quality gates) and the pitch (the retention story).

---

## 10. Open architecture decisions
1. **Narrator LLM** — Gemini vs alternative long-context model. Keep behind an interface; benchmark on routing accuracy + cost.
2. **pgvector vs Pinecone in prod** — pgvector simplifies ops at small scale; revisit at volume.
3. **Cross-session memory** — do NPCs remember the player across arcs? Strong retention hook; gate behind a flag and a privacy review.
4. **When to fine-tune** — define the volume/cost trigger for the LoRA NPC model (see §7.1).
