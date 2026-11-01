#!/usr/bin/env python3
"""Cross-port conversion error of a redundant pair (lane evidence, round 4;
not a gate).

Derives the error between the two converted copies of one packet instead of
injecting it. Two networks run grandmaster time scales at frequency offsets
f0 and f1 (each within 100 ppm, IEEE 802.1AS-2020 B.1.1). On each network the
talker's and the listener's PHCs differ by a constant error within 1 us
(B.3). Every PHC read truncates to a 40 ns granule (B.1.2).

The talker captures at t_c, stamps at t_s >= t_c, and adds the PHC offset it
latched at its last 125 us latch, at or before t_s. The listener subtracts
the PHC offset it latched at its last latch at or before the arrival t_r.
Arrival is at most 2.792 ms after the stamp (assumption A4: the offset plus
Milan v1.2 5.3.7.6's 125 us, for offsets up to the 2.667 ms span).

Check: over adversarial and random cases, |P0 - P1'| stays within the page's
E_x = 2.000 + 0.584 + 0.160 = 2.744 us, and the drift-only worst case reaches
the drift term (so the term is not over-counted by more than the granules).
A mutant that books the drift over the latch age only (2 x 125 us, the
round-3 bound 2.210 us) must be exceeded.
Usage: python3 -I conversion_error.py
"""
import math
import random
import sys

PPM = 100e-6
SYNC = 1.0            # us, per network, talker vs listener PHC (B.3)
GRAN = 0.040          # us, PHC read granule (B.1.2)
LATCH = 125.0         # us, latch period at each end
A4 = 2792.0           # us, stamp to arrival at most
E_X = 2.744           # us, the page's bound
E_X_R3 = 2.210        # us, the round-3 bound


def q(x):
    return math.floor(x / GRAN) * GRAN


def err(f0, f1, e0, e1, t_c, ds, dr, age_a, age_b):
    """f: frequency offsets; e: talker minus listener PHC error per network;
    t_c capture; ds stamp delay; dr stamp-to-arrival; age_a, age_b: how long
    before the stamp and before the arrival each end last latched, in
    [0, 125) us."""
    T0 = lambda t: (1 + f0) * t
    T1 = lambda t: (1 + f1) * t + 12_345.678
    t_s = t_c + ds
    t_a = t_s - age_a                                          # talker latch
    t_r = t_s + dr
    t_b = t_r - age_b                                          # listener latch
    # talker PHCs carry the errors e; listener PHCs read the network time
    d_t = q(T1(t_a) + e1) - q(T0(t_a) + e0)
    d_l = q(T1(t_b)) - q(T0(t_b))
    p0 = q(T0(t_c) + e0) + 2000.0
    p1 = p0 + d_t
    p1_conv = p1 - d_l
    return abs(p1_conv - p0), t_b - t_a


def main():
    rnd = random.Random(7)
    worst = 0.0
    worst_case = None
    span = 0.0
    n = 0
    for f0, f1 in ((PPM, -PPM), (-PPM, PPM)):
        for e0, e1 in ((SYNC, -SYNC), (-SYNC, SYNC)):
            for dr in (0.0, 1.0, 1000.0, A4 - 1.0, A4):
                for ds in (0.0, 0.5, 60.0, 124.9):
                    for age_a in (0.0, 0.01, 62.5, 124.999):
                        for age_b in (0.0, 0.001, 62.5, 124.99):
                            t_c = rnd.uniform(1e5, 1e7)
                            e, sep = err(f0, f1, e0, e1, t_c, ds, dr, age_a, age_b)
                            n += 1
                            span = max(span, abs(sep))
                            if e > worst:
                                worst, worst_case = e, (f0, f1, e0, e1, dr, ds, age_a, age_b, sep)
    for _ in range(200_000):
        f0, f1 = rnd.uniform(-PPM, PPM), rnd.uniform(-PPM, PPM)
        e0, e1 = rnd.uniform(-SYNC, SYNC), rnd.uniform(-SYNC, SYNC)
        e, sep = err(f0, f1, e0, e1, rnd.uniform(1e5, 1e7), rnd.uniform(0, 125),
                     rnd.uniform(0, A4), rnd.uniform(0, LATCH), rnd.uniform(0, LATCH))
        n += 1
        span = max(span, abs(sep))
        if e > worst:
            worst, worst_case = e, (f0, f1, e0, e1, sep)
    drift_term = 2 * PPM * (LATCH + A4)
    print(f"cases: {n}")
    print(f"largest latch separation: {span:.3f} us (bound {LATCH + A4:.3f} us)")
    print(f"drift term: 200 ppm x {LATCH + A4:.0f} us = {drift_term:.4f} us")
    print(f"worst |P0 - P1'|: {worst:.4f} us at {worst_case}")
    print(f"page bound E_x = {E_X:.3f} us; round-3 bound {E_X_R3:.3f} us")
    ok = worst <= E_X and span <= LATCH + A4 + 1e-6
    ok &= worst > E_X_R3          # the latch-age-only bound is exceeded
    ok &= worst >= 2 * SYNC + drift_term - 2 * 2 * GRAN   # the term is reached
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
