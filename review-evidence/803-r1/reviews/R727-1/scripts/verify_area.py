#!/usr/bin/env python3
"""verify_area.py <evidence vivado dir> <repo clone>

Recompute the #803 area figures from the published Vivado reports and the
committed resource record (syn/ooc/pp_resource_baseline.json); tolerances are
those AREA_BUDGET.md lists. Prints each figure, delta and verdict."""
import json, re, sys
from pathlib import Path
ev, repo = Path(sys.argv[1]), Path(sys.argv[2])

def used(path, label):
    for line in path.read_text().splitlines():
        m = re.match(r"\|\s*%s\s*\|\s*([0-9.]+)\s*\|" % re.escape(label), line)
        if m:
            return float(m.group(1))
    raise SystemExit("no row %r in %s" % (label, path))

rec = json.loads((repo / "syn/ooc/pp_resource_baseline.json").read_text())["endpoints"]
TOL = {"route-1x1": {"LUT": 500, "FF": 600, "SLICE": 80},
       "ooc-1x1": {"LUT": 250, "FF": 250}, "ooc-8x8": {"LUT": 316, "FF": 339}}
head = {
    "route-1x1": ev / "route-1x1-alinx_ax7101_utilization_place.rpt",
    "ooc-1x1": ev / "ooc-1x1-baseline_utilization.rpt",
    "ooc-8x8": ev / "ooc-8x8-baseline_utilization.rpt",
}
ok = True
for ep, rpt in head.items():
    lut_label = "Slice LUTs" if ep == "route-1x1" else "Slice LUTs*"
    fig = {"LUT": used(rpt, lut_label), "FF": used(rpt, "Slice Registers")}
    if ep == "route-1x1":
        fig["SLICE"] = used(rpt, "Slice")
    for k, v in fig.items():
        base = rec[ep]["record"]["figures"][k]
        d = v - base
        verdict = "ok" if d <= TOL[ep][k] else "OVER"
        ok &= verdict == "ok"
        print("%-9s %-5s record %8d head %8d delta %+5d tol %4d %s" % (ep, k, base, v, d, TOL[ep][k], verdict))
dev = ev / "dev-97aab1d0-nightly-utilization_place.rpt"
r = head["route-1x1"]
for label, k in (("Slice LUTs", "LUT"), ("Slice Registers", "FF"), ("Slice", "SLICE")):
    print("route-1x1 %-5s dev %8d head %8d delta %+5d" % (k, used(dev, label), used(r, label), used(r, label) - used(dev, label)))
print("route-1x1 slices free at head: %d of 15850" % (15850 - used(r, "Slice")))
print("RESULT:", "PASS" if ok else "FAIL")
