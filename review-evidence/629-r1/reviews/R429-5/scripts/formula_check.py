#!/usr/bin/env python3
"""Closed-form check of the #629 random-loss falloff statements (round 5).

q = 1 - (1 - p)^16 per group; 500 groups/s; run-start rate 500 q^2 (1 - q);
valid fraction exp(-4.096 * rate). Prints the table rows, the 90/50/10/1 %
crossings in lost PDUs per second, round 3's comparison and the round-4
single-seed expectations.
"""
import math

T = 4.096


def q_of(p):
    return 1.0 - (1.0 - p) ** 16


def approx(p):
    q = q_of(p)
    return 500 * q * q


def exact(p):
    q = q_of(p)
    return 500 * q * q * (1 - q)


def solve(target, f):
    lo, hi = 1e-7, 0.05
    for _ in range(200):
        mid = (lo + hi) / 2
        if math.exp(-T * f(mid)) > target:
            lo = mid
        else:
            hi = mid
    return lo


print("p, lost/s, 500q^2, exact, valid(approx), valid(exact)")
for p in (1e-4, 5e-4, 1e-3, 1.4e-3, 2e-3, 3e-3):
    print(f"{p:.1e} {8000*p:6.1f} {approx(p):.4f} {exact(p):.4f} "
          f"{math.exp(-T*approx(p)):.4f} {math.exp(-T*exact(p)):.4f}")
for tgt in (0.9, 0.5, 0.1, 0.01):
    pe, pa = solve(tgt, exact), solve(tgt, approx)
    print(f"valid {tgt:.2f}: exact at {8000*pe:.2f} lost/s, approx at {8000*pa:.2f} lost/s")
p3 = 3e-5
print(f"round 3: p=3e-5 -> {8000*p3:.2f}/s, one per {1/(8000*p3):.2f} s, valid {math.exp(-T*8000*p3):.3f}")
r1 = -math.log(0.01) / T
print(f"round 3: 1 % at {r1:.3f} lost/s")
fill = (300 - T) / 300
for p, rows in ((1e-4, (1, 0.98)), (1e-3, (41, 0.55))):
    print(f"300 s at p={p:g}: expected restarts {exact(p)*300:.2f} (approx {approx(p)*300:.2f}); "
          f"expected valid {math.exp(-T*exact(p))*fill:.3f}; round-4 row {rows}")
print(f"fill factor {fill:.4f}")
