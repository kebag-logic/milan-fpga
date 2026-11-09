#!/usr/bin/env python3
"""cmp_campaign.py MINE THEIRS: compare two tb/srp_top mutants.py logs line by line on (label, rc, failures,
verdict) in declared order, and the closing tally and coverage lines. Prints every difference."""
import re, sys
def parse(p):
    rows, tail = [], []
    for line in open(p, errors="replace"):
        m = re.match(r"^([a-z0-9-]+): rc=(\d+) failures=(\d+) (KILLED|UNPROVEN)", line)
        if m: rows.append(m.groups())
        elif line.startswith(("assertion coverage:", "control ")) or re.match(r"^\d+ checks:", line): tail.append(line.strip())
    return rows, tail
a, ta = parse(sys.argv[1]); b, tb = parse(sys.argv[2])
n = min(len(a), len(b)); diff = [(i, a[i], b[i]) for i in range(n) if a[i] != b[i]]
print(f"mine {len(a)} arm results, theirs {len(b)}; compared {n}; differing {len(diff)}")
for d in diff: print("DIFF", *d)
print("mine killed", sum(r[3] == "KILLED" for r in a), "unproven", sum(r[3] == "UNPROVEN" for r in a))
for x, y in zip(ta, tb):
    print(("SAME " if x == y else "DIFF ") + x + ("" if x == y else "  |  " + y))
if len(ta) != len(tb): print(f"tail lines: mine {len(ta)}, theirs {len(tb)}")
