#!/usr/bin/env python3
"""xorshift_pairs.py - the stack's ADP draw (tsn-c-stack src/adp.c rng_next, draw_ms: xorshift32 13/17/5, the top
16 bits scaled to 0..max) taken in G4's order, a LINK_UP draw then a grandmaster change's draw per link-up, 32
link-ups, from many random seeds: how often the 32 second draws split as unevenly as 6 / 26 between the halves
of 0 to 4 s, against an independent fair draw's binomial tail."""
import random
from math import comb

def nxt(x):
    x ^= (x << 13) & 0xffffffff
    x ^= x >> 17
    x ^= (x << 5) & 0xffffffff
    return x

def draw(x, mx=4000):
    return ((x >> 16) * (mx + 1)) >> 16

random.seed(972)
trials, extreme = 200000, 0
for _ in range(trials):
    x = random.getrandbits(32) or 1
    upper = 0
    for _ in range(32):
        x = nxt(x)            # LINK_UP draw
        x = nxt(x)            # grandmaster change draw
        upper += draw(x) >= 2001
    extreme += upper >= 26 or upper <= 6
fair = sum(comb(32, k) for k in list(range(0, 7)) + list(range(26, 33))) / 2 ** 32
print(f"trials {trials}: split at least as uneven as 6/26 in {extreme} ({extreme / trials:.5f}); "
      f"an independent fair draw: {fair:.5f}")
