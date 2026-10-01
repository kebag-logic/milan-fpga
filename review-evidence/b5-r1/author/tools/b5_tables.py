#!/usr/bin/env python3
"""Packet summary and page tables for lane B5 from grade_a.py output.

usage: b5_tables.py <grade-full.json> <summary_dir>

Writes <summary_dir>/summary.json (the grade without the per-event list),
<summary_dir>/continuity-events.csv (one row per discontinuity, with the frame's
position in content time) and <summary_dir>/tables.md (the page tables).
"""
import csv
import json
import sys
from pathlib import Path

import numpy as np

g = json.load(open(sys.argv[1]))
out = Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
c = g["continuity"]
ev = c["events"]

# content position of each event: cumulative ordinal advance from the window start
pos = 0
prev = c["window"][0]
rows = []
for x in ev:
    rows.append(dict(frame=x["frame"], kind=x["kind"], step=x["step"], frames=x["frames"]))
with open(out / "continuity-events.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["frame", "kind", "step", "frames"])
    w.writeheader()
    w.writerows(rows)

summ = dict(g)
summ["continuity"] = {k: v for k, v in c.items() if k != "events"}
json.dump(summ, open(out / "summary.json", "w"), indent=1)

sk = [x for x in ev if x["kind"] == "skip"]
one = [x for x in sk if x["frames"] == 1]
small = [x for x in sk if 2 <= x["frames"] < 60]
large = [x for x in sk if x["frames"] >= 60]
secs = c["seconds"]
L = []
L.append("| Class | Events | Frames | Per second |")
L.append("|---|---|---|---|")
L.append(f"| Whole-frame repeat | {c['repeats']:,} | {c['repeats']:,} | {c['repeats'] / secs:.3f} |")
L.append(f"| One-frame skip | {len(one):,} | {len(one):,} | {len(one) / secs:.3f} |")
L.append(f"| Skip of 2 to 59 frames | {len(small):,} | {sum(x['frames'] for x in small):,} | {len(small) / secs:.3f} |")
L.append(f"| Skip of 60 frames or more | {len(large):,} | {sum(x['frames'] for x in large):,} | {len(large) / secs:.3f} |")
L.append(f"| Silent stretch | {len(c['silent_stretches'])} | {sum(s['frames'] for s in c['silent_stretches'])} | - |")
L.append("")
L.append("| Cycle | Hold, s | Stopped in hold | Last valid after unbind, s | Restart, s | From command, s | Capture stall in restart | Result |")
L.append("|---|---|---|---|---|---|---|---|")
for r in g["cycles"]:
    st = "yes, %s ms" % "/".join(f"{x:.1f}" for x in r["capture_stalls_bind_to_first_valid"]) \
        if r.get("capture_stalls_bind_to_first_valid") else "no"
    L.append(f"| {r['cycle']} | {r['hold_s']:.3f} | {'yes' if r['stopped'] else 'no'} | "
             f"{r['last_valid_after_unbind_s']:.4f} | {r['restart_s']:.4f} | {r['restart_from_command_s']:.4f} | {st} | "
             f"{'PASS' if r['pass_1s'] else 'FAIL'} |")
d = g["restart_distribution"]
L.append("")
L.append("| Population | Count | Below 1 s | Min, s | Median, s | p95, s | Max, s |")
L.append("|---|---|---|---|---|---|---|")
L.append(f"| Demonstrated restarts | {d['count']} | {d['below_1s']} | {d['min']:.4f} | {d['median']:.4f} | {d['p95']:.4f} | {d['max']:.4f} |")
gr = g["restart_growth"]
L.append("")
L.append("| First ten median, s | Last ten median, s | Slope, s per cycle | 95% slope interval, s per cycle | Residual df |")
L.append("|---|---|---|---|---|")
L.append(f"| {gr['first_ten_median']:.4f} | {gr['last_ten_median']:.4f} | {gr['slope_s_per_cycle']:+.6f} | "
         f"[{gr['slope_ci95'][0]:+.6f}, {gr['slope_ci95'][1]:+.6f}] | {gr['dof']} |")
(out / "tables.md").write_text("\n".join(L) + "\n")
print("\n".join(L))
