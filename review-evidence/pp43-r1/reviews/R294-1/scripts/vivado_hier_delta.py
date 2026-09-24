#!/usr/bin/env python3
"""R294: per-instance delta of two Vivado `report_utilization -hierarchical`
reports (published author evidence, base vs candidate). Usage: a.rpt b.rpt"""
import sys
def parse(p):
    hdr, rows = None, {}
    for line in open(p):
        if line.startswith('|') and 'Instance' in line and hdr is None:
            hdr = [c.strip() for c in line.strip().strip('|').split('|')]
        elif hdr and line.startswith('|'):
            cells = [c.rstrip() for c in line.strip().strip('|').split('|')]
            if len(cells) == len(hdr):
                rows[cells[0]] = dict(zip(hdr, [c.strip() for c in cells]))
    return rows
b, c = parse(sys.argv[1]), parse(sys.argv[2])
for k, v in c.items():
    if k in b:
        d = {col: int(v[col]) - int(b[k][col]) for col in ('Total LUTs', 'FFs', 'RAMB36', 'RAMB18')}
        if any(d.values()):
            print(f"{k.rstrip():45s} {v['Module']:40s} dLUT={d['Total LUTs']:+5d} dFF={d['FFs']:+5d} dRAMB36={d['RAMB36']:+d} dRAMB18={d['RAMB18']:+d}")
