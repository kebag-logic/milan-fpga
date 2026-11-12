#!/usr/bin/env python3
"""Print rows_grade's inputs and each solved row's terms at a point, from a tree given as argv[1]."""
import sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
point = sys.argv[2] if len(sys.argv) > 2 else '1x1/1if'
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
import rows_grade as rg
inp = rg.point_inputs(root, point)
print('header', inp.h)
print('costs', dict(sorted(inp.c.items())))
print('counts', inp.s)
print('rate', inp.rate, 'tick_ms', inp.tick_ms)
for row in rg.SOLVED:
    w, d = rg.solve(row, inp)
    print(row, 'W', w, 'total_ms', round(sum(d.values()) / 1000, 3))
    for k, v in sorted(d.items(), key=lambda t: -t[1]):
        print(f'   {k:14s} {v/1000:8.3f} ms')
