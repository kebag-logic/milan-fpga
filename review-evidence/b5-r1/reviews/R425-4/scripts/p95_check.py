#!/usr/bin/env python3
"""Recompute the restart distribution figures from the page's per-cycle table.
usage: p95_check.py <page.md>"""
import math, re, statistics, sys
rows = [l.split("|") for l in open(sys.argv[1]) if re.match(r"\| \d+ \| 2\.0", l)]
r = [(float(c[5]), int(c[1])) for c in rows]
s = sorted(r)
v = [x for x, _ in s]
k = math.ceil(0.95 * len(v))
pos = 0.95 * (len(v) - 1); lo = int(pos)
lin = v[lo] + (v[lo + 1] - v[lo]) * (pos - lo)
print(f"n={len(v)} min={v[0]} median={statistics.median(v):.4f} max={v[-1]} below1s={sum(x < 1 for x in v)}")
print(f"nearest-rank p95: rank {k} -> {v[k-1]} (cycle {s[k-1][1]})")
print(f"linear-interpolation p95: {lin:.4f}")
xs = [c for _, c in r]; ys = [x for x, _ in r]
mx, my = statistics.mean(xs), statistics.mean(ys)
b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
print(f"OLS slope {b:.6f} s per cycle; first ten median {statistics.median(ys[:10]):.4f}; last ten median {statistics.median(ys[-10:]):.4f}")
