# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Grade r217_probes.py's results against the behaviour R217 DEMANDED.

R217's own check_probes.py asserts the round-two counterexamples (a partial
restore reported done without failure); revision c must make every one of
them fail. This file asserts the demanded outcome instead, variant by
variant, and prints one line each. Exit 0 only if every line holds.
"""
import json
import os
import sys
from pathlib import Path

data = json.loads((Path(os.environ["PROBE_OUT"]) / "r217" / "probe-results.json").read_text())
by = {r["variant"]: r for r in data}
bad = 0


def verdict(name: str, ok: bool, detail: str) -> None:
    global bad
    bad += not ok
    print(f"{'HOLDS' if ok else 'FAILS'} R217 {name}: {detail}")


def rows_default(r: dict, tag: str = "terminal") -> bool:
    return all(row[3] == 0 for row in r["snaps"][tag]["rows"])


for r in data:
    verdict(f"{r['variant'] or 'first-pass'} completed", r["rc"] == 0 and r["completed"], f"rc {r['rc']}")
# the original payload faults: contained, as in round two
for v, rb in (("", 0), ("original-second-pass", 1)):
    o = by[v]["obs"]["restored"]
    verdict(f"original payload fault {v or 'first-pass'}",
            rows_default(by[v]) and o["restore_fail"] == 1 and o["d3_rb"] == rb,
            f"every row at its default {rows_default(by[v])}, restore fail {o['restore_fail']}, rolled back {o['d3_rb']}")
o = by["control"]["obs"]["observed"]
verdict("control", o["restore_done"] == 1 and o["restore_fail"] == 0 and o["entity_en"] == 1 and o["rs_app"] == 10,
        f"done {o['restore_done']} fail {o['restore_fail']} enabled {o['entity_en']} applied {o['rs_app']}")
# the header counterexamples: a failure verdict, complete defaults, never blank
for v in ("header-repeat", "header-balanced", "header-pass0"):
    o = by[v]["obs"]["observed"]
    verdict(v, rows_default(by[v]) and o["restore_done"] == 1 and o["restore_fail"] == 1 and o["d3_fail"] == 1
            and o["d3_cause"] == 2 and o["blank"] == 0 and o["entity_en"] == 1,
            f"every row at its default {rows_default(by[v])}, done {o['restore_done']} fail {o['restore_fail']} "
            f"(D3 {o['d3_fail']}, cause {o['d3_cause']}), blank {o['blank']}, applied {o['rs_app']}, enabled "
            f"{o['entity_en']}")
# the descriptor counterexamples
o = by["descriptor-error"]["obs"]["observed"]
verdict("descriptor-error", o["d3_closed"] == 1 and o["restore_done"] == 0 and o["entity_en"] == 0 and o["d3_cause"] == 6,
        f"closed {o['d3_closed']}, done {o['restore_done']}, enabled {o['entity_en']}, cause {o['d3_cause']} "
        f"(the memory still fails, so the roll-back cannot prove its image)")
o = by["descriptor-timeout"]["obs"]["observed"]
verdict("descriptor-timeout", rows_default(by["descriptor-timeout"]) and o["restore_done"] == 1
        and o["restore_fail"] == 1 and o["d3_rb"] == 1 and o["d3_cause"] == 6 and o["entity_en"] == 1,
        f"every row at its default {rows_default(by['descriptor-timeout'])}, done {o['restore_done']} fail "
        f"{o['restore_fail']}, rolled back {o['d3_rb']}, cause {o['d3_cause']}, enabled {o['entity_en']}")
o = by["descriptor-initial-error"]["obs"]["observed"]
verdict("descriptor-initial-error", o["d3_closed"] == 1 and o["restore_done"] == 0 and o["entity_en"] == 0
        and o["d3_cause"] == 7 and o["desc_valid"] == 0 and o["rs_app"] == 0 and o["rs_ref"] == 0,
        f"closed {o['d3_closed']}, done {o['restore_done']}, enabled {o['entity_en']}, cause {o['d3_cause']}, image "
        f"validated {o['desc_valid']}, applied {o['rs_app']} refused {o['rs_ref']}")
print(f"R217 PROBES: {len(data)} runs, {bad} not as demanded")
sys.exit(1 if bad else 0)
