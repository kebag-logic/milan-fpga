#!/usr/bin/env python3
"""Recompute the restart statistics from the page's per-cycle table.

usage: restart_stats.py <117_AUDIO_CONTINUITY.md>

Reads the table after the restart-cycles marker, and prints the min, median,
nearest-rank p95 (srt[ceil(0.95 n) - 1], the grader's rule), the linearly
interpolated p95, the max, the first-ten and last-ten medians and an OLS slope
with its 95% Student-t interval. The page's printed values are rounded to
four decimals, so the slope is compared at the page's printed precision only.
"""
import math
import statistics
import sys

T975_DF28 = 2.048407141795244  # Student t, 0.975 quantile, 28 df


def rows(path):
    lines = open(path, encoding="utf-8").read().splitlines()
    i = lines.index("<!-- restart-cycles -->")
    out = []
    for line in lines[i + 3:]:
        if not line.startswith("|"):
            break
        cells = [c.strip() for c in line.strip("|").split("|")]
        out.append((int(cells[0]), float(cells[4]), cells[6], cells[7]))
    return out


def main():
    data = rows(sys.argv[1])
    n = len(data)
    rs = [r for _, r, _, _ in data]
    srt = sorted(rs)
    nr = srt[math.ceil(0.95 * n) - 1]
    nr_cycle = [c for c, r, _, _ in data if r == nr]
    pos = 0.95 * (n - 1)
    lo = math.floor(pos)
    lin = srt[lo] + (srt[lo + 1] - srt[lo]) * (pos - lo)
    xs = [c for c, _, _, _ in data]
    mx, my = statistics.fmean(xs), statistics.fmean(rs)
    sxx = sum((x - mx) ** 2 for x in xs)
    slope = sum((x - mx) * (y - my) for x, y in zip(xs, rs)) / sxx
    icpt = my - slope * mx
    rss = sum((y - icpt - slope * x) ** 2 for x, y in zip(xs, rs))
    se = math.sqrt(rss / (n - 2) / sxx)
    print(f"cycles {n}, all PASS {all(v == 'PASS' for *_, v in data)}, below 1 s {sum(r < 1 for r in rs)}")
    print(f"min {min(rs):.4f} median {statistics.median(rs):.4f} max {max(rs):.4f}")
    print(f"p95 nearest-rank (rank {math.ceil(0.95 * n)} of {n}) {nr:.4f}, cycle(s) {nr_cycle}")
    print(f"p95 linear interpolation (position {pos:.2f}) {lin:.4f}")
    print(f"first ten median {statistics.median(rs[:10]):.4f} last ten median {statistics.median(rs[-10:]):.4f}")
    print(f"OLS slope {slope:+.6f} s/cycle, 95% interval [{slope - T975_DF28 * se:+.6f}, {slope + T975_DF28 * se:+.6f}], df {n - 2}")
    print(f"stall rows: {[c for c, _, s, _ in data if s != 'no']}")


if __name__ == "__main__":
    main()
