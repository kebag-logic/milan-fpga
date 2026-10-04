#!/usr/bin/env python3
"""R457-3: tabulate every standing window at W = 9 (the suites' full legs and
--law-only at both processors) from walk_audit.py's output.

usage: standing_margins.py walk-audit.txt
"""
import sys

rows = {}
for ln in open(sys.argv[1]):
    p = ln.rstrip('\n').split('\t')
    if len(p) == 8 and (p[0].startswith('suite-') or p[0].startswith('lawonly-')):
        rows.setdefault(p[1], {})[p[0]] = (p[2], p[3], p[4], p[7], p[6])
cols = ['suite-head.log', 'lawonly-head.log', 'suite-c4.log', 'lawonly-c4.log']
print('# R457-3: every standing window at W = 9, from walk-audit.txt (suites and --law-only at both processors)')
print('# cell: nearest-pop range, walk w, least clearance c, margin m (= c - 9), fill at graded PDU ends')
print('window\t' + '\t'.join(c.replace('.log', '') for c in cols))
mins = {}
for tag in sorted(rows, key=lambda t: (0, 0) if 'CRF' in t else (1, int(t.split('+')[1]))):
    cells = []
    for c in cols:
        v = rows[tag].get(c)
        if v:
            cells.append(f"{v[3]} w{v[0]} c{v[1]} m{v[2]} {v[4]}")
            if c not in mins or int(v[2]) < mins[c][0]:
                mins[c] = (int(v[2]), tag)
        else:
            cells.append('-')
    print(tag + '\t' + '\t'.join(cells))
for c in cols:
    print(f"# least margin {c}: {mins[c][0]} ({mins[c][1]}); standing windows: "
          f"{sum(1 for t in rows if c in rows[t])}")
