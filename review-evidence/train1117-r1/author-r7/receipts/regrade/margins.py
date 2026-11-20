#!/usr/bin/env python3
"""margins.py OUTDIR [TREE]: each statement's margin at each point from a head's survey (r4meas/out/<rev>): the most
measured cycles, the statement it is held to and the cycles left before the rule (the most measured plus 5 %,
rounded up to 5 us) passes it, floor(stated * 100 / 1.05) - cycles, thinnest first. With TREE, the statements are
read again from TREE's tables (load_grade.stated and poll_grade), so a restated tree's margins are shown."""
import json
import math
import re
import sys
from pathlib import Path

out = Path(sys.argv[1])
tree = Path(sys.argv[2]) if len(sys.argv) > 2 else None
PT = {'1x1': '1x1/1if', '8x8-1if': '8x8/1if', '8x8': '8x8/2if'}
ROW = re.compile(r'^(\S+)\s+([\d,]+)\s+[\d.]+\s+(\d+)\s+(\d+)\s+(within|OVER(?:-raw)?)\s+(.*?); (\S+)')
now = {}
if tree:
    sys.path.insert(0, str(tree / 'tb/verilator/ctrl_service_budget'))
    import load_grade  # noqa: E402
    for point in PT.values():
        now[point] = load_grade.stated(tree, point)
for p, point in PT.items():
    f = out / f'survey-{p}/compare-ordinary.txt'
    if not f.is_file():
        continue
    seen = {}
    for line in f.read_text().splitlines():
        m = ROW.match(line)
        if not m:
            continue
        key, cycles, rule, stated, verdict, table, where = m.groups()
        cycles, stated = int(cycles.replace(',', '')), int(stated)
        if cycles == 0:
            continue
        if tree and table.startswith('load_grade') and key in now[point]:
            stated = int(now[point][key])
        k = (key, table.split('(')[0].split('[')[0])
        if k not in seen or stated < seen[k][1]:
            seen[k] = (cycles, stated, where.rstrip(';'))
    rows = sorted(((math.floor(st * 100 / 1.05) - c, key, tab, c, st, w) for (key, tab), (c, st, w) in seen.items()))
    print(f'### {point}\n\n| Cost | Table | Most measured, cycles | Statement, us | Margin, cycles | Where |\n|---|---|---:|---:|---:|---|')
    for margin, key, tab, c, st, w in rows:
        print(f'| {key} | {tab} | {c:,} | {st} | {margin:+,} | {w} |')
    print()
