# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Grade r218_probe_headers.py's results against the behaviour R218 DEMANDED:
a header transport error, in either pass or both, ends with a failure
verdict and complete defaults (never a partial restore reported done), and
the original payload and timeout triggers keep rolling back. One line per
run; exit 0 only if every line holds.
"""
import json
import os
import sys
from pathlib import Path

data = json.loads((Path(os.environ["PROBE_OUT"]) / "r218" / "probes" / "results.json").read_text())
by = {r["variant"]: r for r in data}
bad = 0


def verdict(name: str, ok: bool, detail: str) -> None:
    global bad
    bad += not ok
    print(f"{'HOLDS' if ok else 'FAILS'} R218 {name}: {detail}")


def contained(r: dict, rb: int, causes: tuple) -> tuple:
    t, b = r["terminal"] or {}, r["boot"]
    ok = (r["rc"] == 0 and r["done"] and not r["mismatches_defaults"] and t.get("d3_done") == 1
          and t.get("d3_fail") == 1 and t.get("d3_rb") == rb and t.get("restore_fail") == 1 and t.get("blank") == 0
          and b.get("cause") in causes and b.get("enable", 0) >= b.get("terminal", 1) > 0)
    return ok, (f"{len(r['mismatches_defaults'])} records off their defaults, D3 done {t.get('d3_done')} fail "
                f"{t.get('d3_fail')} rolled back {t.get('d3_rb')}, restore fail {t.get('restore_fail')} blank "
                f"{t.get('blank')}, cause {b.get('cause')}, terminal {b.get('terminal')} enable {b.get('enable')}")


# pass 0 meets the device error first: nothing applied, defaults, not rolled back
for v in ("pass0", "repeat", "swap"):
    verdict(f"V18 {v}", *contained(by[v], 0, (2,)))
# pass 1 only: records applied, then rolled back
verdict("V18 pass1", *contained(by["pass1"], 1, (2,)))
# the round-one triggers: a payload read failing after an application, and a
# read 3,100,000 cycles late after an application
verdict("original F1 trigger (V11b)", *contained(by["R218_ORIGINAL_F1"], 1, (2,)))
verdict("original F2 trigger (W12)", *contained(by["R218_ORIGINAL_F2"], 1, (3,)))
print(f"R218 PROBES: {len(data)} runs, {bad} not as demanded")
sys.exit(1 if bad else 0)
