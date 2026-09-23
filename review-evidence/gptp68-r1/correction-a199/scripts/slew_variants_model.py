#!/usr/bin/env python3
"""Discrete per-pair model of the SERVO loop under the re-decided #68 policy,
comparing the PI input saturated at +-20 us (A) with an unsaturated input (B),
both with the total written rate clamped to +-200 ppm. Units: ppm and ns;
one pair per 125 ms. Ideal arithmetic (no Q8.24 truncation): this compares
shapes, it is not the ROM mirror."""
def run(x0, fm, sat_in, n=400):
    x, i = float(x0), -float(fm)          # converged rate before the jump
    hist = []
    for _ in range(n):
        e = x
        if sat_in:
            e = max(-20000.0, min(20000.0, e))
        t = 8.0 * e / 1000.0              # ppm that removes e in one pair
        i = max(-200.0, min(200.0, i + t / 4))
        out = max(-200.0, min(200.0, 0.75 * t + i))
        a = -out
        hist.append((x, a))
        x = x + (a - fm) * 125.0          # ns gained over 125 ms
    return hist

def settle(hist, tol=1000.0):
    last = max((k for k, (x, _) in enumerate(hist) if abs(x) >= tol), default=-1)
    return last + 1

for fm in (-140, 0, 140):
    for x0 in (25000, 50000, 90000, 100000, -100000):
        row = []
        for sat_in in (True, False):
            h = run(x0, fm, sat_in)
            s = settle(h)
            sign = 1 if x0 > 0 else -1
            over = max(0.0, max(-sign * x for x, _ in h))
            peak = max(abs(a) for _, a in h)
            row.append(f"{'A' if sat_in else 'B'}: settle<1us {s:3d} pairs "
                       f"({s * 0.125:5.2f} s) overshoot {over / 1000:6.2f} us "
                       f"peak {peak:5.1f} ppm")
        print(f"master {fm:+4d} ppm, jump {x0 / 1000:+7.1f} us | " + " | ".join(row))
