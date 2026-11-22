#!/usr/bin/env python3
"""hierdiff.py A.rpt B.rpt [depth]: Vivado hierarchical utilization of two synthesized designs, per instance at the
given indent depth (default: every row), the rows whose LUT/FF/RAMB36/RAMB18/DSP differ, and the totals."""
import re, sys
def rows(path):
    out = {}
    stack = []
    for line in open(path):
        m = re.match(r'^\|(\s*)(\S.*?)\s*\|\s*(\S.*?)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|\s*(\d+)\s*\|', line)
        if not m: continue
        ind = len(m.group(1)); name = m.group(2)
        while stack and stack[-1][0] >= ind: stack.pop()
        stack.append((ind, name))
        key = '/'.join(n for _, n in stack)
        out[key] = (ind, m.group(3), int(m.group(4)), int(m.group(8)), float(m.group(9)), float(m.group(10)), int(m.group(11)))
    return out
a, b = rows(sys.argv[1]), rows(sys.argv[2])
depth = int(sys.argv[3]) if len(sys.argv) > 3 else 99
print('| Instance | Module | LUT A | LUT B | dLUT | FF A | FF B | dFF | RAMB36 A/B | RAMB18 A/B | DSP A/B |')
print('|---|---|---:|---:|---:|---:|---:|---:|---|---|---|')
for k in sorted(set(a) | set(b), key=lambda k: (k.count('/'), k)):
    ra, rb = a.get(k), b.get(k)
    r = ra or rb
    if r[0] // 2 > depth: continue
    va = ra[2:] if ra else (0, 0, 0, 0, 0); vb = rb[2:] if rb else (0, 0, 0, 0, 0)
    if va == vb: continue
    print(f'| {k} | {r[1]} | {va[0]} | {vb[0]} | {vb[0]-va[0]:+d} | {va[1]} | {vb[1]} | {vb[1]-va[1]:+d} | {va[2]:g}/{vb[2]:g} | {va[3]:g}/{vb[3]:g} | {va[4]}/{vb[4]} |')
