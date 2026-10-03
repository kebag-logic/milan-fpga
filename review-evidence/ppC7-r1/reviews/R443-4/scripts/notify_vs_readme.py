#!/usr/bin/env python3
"""Compare notify_mutants.py per-arm failing-check counts (from each arm's own log) with the README.

Usage: notify_vs_readme.py <campaign-output-dir> <tb/pp_top/README.md> <campaign-log>
"""
import json, re, sys
from pathlib import Path
out, readme, log = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
verdict = {}
for line in open(log):
    if line.startswith("{"):
        d = json.loads(line); verdict[d["mutant"]] = d["verdict"]
rec, on = {}, False
for line in open(readme):
    if line.startswith("#"):
        on = "notify_mutants.py" in line
    m = re.match(r"^\| `([a-z0-9_]+)` \|.*\| (\d+)[,:]", line)
    if on and m:
        rec[m.group(1)] = int(m.group(2))
bad = 0
for arm, n in rec.items():
    f = out / f"{arm}.log"
    got = sum(1 for l in f.read_text(errors="replace").splitlines() if re.match(r"^\s*FAIL\b", l)) if f.exists() else None
    ok = got == n and verdict.get(arm) == "KILLED"; bad += not ok
    print(f"{'AGREE' if ok else 'DISAGREE'} {arm}: log FAIL lines {got}, verdict {verdict.get(arm)}; README {n}")
print(f"README arms {len(rec)}, KILLED in run {sum(v == 'KILLED' for v in verdict.values())}, disagreeing {bad}")
sys.exit(1 if bad else 0)
