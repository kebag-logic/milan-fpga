#!/usr/bin/env python3
"""Compare a campaign's printed per-arm failure counts with a README table's last column.

Usage: campaign_vs_readme.py <campaign-log> <README.md> [section-heading-substring]
Log lines: "<arm>: rc=N failures=N ... KILLED|UNPROVEN". README rows: "| `<arm>` | ... | N |".
If a heading substring is given, README rows are read only from that section on to the next ### heading.
"""
import re, sys
log, readme = sys.argv[1], sys.argv[2]
sect = sys.argv[3] if len(sys.argv) > 3 else None
run = {}
for line in open(log):
    m = re.match(r"^(\S+): rc=-?\d+ failures=(\d+)\b.*\b(KILLED|UNPROVEN)\s*$", line)
    if m:
        run[m.group(1)] = (int(m.group(2)), m.group(3))
rec, on = {}, sect is None
for line in open(readme):
    if sect is not None and line.startswith("#"):
        on = sect in line
    if not on:
        continue
    m = re.match(r"^\| `([A-Za-z0-9_.-]+)` \|.*\| (\d+) \|\s*$", line)
    if m and m.group(1) not in rec:
        rec[m.group(1)] = int(m.group(2))
bad = 0
for arm, (n, v) in run.items():
    r = rec.get(arm)
    ok = r == n and v == "KILLED"
    bad += not ok
    print(f"{'AGREE' if ok else 'DISAGREE'} {arm}: run {n} {v}; README {r}")
missing = sorted(set(rec) - set(run))
print(f"arms run {len(run)}, README rows {len(rec)}, disagreeing {bad}, README rows not run {missing}")
sys.exit(1 if bad else 0)
