#!/usr/bin/env python3
"""probe_tally.py < probes.md: count the base/head CPU probe rows, the verdicts that changed, and the largest
|head-base| with its budget (the author's cpu/compare table format)."""
import sys
n = chg = 0
mx = (0.0, "")
for r in sys.stdin.read().splitlines():
    if not r.startswith("|") or r.startswith("| Probe") or r.startswith("|---"):
        continue
    c = [x.strip() for x in r.strip("|").split("|")]
    if len(c) < 6:
        continue
    n += 1
    a, _, b = c[5].partition("/")
    if a.strip() != b.strip():
        chg += 1
        print("CHANGED", r)
    try:
        d = abs(float(c[3]))
    except ValueError:
        print("UNPAIRED", r)
        continue
    if d > mx[0]:
        mx = (d, f"{c[0]} (budget {c[4]} ms)")
print(f"rows {n}; verdict changes {chg}; max |head-base| {mx[0]:.3f} ms at {mx[1]}")
