#!/usr/bin/env python3
"""Compare each arm's failing-check count in a driver log (`name: rc=R failures=N named=K VERDICT`)
with the count its suite README records (`| `name` | ... | N...` table rows, the first integer of
the row's last cell, or of its last cell that starts with a digit).
usage: compare_counts.py LOG README [README ...]"""
import re, sys
log = open(sys.argv[1]).read()
rows = {}
for path in sys.argv[2:]:
    for line in open(path):
        m = re.match(r"^\|\s*`([A-Za-z0-9_.-]+)`\s*\|", line)
        if not m:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        nums = [c for c in cells[1:] if re.match(r"^\*?\*?\d", c)]
        if nums:
            rows.setdefault(m.group(1), []).append(int(re.match(r"^\*?\*?(\d+)", nums[-1]).group(1)))
same = diff = missing = 0
for name, n, verdict in re.findall(r"^([A-Za-z0-9_.-]+): rc=\S+ failures=(\d+) named=\d+ (\S+)", log, re.M):
    rec = rows.get(name)
    if rec is None:
        missing += 1; print(f"NO RECORD {name} {n} {verdict}")
    elif int(n) in rec:
        same += 1
    else:
        diff += 1; print(f"DIFFERS {name}: run {n} {verdict}, record {rec}")
print(f"{same} at the record, {diff} differ, {missing} without a parsed record")
