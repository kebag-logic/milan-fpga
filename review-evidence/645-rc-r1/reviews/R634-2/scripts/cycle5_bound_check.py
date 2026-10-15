#!/usr/bin/env python3
"""Simulation sanity check of B17's later-burst lower-bound argument on dev's datapath:
for B17 cycle 5 (later burst 30.260 us), a bind whose head-measured lowest primed margin
is below 30.260 - 20.833 = 9.427 us should slip a second frame at a later burst; above
it, only the first-burst frame. usage: cycle5_bound_check.py <head dir> <base dir> [...pairs]"""
import re, sys
from pathlib import Path
res = re.compile(r"RESULT-645-BIND: B17 cycle (\d+) phase ([0-9.]+) .*?primed margin ([-0-9.e+]+)\.\.([-0-9.e+]+) us.*?SLIP_LB \+(\d+) dups")
def read(d):
    o = {}
    for log in Path(d).glob('bind_*.log'):
        for line in log.read_text().splitlines():
            m = res.search(line)
            if m: o[(log.stem, int(m.group(1)))] = (float(m.group(2)), float(m.group(3)), float(m.group(4)), int(m.group(5)))
    return o
args = sys.argv[1:]
rows = []
for h, b in zip(args[::2], args[1::2]):
    H, B = read(h), read(b)
    for k in H:
        if k[1] == 5: rows.append((H[k][1], H[k][2], B[k][3], Path(h).name, k[0]))
rows.sort()
below = [r for r in rows if r[0] < 9.4267]; above = [r for r in rows if r[0] > 9.4267]
print('cycle-5 binds', len(rows))
print('head lowest primed < 9.427 us:', len(below), 'dev dups histogram', {d: sum(1 for r in below if r[2] == d) for d in sorted({r[2] for r in below})})
print('head lowest primed > 9.427 us:', len(above), 'dev dups histogram', {d: sum(1 for r in above if r[2] == d) for d in sorted({r[2] for r in above})})
print('nearest the edge:')
for r in rows:
    if 8.0 <= r[0] <= 11.0: print('  primed %.3f..%.3f dev +%d dups  %s/%s' % r)
