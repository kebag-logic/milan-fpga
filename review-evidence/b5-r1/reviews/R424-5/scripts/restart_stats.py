#!/usr/bin/env python3
"""Re-derive the restart distribution and slope rows from the page's per-cycle table.

Usage: restart_stats.py <page.md>
"""
import math
import re
import statistics
import sys

T28_975 = 2.048407141795244  # Student's t, 28 df, two-sided 95%


def main(page):
    rows = re.findall(r"^\| (\d+) \| [0-9.]+ \| yes \| [0-9.]+ \| ([0-9.]+) \| [0-9.]+ \| [^|]+ \| PASS \|$",
                      open(page, encoding="utf-8").read(), re.M)
    cyc = [int(c) for c, _ in rows]
    r = [float(v) for _, v in rows]
    n = len(r)
    s = sorted(r)
    p95 = s[math.ceil(0.95 * n) - 1]
    lin = statistics.quantiles(r, n=100, method="inclusive")[94]
    print(f"cycles {n}; below 1 s {sum(v < 1 for v in r)}")
    print(f"min {min(r):.4f} median {statistics.median(r):.4f} p95(nearest rank) {p95:.4f} "
          f"(cycle {cyc[r.index(p95)]}) p95(linear) {lin:.4f} max {max(r):.4f}")
    print(f"first ten median {statistics.median(r[:10]):.4f} last ten median {statistics.median(r[-10:]):.4f}")
    xm, ym = statistics.mean(cyc), statistics.mean(r)
    sxx = sum((x - xm) ** 2 for x in cyc)
    b = sum((x - xm) * (y - ym) for x, y in zip(cyc, r)) / sxx
    a = ym - b * xm
    rss = sum((y - a - b * x) ** 2 for x, y in zip(cyc, r))
    se = math.sqrt(rss / (n - 2) / sxx)
    print(f"slope {b:+.6f} s/cycle, 95% [{b - T28_975 * se:+.6f}, {b + T28_975 * se:+.6f}], df {n - 2}")


if __name__ == "__main__":
    main(sys.argv[1])
