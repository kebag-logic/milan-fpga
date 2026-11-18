#!/usr/bin/env python3
"""hier_diff.py OLD.rpt NEW.rpt OLDTAG NEWTAG: two `report_utilization -hierarchical` reports of the release image's
routed checkpoint, diffed per instance on Total LUTs, FFs, RAMB36, RAMB18 and LUTRAMs (Logic LUTs shown too).
Prints (1) the totals; (2) the leaves, each a module's own cells (its "(name)" row or an instance with no children),
which partition the design, so their deltas sum to the totals; grouped by top-level instance and sorted by the LUT
delta, every leaf that moved; (3) every cdc_pair_fifo instance, and its primitives from prims-OLDTAG/NEWTAG.txt."""
import sys
from collections import defaultdict
from pathlib import Path

COLS = ('Total LUTs', 'Logic LUTs', 'LUTRAMs', 'SRLs', 'FFs', 'RAMB36', 'RAMB18', 'DSP Blocks')
SHOW = ('Total LUTs', 'Logic LUTs', 'FFs', 'RAMB36', 'RAMB18', 'LUTRAMs')
SHORT = {'Total LUTs': 'LUT', 'Logic LUTs': 'logic', 'FFs': 'FF', 'RAMB36': 'RAMB36', 'RAMB18': 'RAMB18',
         'LUTRAMs': 'LUTRAM'}


def parse(path: Path) -> tuple[dict, set]:
    rows, parents, stack = {}, set(), []
    header = None
    for line in path.read_text().splitlines():
        if not line.startswith('|'):
            continue
        cells = line.split('|')[1:-1]
        if header is None:
            if cells and cells[0].strip() == 'Instance':
                header = [c.strip() for c in cells]
            continue
        raw = cells[0]
        depth = (len(raw) - len(raw.lstrip(' ')) - 1) // 2
        name = raw.strip()
        stack = stack[:depth]
        own = name.startswith('(') and name.endswith(')')
        path_name = '/'.join(stack + ([f'{name}'] if not own else [name]))
        if stack:
            parents.add('/'.join(stack))
        if not own:
            stack.append(name)
        vals = dict(zip(header, (c.strip() for c in cells)))
        rows[path_name] = {'module': vals['Module'], **{c: float(vals[c]) for c in COLS}}
    return rows, parents


def fmt(x: float) -> str:
    return f'{x:+g}' if x else '0'


old_rows, old_par = parse(Path(sys.argv[1]))
new_rows, new_par = parse(Path(sys.argv[2]))
ot, nt = sys.argv[3], sys.argv[4]
top = next(iter(new_rows))
zero = {c: 0.0 for c in COLS}
print(f'# the release image (all-fabric), routed, ExtraPostPlacementOpt: {ot} against {nt}, '
      'report_utilization -hierarchical')
print(f'# columns {", ".join(SHORT[c] for c in SHOW)}; each delta is {nt} minus {ot}')
o, n = old_rows[top], new_rows[top]
print(f'\n## totals\n{top}: ' + ', '.join(f'{SHORT[c]} {o[c]:g} -> {n[c]:g} ({fmt(n[c] - o[c])})' for c in SHOW))


moved = []
for p in [q for q in old_rows if q != top] + [q for q in new_rows if q != top and q not in old_rows]:
    a, b = old_rows.get(p, zero), new_rows.get(p, zero)
    d = {c: b[c] - a[c] for c in COLS}
    if any(d[c] for c in SHOW):
        moved.append((p, (old_rows.get(p) or new_rows.get(p))['module'], a, b, d))
print('\n## each instance that moved, by its whole total (its own cells and its children), in tree order')
print('# Vivado counts a LUT that packs logic from two instances (LUT6_2) in each of them, so an instance\'s children')
print('# need not sum to it exactly; each row is that instance\'s own report line in each checkpoint.')
for p, mod, a, b, d in moved:
    depth = p.count('/')
    big = abs(d['Total LUTs']) >= 20 or abs(d['FFs']) >= 20 or d['RAMB36'] or d['RAMB18'] or d['LUTRAMs']
    if depth <= 2 or big:
        print(f'{"  " * depth}{p.split("/")[-1]} [{mod}]: ' + ', '.join(f'{SHORT[c]} {a[c]:g}->{b[c]:g} ({fmt(d[c])})' for c in SHOW if d[c]))
small = [m for m in moved if not (m[0].count('/') <= 2 or abs(m[4]['Total LUTs']) >= 20 or abs(m[4]['FFs']) >= 20
                                  or m[4]['RAMB36'] or m[4]['RAMB18'] or m[4]['LUTRAMs'])]
print(f'# {len(small)} deeper instance(s) moved by under 20 LUTs and 20 flops with no RAM change, not listed')
print('\n## every cdc_pair_fifo instance (the whole instance, its primitives)')
for p in sorted(set(old_rows) | set(new_rows)):
    r = old_rows.get(p) or new_rows.get(p)
    if not r['module'].startswith('cdc_pair_fifo') or p.split('/')[-1].startswith('('):
        continue
    a, b = old_rows.get(p, zero), new_rows.get(p, zero)
    same = all(a[c] == b[c] for c in ('LUTRAMs', 'FFs', 'RAMB36', 'RAMB18', 'SRLs'))
    print(f'{"SAME storage and flops" if same else "CHANGED storage or flops"}: {p} [{r["module"]}] '
          + ', '.join(f'{SHORT[c]} {a[c]:g}->{b[c]:g}' for c in SHOW))
here = Path(sys.argv[1]).parent
for tag in (ot, nt):
    f = here / f'prims-{tag}.txt'
    if f.is_file():
        for line in f.read_text().splitlines():
            print(f'  {tag} primitives (cells inside the instance): {line}')
for stem, title in (('lutram', "every primitive named for u_fcdc, wherever synthesis left it in the hierarchy "
                     "(lutram.tcl; its stem lines match distributed RAM alone, since block RAM's primitive group is BMEM, not the "
                     "BLOCKRAM it names, so the candidate's three RAMB36E1 are in its by-type list)"),
                    ('ffs', 'flops of the instances whose flop count moved, and the datapath\'s own (ffs.tcl)')):
    for tag in (ot, nt):
        f = here / f'{stem}-{tag}.txt'
        if f.is_file():
            print(f'\n## {tag}: {title}')
            print(f.read_text().rstrip('\n'))
