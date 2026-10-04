#!/usr/bin/env python3
"""Compare each datapath point's recorded shape-header digest with a fresh builder generation.

Usage: check_shape_digests.py <run-receipts.json> <sweep_plan.json> <repo> <work>
"""
import hashlib, json, sys
from pathlib import Path
rr = json.load(open(sys.argv[1])); plan = json.load(open(sys.argv[2])); repo, work = Path(sys.argv[3]), Path(sys.argv[4])
bad = 0
for p in plan["points"]:
    if p["top"] != "milan_datapath": continue
    shape = p.get("shape", plan["tops"]["milan_datapath"]["shape"])
    stem = shape if shape.startswith("endstation_") else f"endstation_{shape}"
    for root in (repo, work / "tree"):
        h = root / "configs/generated" / stem / "gen/adp_shape_defaults.svh"
        if h.is_file(): break
    mine = hashlib.sha256(h.read_bytes()).hexdigest()
    rec = rr["points"][p["name"]]["inputs"]["shape_header"]
    ok = mine == rec; bad += not ok
    print(f"{'MATCH ' if ok else 'DIFFER'} {p['name']:20s} {shape:32s} {mine[:16]} {'tracked' if root == repo else 'generated'}")
print("differing:", bad); sys.exit(1 if bad else 0)
