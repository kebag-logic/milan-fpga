#!/usr/bin/env python3
"""Merge batched tb/pp_top/d3_mutants.py results.json files and apply the driver's rule.

usage: d3_merge.py <repo> <batchdir> [<batchdir> ...]
Every mutant of the driver's MUTANTS table must appear exactly once across the
batches with verdict KILLED, and every golden of every batch must be PASS.
"""
import importlib.util
import json
import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location("d3", repo / "tb/pp_top/d3_mutants.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
names = [m.name for m in mod.MUTANTS]
seen: dict[str, str] = {}
goldens = []
for d in sys.argv[2:]:
    for r in json.loads((Path(d) / "results.json").read_text()):
        if r["mutant"].startswith("golden-"):
            goldens.append((d, r["mutant"], r["verdict"]))
        else:
            if r["mutant"] in seen:
                print("DUPLICATE", r["mutant"])
            seen[r["mutant"]] = r["verdict"]
missing = [n for n in names if n not in seen]
extra = [n for n in seen if n not in names]
killed = sum(v == "KILLED" for v in seen.values())
bad_g = [g for g in goldens if g[2] != "PASS"]
print(f"table {len(names)}; results {len(seen)}; KILLED {killed}; missing {missing}; extra {extra}")
print(f"goldens {len(goldens)} run, not PASS: {bad_g}")
for n, v in seen.items():
    if v != "KILLED":
        print("NOT KILLED", n, v)
sys.exit(0 if (killed == len(names) and not missing and not extra and not bad_g) else 1)
