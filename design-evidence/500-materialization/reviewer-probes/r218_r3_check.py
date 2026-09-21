# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Grade r218_r3_probe_stage1.py against what R218 R3-F1 DEMANDED: stage 1's
own roll-back scope recovers the finite descriptor delays to proven DEFAULTS
with the entity enabled, and removing the stage-1 recovery mechanism fails
its own completed scenario (CLOSED), while the one-error control recovers
either way.

Exit 0 only if every line reads HOLDS.
"""
import json
import os
from pathlib import Path
import sys

rows = json.loads((Path(os.environ["PROBE_OUT"]) / "r218r3" / "stage1-probe.json").read_text())
bad = 0


def say(ok: bool, text: str) -> None:
    global bad
    bad += not ok
    print(f"{'HOLDS' if ok else 'DOES NOT HOLD'} R218 r3 {text}")


def defaults(r: dict) -> bool:
    return (r["rc"] == 0 and r["done"] and (r["d3_done"], r["d3_fail"], r["d3_rb"], r["d3_closed"], r["own"])
            == (1, 1, 1, 0, 0) and r["enable"] and r["enable"] >= r["terminal"] and not r["mismatches"])


def closed(r: dict) -> bool:
    return (r["rc"] == 0 and r["done"] and (r["d3_done"], r["d3_fail"], r["d3_rb"], r["d3_closed"], r["own"])
            == (0, 1, 0, 1, 1) and not r["enable"] and not r["mismatches"])


say(len(rows) == 12, f"{len(rows)} runs (3 cases x 4 builds)")
for r in rows:
    late = r["case"] != "V20b_desc_error_once_after_apply"
    scope = r["build"] in ("base-1x1", "base-1x1-stage1")
    want = "DEFAULTS" if (scope or not late) else "CLOSED"
    ok = defaults(r) if want == "DEFAULTS" else closed(r)
    if ok and want == "DEFAULTS" and late:
        #! the owners left reset only after the late burst: the guard's debt
        #! survived the roll-back's own reset
        ok = 0 < r["accepted"] < r["abort"] < r["late_beat"] < r["rb_end"]
    say(ok, f"{r['build']} {r['case']}: want {want}; done/fail/rolled back/closed/own "
            f"{r['d3_done']}/{r['d3_fail']}/{r['d3_rb']}/{r['d3_closed']}/{r['own']}, terminal {r['terminal']}, "
            f"enable {r['enable']}, request {r['accepted']}, abort {r['abort']}, late beat {r['late_beat']}, "
            f"owners out of reset {r['rb_end']}, {len(r['mismatches'])} records off their defaults")
print(f"R218 r3 PROBES: {len(rows)} runs, {bad} not as demanded")
sys.exit(1 if bad else 0)
