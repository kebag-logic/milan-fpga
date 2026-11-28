#!/usr/bin/env python3
"""Compare two arcs.py dumps: rows (function, state, arcs, source text) only in one side,
and the per-side totals of lines and arcs those rows carry.
usage: arcdiff.py <before> <after>"""
import sys
from collections import Counter
def rows(path):
    return [l.rstrip('\n') for l in open(path) if not l.startswith('#')]
def narcs(row):
    return int(row.split('arcs=')[1].split()[0])
a, b = Counter(rows(sys.argv[1])), Counter(rows(sys.argv[2]))
only_a, only_b = a - b, b - a
for tag, side in (('-', only_a), ('+', only_b)):
    for row, n in sorted(side.items()):
        for _ in range(n):
            print(tag, row)
print(f'only before: {sum(only_a.values())} lines, {sum(narcs(r) * n for r, n in only_a.items())} arcs, '
      f'{sum(n for r, n in only_a.items() if narcs(r))} lines with arcs')
print(f'only after:  {sum(only_b.values())} lines, {sum(narcs(r) * n for r, n in only_b.items())} arcs, '
      f'{sum(n for r, n in only_b.items() if narcs(r))} lines with arcs')
for name, c in (('before', a), ('after', b)):
    print(f'{name}: lines {sum(c.values())} arcs {sum(narcs(r) * n for r, n in c.items())} '
          f'untaken arcs {sum(r.split("[")[1].split("]")[0].split().count("u") * n for r, n in c.items())} '
          f'unexecuted lines {sum(n for r, n in c.items() if " ZERO " in r)}')
