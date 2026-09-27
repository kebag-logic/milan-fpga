#!/usr/bin/env python3
"""R347-5: break down start_edge_probe Part 2 differences by lag and direction.

Usage: python3 -B float_edge_breakdown.py <repo-root>
Differences are sub-ULP knife-edge effects; this reports their size.
"""
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from start_edge_probe import exact, grade, load  # noqa: E402

tc = load(Path(sys.argv[1]))
tally = Counter()
worst = Fraction(0)
for res in (0.001, 0.0001, 0.00025, 1e-6):
    for k in range(1, 20001):
        t_e = k * 0.0137 + 3.3
        for frac in (0.5, 1.0, 2.0):
            start = t_e + frac * res
            clear = t_e + 0.45
            got = grade(tc, start, clear, [t_e], res)[0]
            want = exact(start, clear, [t_e], res)
            if got != want:
                tally[(frac, f"oracle {got} exact {want}")] += 1
                gap = abs(Fraction(start) - Fraction(res) - Fraction(t_e))
                worst = max(worst, gap)
for key, n in sorted(tally.items()):
    print(key, n)
print(f"largest |start - res - event| among differing cases: {float(worst):.3e} s")
