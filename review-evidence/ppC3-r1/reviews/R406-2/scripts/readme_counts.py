#!/usr/bin/env python3
"""Compare tb/adp_engine/README.md's campaign table (the leading count of 'Failing checks')
with the failure counts of mutants.py stdouts. usage: readme_counts.py README stdout..."""
import re, sys
readme = {}
for line in open(sys.argv[1]):
    m = re.match(r"\| `([a-z0-9-]+)` \|[^|]*\|[^|]*\| (\d+)[:,]? ", line)
    if m: readme[m[1]] = int(m[2])
runs = {}
for path in sys.argv[2:]:
    for line in open(path):
        m = re.match(r"([a-z0-9-]+): rc=\d+ failures=(\d+) named=\d+ (KILLED|UNPROVEN)", line)
        if m: runs[m[1]] = (int(m[2]), m[3])
bad = 0
for arm in sorted(set(readme) | set(runs)):
    r, (n, v) = readme.get(arm), runs.get(arm, (None, None))
    ok = r == n and v == "KILLED"; bad += not ok
    print(f"{'OK ' if ok else 'BAD'} {arm}: README {r}, measured {n} {v}")
print(f"{len(runs)} arms measured, {len(readme)} README rows, {bad} mismatches")
