"""Knowledge-isolation eval harness — turns the "leak-proof" claim into a NUMBER.

    python -m app.eval_leak        (from the backend/ directory)

Katha's core guarantee (docs/01 sec 4): an AI character can only surface facts it
WITNESSED. This is enforced structurally in the retrieval layer (rag/knowledge_state.py),
not by prompt politeness — so no model, however jailbroken, can leak a secret it was never
handed. This harness replays the adversarial probe set in
data/processed/eval/knowledge_leak.jsonl against the live engine.

Two distinct properties are measured and reported SEPARATELY, because they are different
kinds of claim:

  * LEAK-PROOFNESS (the security invariant, one-sided): a secret a character did not
    witness must NEVER be retrievable by it. A failure here is a *leak*. CI gates on this.
  * RECALL (a retrieval-quality metric): the rightful witness/teller SHOULD be able to
    retrieve the facts it is entitled to. A miss here is a quality issue, not a leak, and
    is reported but does not fail the run.

Exits non-zero only on a LEAK, so the green CI badge means exactly "0 information leaks".
"""
from __future__ import annotations

import json
import os
import sys

from .models import WorldEvent
from .rag.knowledge_state import engine as ks
from .store import store

EVAL_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "data", "processed", "eval", "knowledge_leak.jsonl"
)


def _load(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def main() -> int:
    print("=" * 78)
    print("KATHA -- Knowledge-Isolation Eval  (the \"witness gate\")")
    print("=" * 78)

    probes = _load(EVAL_PATH)

    # --- security invariant: secrets withheld from non-witnesses (gates CI) -----
    withhold_total = withhold_ok = 0
    leaks: list[str] = []
    # --- recall: rightful witness/teller can reach its entitled facts (reported) -
    recall_total = recall_ok = 0
    recall_misses: list[str] = []

    for p in probes:
        pid = p.get("id", "?")

        if p.get("type") == "world_event":
            sid = f"eval-{pid}"
            store.get(sid).events.clear()
            store.add_event(WorldEvent(
                id="e1", session_id=sid, scene_id="s", description="a witnessed event",
                known_to=p["event_known_to"], turn_no=1,
            ))
            retrieved = len(ks.witnessed_events(p["agent"], sid)) > 0
            if p["expect_retrieved"]:
                recall_total += 1
                recall_ok += retrieved
                if not retrieved:
                    recall_misses.append(f"{pid} (L2 event hidden from rightful witness {p['agent']})")
            else:
                withhold_total += 1
                blocked = not retrieved
                withhold_ok += blocked
                if not blocked:
                    leaks.append(f"{pid} (L2 LEAK: event visible to non-witness {p['agent']})")
            continue

        # L1 canon retrieval through the witness gate.
        ids = [r.id for r in ks.canon(p["agent"], p["query"], p["tale"])]

        if "forbidden_chunk" in p:
            withhold_total += 1
            withheld = p["forbidden_chunk"] not in ids
            withhold_ok += withheld
            if not withheld:
                leaks.append(f"{pid} (L1 LEAK: {p['agent']} retrieved forbidden {p['forbidden_chunk']})")

        if "required_chunk" in p:
            recall_total += 1
            present = p["required_chunk"] in ids
            recall_ok += present
            if not present:
                recall_misses.append(f"{pid} (recall miss: {p['agent']} -> {p['required_chunk']})")

    leak_count = len(leaks)

    print(f"\n  LEAK-PROOFNESS (security invariant -- gates this run)")
    print(f"    forbidden facts withheld from non-witnesses : {withhold_ok}/{withhold_total}")
    print(f"    information leaks                           : {leak_count}")
    print(f"\n  RECALL (retrieval quality -- reported, non-gating)")
    print(f"    entitled facts reachable by witness/teller  : {recall_ok}/{recall_total}")
    if recall_misses:
        for m in recall_misses:
            print(f"      - {m}")

    print("  " + "-" * 56)
    if leak_count == 0:
        print(f"  RESULT: {withhold_ok}/{withhold_total} secrets withheld across the probe set -- "
              f"0 leaks. Leak-proof by construction. [OK]")
        print("=" * 78)
        return 0

    print(f"  RESULT: {leak_count} LEAK(S) —")
    for x in leaks:
        print(f"    - {x}")
    print("=" * 78)
    return 1


if __name__ == "__main__":
    sys.exit(main())
