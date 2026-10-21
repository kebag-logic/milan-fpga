#!/usr/bin/env python3
"""Per-instance LUT and FF movement between two Vivado hierarchical
utilization reports (report_utilization -hierarchical), down to depth 3.

usage: hier_delta.py <base.rpt> <cand.rpt> [min |delta|, default 15]
"""
import sys


def read(path):
    rows = {}
    for line in open(path):
        cells = line.split("|")
        if len(cells) < 10 or not cells[1].startswith("   "):
            continue
        name = cells[1].rstrip()
        depth = (len(name) - len(name.lstrip())) // 2
        if depth > 4:
            continue
        try:
            rows[name] = (int(cells[3]), int(cells[7]))
        except ValueError:
            continue
    return rows


base, cand = read(sys.argv[1]), read(sys.argv[2])
lim = int(sys.argv[3]) if len(sys.argv) > 3 else 15
print(f"{'instance':70s} {'LUT':>7s} {'FF':>7s}   (candidate - base)")
for name, (lut, ff) in cand.items():
    b = base.get(name, (0, 0))
    if abs(lut - b[0]) >= lim or abs(ff - b[1]) >= lim:
        print(f"{name:70s} {lut - b[0]:+7d} {ff - b[1]:+7d}")
for name, (lut, ff) in base.items():
    if name not in cand:
        print(f"{name:70s} {-lut:+7d} {-ff:+7d}   (absent in candidate)")
