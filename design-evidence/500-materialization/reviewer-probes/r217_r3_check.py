# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Grade r217_r3_probe_preload.py's two result files against what R217 R3-F1
DEMANDED: bounded manager recovery and usable GET service under finite and
persistent listener interference, with the descriptor-boundary observations
the reviewer recorded as safe unchanged. The reviewer's own
assert_review_observations.py asserts the COUNTEREXAMPLE instead; this file
requires it to hold only where the admission gate is deleted.

Exit 0 only if every line reads HOLDS.
"""
import json
import os
from pathlib import Path
import sys

base = Path(os.environ["PROBE_OUT"]) / "r217r3"
sets = {k: {row["variant"]: row for row in json.loads((base / f"adjacent-probes-{k}.json").read_text())}
        for k in ("gate", "gate-deleted")}
bad = 0


def say(ok: bool, text: str) -> None:
    global bad
    bad += not ok
    print(f"{'HOLDS' if ok else 'DOES NOT HOLD'} R217 r3 {text}")


def boot(k: str, v: str) -> dict:
    return next((e for e in sets[k][v]["events"] if e.get("k") == "boot"), {})


def answers(k: str, v: str) -> dict:
    return {e["tag"]: int(e["v"], 16) for e in sets[k][v]["events"] if e.get("k") == "ans"}


def lt(k: str, v: str, what: str) -> dict:
    return next((e for e in sets[k][v]["events"] if e.get("k") == "lt" and e.get("what") == what),
                {"n": 0, "first": [], "last": 0})


for k in sets:
    say(len(sets[k]) == 10 and all(r["rc"] == 0 and r["done"] for r in sets[k].values()),
        f"{k}: ten scenarios completed")
g = "gate"
ctl = boot(g, "control")
for v in ("control", "held", "finite"):
    t, b, a = sets[g][v]["obs"].get("terminal", {}), boot(g, v), answers(g, v)
    ok = (t.get("restore_done") == 1 and t.get("restore_fail") == 0 and t.get("entity_en") == 1
          and a.get("post.ptof0.value") == 1500000 and a.get("post.ptof0.valid") == 1
          and b.get("bind_end", 0) > 0 and abs(b.get("bind_end", 0) - ctl.get("bind_end", 0)) <= 10
          and abs(b.get("terminal", 0) - ctl.get("terminal", 0)) <= 10)
    say(ok, f"gate {v}: binding walk ends at {b.get('bind_end')} (control {ctl.get('bind_end')}), D3 terminal "
            f"{b.get('terminal')} (control {ctl.get('terminal')}), enable {b.get('enable')}, GET "
            f"({a.get('post.ptof0.value')}, {a.get('post.ptof0.valid')})")
tk_h, tk_f = lt(g, "held", "tk_take"), lt(g, "finite", "tk_take")
say(tk_h["n"] > 0 and tk_h["first"][0] >= boot(g, "held").get("bind_end", 1 << 40),
    f"gate held: the level presented from reset was first taken at {tk_h['first'][:1]}, after the release "
    f"{boot(g, 'held').get('bind_end')}, {tk_h['n']} times")
say(tk_f["n"] > 0 and 100000 <= tk_f["last"] <= 100010,
    f"gate finite: the level taken {tk_f['n']} times, the last at {tk_f['last']} (released at 100000)")
for v in ("4094",):
    t = sets[g][v]["obs"].get("terminal", {})
    say(t.get("restore_done") == 1 and t.get("restore_fail") == 0 and t.get("entity_en") == 1,
        f"gate {v}: the descriptor response inside the store's watchdog completes")
for v in ("4095", "4096", "4097"):
    t, a = sets[g][v]["obs"].get("terminal", {}), answers(g, v)
    say(t.get("restore_done") == 1 and t.get("restore_fail") == 1 and t.get("d3_rb") == 1 and t.get("d3_cause") == 6
        and t.get("entity_en") == 1 and a.get("rec.ptof0.value") == 0 and a.get("rec.ptof0.valid") == 0,
        f"gate {v}: rolled back to defaults (cause {t.get('d3_cause')}), enabled, GET (0, 0)")
for v in ("24090", "24098", "24100"):
    t, a = sets[g][v]["obs"].get("terminal", {}), answers(g, v)
    say(t.get("restore_done") == 0 and t.get("restore_fail") == 1 and t.get("d3_closed") == 1
        and t.get("d3_cause") == 6 and t.get("own") == 1 and t.get("entity_en") == 0 and not a,
        f"gate {v}: burst debt past the roll-back deadline stays CLOSED")
d = "gate-deleted"
t, a = sets[d]["held"]["obs"].get("terminal", {}), answers(d, "held")
say(all(t.get(key) == 0 for key in ("mgr_done", "restore_done", "restore_fail", "d3_closed", "entity_en", "port_busy"))
    and t.get("own") == 1 and not a,
    "gate deleted, held: the counterexample comes back (neither walk ends, no failure, no CLOSED, port idle, "
    "ownership kept, no GET answer)")
b = boot(d, "finite")
say(sets[d]["finite"]["obs"].get("terminal", {}).get("restore_done") == 1 and b.get("bind_end", 0) >= 100000,
    f"gate deleted, finite: the binding walk ends only after the release, at {b.get('bind_end')}")
print(f"R217 r3 PROBES: {sum(len(v) for v in sets.values())} runs, {bad} not as demanded")
sys.exit(1 if bad else 0)
