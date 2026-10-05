#!/usr/bin/env python3
"""Recompute the D-minus-C tables of docs/findings/234_PP_SHADOW_AREA_BASELINE.md
from syn/ooc/pp_resource_baseline.json at base (C) and head (D).
Usage: area_table_check.py <repo> <base-rev> <head-rev>"""
import json, subprocess, sys
repo, base, head = sys.argv[1:4]
ld = lambda r: json.loads(subprocess.check_output(["git", "-C", repo, "show", f"{r}:syn/ooc/pp_resource_baseline.json"]))["endpoints"]
C, D = ld(base), ld(head)
print("ENDPOINT FIGURES C -> D")
for ep in ("route-1x1", "ooc-1x1", "ooc-8x8"):
    c, d = C[ep]["record"]["figures"], D[ep]["record"]["figures"]
    print(" ", ep, {k: (c.get(k), d.get(k)) for k in sorted(d)})
print("SCOPE DELTAS D-C (LUT / FF)")
scopes = ["wrapper", "u_pp", "u_pp/u_notify", "u_pp/u_srp", "u_pp/u_listener", "u_pp/u_aecp",
          "u_pp/u_aecp/u_d3", "u_pp/u_aecp/u_store", "u_pp/u_aecp/u_dyn", "u_pp/u_nvm_port", "u_nvm"]
for s in scopes:
    row = []
    for ep in ("route-1x1", "ooc-1x1", "ooc-8x8"):
        c, d = C[ep]["record"]["scopes"].get(s), D[ep]["record"]["scopes"].get(s)
        row.append("absent" if c is None or d is None else f"{d['LUT']-c['LUT']:+,} / {d['FF']-c['FF']:+,}")
    print(f"  {s:22s} " + " | ".join(row))
r = lambda X, s: X["route-1x1"]["record"]["scopes"][s]
for s in sorted(D["route-1x1"]["record"]["scopes"]):
    if s.startswith("milan") or "datapath" in s:
        print("  route scope", s, "C", r(C, s)["LUT"], r(C, s)["FF"], "D", r(D, s)["LUT"], r(D, s)["FF"])
print("ROUTE RAMB36 by scope D-C:", {s: D["route-1x1"]["record"]["scopes"][s]["RAMB36"] - C["route-1x1"]["record"]["scopes"].get(s, {"RAMB36": 0})["RAMB36"]
      for s in D["route-1x1"]["record"]["scopes"] if D["route-1x1"]["record"]["scopes"][s]["RAMB36"] != C["route-1x1"]["record"]["scopes"].get(s, {"RAMB36": 0})["RAMB36"]})
