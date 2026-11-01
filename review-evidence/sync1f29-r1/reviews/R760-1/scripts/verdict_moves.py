#!/usr/bin/env python3
"""Per probe, the verdict in each pair of published arms: which moved between staged and no-stage."""
import re, sys
from pathlib import Path
ev = Path(sys.argv[1])
def verdicts(p):
    out = {}
    for line in p.read_text().splitlines():
        m = re.match(r'^\| ([^|]+) \| (\d+) \| `([^`]+)` \(([^)]+)\) \| ([^|]*) \| ([^|]+) \|', line)
        if m:
            out[m.group(3)] = m.group(6).strip()
    return out
for a, b in (('P1-none', 'P1-none-u'), ('P8-none', 'P8-none-u'), ('P1-xip-64x1', 'P1-xip-64x1-u'),
             ('P8-xip-64x1', 'P8-xip-64x1-u'), ('P1-xip-512x1', 'P1-xip-512x1-u'), ('P8-xip-512x1', 'P8-xip-512x1-u')):
    va, vb = verdicts(ev / f'budget-{a}-table.md'), verdicts(ev / f'budget-{b}-table.md')
    moved = sorted(k for k in va.keys() & vb.keys() if va[k] != vb[k])
    only = sorted(va.keys() ^ vb.keys())
    print(f'{a}: {len(va)} worst-instance rows, verdicts moved {len(moved)}, rows only on one side {len(only)}')
    for k in moved[:8]:
        print(f'   {k}: staged {va[k]}, no stage {vb[k]}')
print('fits <-> miss crossings (a path present on both sides):')
for a, b in (('P1-xip-64x1', 'P1-xip-64x1-u'), ('P8-xip-64x1', 'P8-xip-64x1-u'), ('P1-xip-512x1', 'P1-xip-512x1-u'), ('P8-xip-512x1', 'P8-xip-512x1-u')):
    va, vb = verdicts(ev / f'budget-{a}-table.md'), verdicts(ev / f'budget-{b}-table.md')
    to_miss = sum(1 for k in va.keys() & vb.keys() if vb[k] == 'fits' and va[k] != 'fits')
    to_fit = sum(1 for k in va.keys() & vb.keys() if va[k] == 'fits' and vb[k] != 'fits')
    print(f'  {a}: with the stage {to_miss} newly miss, {to_fit} newly fit; net {to_miss - to_fit}')
