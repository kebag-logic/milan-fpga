#!/usr/bin/env python3
"""Compare aecp_mutants.py per-arm failure counts with the tb/pp_top README C5a table.

Usage: aecp_vs_readme.py <campaign-log> <tb/pp_top/README.md>
Rows group arms as "`base`, `-suffix`"; the last cell is "N: ..." or "the same N; ...".
"""
import re, sys
log, readme = sys.argv[1], sys.argv[2]
run = {}
for line in open(log):
    m = re.match(r"^(\S+): rc=-?\d+ failures=(\d+)\b.*\b(KILLED|UNPROVEN)\s*$", line)
    if m:
        run[m.group(1)] = (int(m.group(2)), m.group(3))
rec, on = {}, False
for line in open(readme):
    if line.startswith("#"):
        on = "aecp_mutants.py" in line and "C5a" in line
    if not on or not line.startswith("| `"):
        continue
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    names = re.findall(r"`([^`]+)`", cells[0])
    m = re.match(r"(?:the same )?(\d+)", cells[-1])
    if not names or not m:
        continue
    n = int(m.group(1)); base = names[0]; arms = [base]
    for s in names[1:]:
        parts = base.split("-")
        for k in range(len(parts), 0, -1):
            cand = "-".join(parts[:k]) + s
            if cand in run:
                arms.append(cand); break
        else:
            arms.append(base + s)
    for a in arms:
        rec[a] = n
bad = 0
for arm, (n, v) in run.items():
    r = rec.get(arm); ok = r == n and v == "KILLED"; bad += not ok
    print(f"{'AGREE' if ok else 'DISAGREE'} {arm}: run {n} {v}; README {r}")
print(f"arms run {len(run)}, README arms {len(rec)}, disagreeing {bad}, README arms not run {sorted(set(rec)-set(run))}")
sys.exit(1 if bad else 0)
