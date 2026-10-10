#!/usr/bin/env python3
"""Compare the MARK_II_AREA_PLAN current-inventory table (scope | route | ooc-1x1 | ooc-8x8)
with the LUT scopes recorded in syn/ooc/pp_resource_baseline.json. argv[1] = repo root."""
import json, re, sys
root = sys.argv[1]
base = json.load(open(f"{root}/syn/ooc/pp_resource_baseline.json"))
eps = base["endpoints"]
plan = open(f"{root}/docs/design/MARK_II_AREA_PLAN.md").read()
start = plan.index("These are the source-scope references of the gate's current record")
rows = re.findall(r"^\| `([^`]+)` \| ([\d,]+) \| ([\d,]+) \| ([\d,]+) \|", plan[start:start + 6000], re.M)
diff = 0
for scope, *vals in rows:
    for ep, v in zip(("route-1x1", "ooc-1x1", "ooc-8x8"), vals):
        rec = eps[ep]["record"]["scopes"].get(scope, {}).get("LUT")
        if rec != int(v.replace(",", "")):
            diff += 1; print("DIFF", scope, ep, v, rec)
print(f"rows {len(rows)}, figures {3*len(rows)}, differences {diff}")
r = eps["route-1x1"]["record"]["figures"]; print("route figures:", {k: r[k] for k in ("LUT", "FF", "SLICE", "WNS_ns", "WHS_ns")})
sys.exit(1 if diff or not rows else 0)
