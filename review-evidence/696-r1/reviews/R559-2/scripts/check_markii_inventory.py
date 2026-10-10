#!/usr/bin/env python3
"""Compare MARK_II_AREA_PLAN.md 'Current processor inventory' table and the
gate row against syn/ooc/pp_resource_baseline.json at the checked-out head.
Usage: python3 -I check_markii_inventory.py <repo-root>"""
import json, re, sys, pathlib
root = pathlib.Path(sys.argv[1])
rec = json.loads((root / "syn/ooc/pp_resource_baseline.json").read_text())["endpoints"]
plan = (root / "docs/design/MARK_II_AREA_PLAN.md").read_text().splitlines()
start = next(i for i, l in enumerate(plan) if l.startswith("### Current processor inventory"))
rows, diffs = 0, 0
for l in plan[start:]:
    if l.startswith("## ") : break
    m = re.match(r"\| `([^`]+)` \| ([\d,]+) \| ([\d,]+) \| ([\d,]+) \|", l)
    if not m: continue
    rows += 1
    scope = m.group(1)
    for col, ep in zip((2, 3, 4), ("route-1x1", "ooc-1x1", "ooc-8x8")):
        doc = int(m.group(col).replace(",", ""))
        sc = rec[ep]["record"].get("scopes", {}).get(scope)
        got = sc["LUT"] if sc else None
        ok = got == doc
        diffs += not ok
        print(f"{scope:24s} {ep:9s} doc={doc:6d} record={got} {'OK' if ok else 'DIFF'}")
print(f"rows={rows} figures={rows*3} differences={diffs}")
r = rec["route-1x1"]
wns, floor, tol = r["record"]["figures"]["WNS_ns"], r["floor"]["WNS_ns"], r["tolerance"]["WNS_ns"]
print(f"route WNS record={wns} floor={floor} fall_tolerance={tol} floor_fall={wns-floor:.3f} tolerance_bound={wns-tol:.3f}")
gate = [l for l in plan if l.startswith("| Gate comparison")]
print("gate row:", gate)
ok_gate = (f"+{wns:.3f}" in gate[0]) and (f"+{floor:.3f}" in gate[0]) and (f"{wns-floor:.3f}" in gate[0]) and (f"{tol:.2f}" in gate[0])
print("gate row matches record:", ok_gate)
sys.exit(0 if diffs == 0 and rows == 22 and ok_gate else 1)
