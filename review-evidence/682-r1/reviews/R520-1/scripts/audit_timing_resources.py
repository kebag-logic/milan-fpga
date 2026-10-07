#!/usr/bin/env python3
"""Audit the published timing and resource evidence for internal consistency.

Usage: audit_timing_resources.py <evidence-author-dir> <repo-clone> <rev>
Checks: each directive's worst = min over corners; section-5 thresholds
(WNS >= 0.03, WHS >= 0) at every corner; route_status fully routed with zero
errors; selected directive figures equal the committed route-1x1 record at
<rev>; worst-path text slack equals the worst setup slack; PR-claimed figures.
"""
import json, re, subprocess, sys
from pathlib import Path

ev, repo, rev = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
t = json.loads((ev / "round2-timing-directives.json").read_text())
base = json.loads(subprocess.check_output(["git", "-C", repo, "show", f"{rev}:syn/ooc/pp_resource_baseline.json"]))
route = base["endpoints"]["route-1x1"]["record"]["figures"]
fails = 0
def check(cond, msg):
    global fails
    print(("PASS " if cond else "FAIL ") + msg)
    fails += 0 if cond else 1
claimed = {"ExtraPostPlacementOpt": (0.124, 0.031), "AltSpreadLogic_high": (0.090, 0.011), "ExtraTimingOpt": (0.055, 0.020)}
for name, d in t["directives"].items():
    c = d["corners"]
    check(len(c) == 4, f"{name}: four corners {sorted(c)}")
    wns = min(v["WNS_ns"] for v in c.values()); whs = min(v["WHS_ns"] for v in c.values())
    check(abs(wns - d["worst"]["WNS_ns"]) < 1e-9 and abs(whs - d["worst"]["WHS_ns"]) < 1e-9, f"{name}: worst equals corner minimum ({wns}, {whs})")
    check(all(v["WNS_ns"] >= 0.03 and v["WHS_ns"] >= 0 for v in c.values()), f"{name}: every corner WNS>=+0.03 and WHS>=0")
    rs = d["route_status"]
    check(rs["routable nets"] == rs["fully routed nets"] and rs["nets with routing errors"] == 0, f"{name}: fully routed, zero errors ({rs['routable nets']} nets)")
    check(claimed[name] == (round(wns, 3), round(whs, 3)), f"{name}: PR table figures {claimed[name]} match evidence")
    m = re.search(r"Slack \(MET\) :\s+([-0-9.]+)ns", d["worst_paths"][0]) if d.get("worst_paths") else None
    check(m is not None and abs(float(m.group(1)) - wns) < 1e-9, f"{name}: worst-path text slack equals worst WNS")
    check(all(re.fullmatch(r"[0-9a-f]{64}", a["sha256"]) for a in d["artifacts"].values()), f"{name}: {len(d['artifacts'])} artifacts carry sha256 digests")
sel = t["best"]
check(sel == "ExtraPostPlacementOpt", "selected directive is ExtraPostPlacementOpt")
u = t["directives"][sel]["utilization"]
for k in ("LUT", "FF", "SLICE", "BRAM_TILE", "RAMB36", "RAMB18", "DSP"):
    check(u[k] == route[k], f"selected {k} {u[k]} == committed route-1x1 {route[k]}")
check(abs(t["directives"][sel]["worst"]["WNS_ns"] - route["WNS_ns"]) < 1e-9 and abs(t["directives"][sel]["worst"]["WHS_ns"] - route["WHS_ns"]) < 1e-9, "selected worst WNS/WHS == committed route record")
best = max(t["directives"], key=lambda n: t["directives"][n]["worst"]["WNS_ns"])
check(best == sel, f"selected route has the best worst-corner WNS ({best})")
print(f"TOTAL failures: {fails}")
sys.exit(1 if fails else 0)
