#!/usr/bin/env python3
"""Compare a ctr_mutants.py printed record with the tb/pp_top README's per-arm record.

Usage: ctr_record_vs_readme.py <campaign-log> <tb/pp_top/README.md>
For each arm: the failure count, and the per-check multiset (K-label x count), must agree.
"""
import collections, re, sys
log, readme = sys.argv[1], sys.argv[2]
run = {}
arm = None
for line in open(log):
    m = re.match(r"^(\S+): rc=\d+ failures=(\d+) named=\d+ (KILLED|UNPROVEN)", line)
    if m:
        arm = m.group(1); run[arm] = [int(m.group(2)), collections.Counter(), m.group(3)]; continue
    m = re.match(r"^\s+FAIL: (K\d+)", line)
    if m and arm:
        run[arm][1][m.group(1)] += 1
rec = {}
for line in open(readme):
    m = re.match(r"^\| `([a-z0-9-]+)` \|.*\| (\d+): (.*) \|\s*$", line)
    if m and m.group(1) in run:
        c = collections.Counter()
        for part in m.group(3).split(","):
            k = re.match(r"\s*(K\d+)(?: x(\d+))?", part)
            if k:
                c[k.group(1)] += int(k.group(2) or 1)
        rec[m.group(1)] = (int(m.group(2)), c)
bad = 0
for a, (n, c, v) in run.items():
    r = rec.get(a)
    ok = r is not None and r[0] == n and r[1] == c and v == "KILLED"
    bad += not ok
    print(f"{'AGREE' if ok else 'DISAGREE'} {a}: run {n} {dict(sorted(c.items()))} {v}; README {r[0] if r else None} {dict(sorted(r[1].items())) if r else None}")
print(f"arms {len(run)}, disagreeing {bad}")
sys.exit(1 if bad else 0)
