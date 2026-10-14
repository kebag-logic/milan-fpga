#!/usr/bin/env python3
"""Independent re-read of the published full/sharded case receipts: for each suite,
check inventory == full receipt cases (driver order), legs are the strided partition
names[i::n], every case appears exactly once across legs, and per-case
(outcome, returncode, output_sha256[, result_line]) equals the full run.
Usage: python3 -I compare_case_evidence.py <case-evidence-dir>"""
import json, sys
from collections import Counter
from pathlib import Path
root = Path(sys.argv[1]); bad = 0; out = []
for suite in sorted(p.name for p in root.iterdir() if p.is_dir()):
    d = root / suite
    inv = json.loads((d / "inventory.json").read_text())
    full = json.loads((d / "full.json").read_text())
    legs = sorted(d.glob("leg-*.json"))
    legv = [json.loads(p.read_text()) for p in legs]
    n = len(legv)
    issues = []
    if full["inventory"] != inv: issues.append("full inventory != inventory.json")
    if full["shard"] is not None: issues.append("full is sharded")
    if [r["case"] for r in full["results"]] != inv: issues.append("full cases != inventory order")
    seen = []
    heads = {(full["head"], full["tree"])}
    for v in legv:
        i, t = map(int, v["shard"].split("/"))
        heads.add((v["head"], v["tree"]))
        if t != n: issues.append(f"leg total {t} != {n}")
        if [r["case"] for r in v["results"]] != inv[i::t]: issues.append(f"leg {i} != strided partition")
        seen += [r["case"] for r in v["results"]]
    if Counter(seen) != Counter(inv): issues.append("union not exactly once")
    fobs = {r["case"]: r for r in full["results"]}
    diff = [r["case"] for v in legv for r in v["results"] if r != fobs[r["case"]]]
    if diff: issues.append("observation differs: " + ",".join(diff))
    outcomes = Counter(r["outcome"] for r in full["results"])
    out.append({"suite": suite, "cases": len(inv), "legs": n, "outcomes": dict(outcomes),
                "head_tree": sorted(heads), "issues": issues})
    bad |= bool(issues)
print(json.dumps(out, indent=1)); sys.exit(bad)
