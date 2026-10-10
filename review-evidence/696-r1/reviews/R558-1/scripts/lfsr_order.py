#!/usr/bin/env python3
"""Independent order check of the KL_maap 32-bit generator step.

Models lfsr_next = {s[30:0], s[31]^s[21]^s[1]^s[0]} as a 32x32 GF(2) matrix
built from the RTL expression (not from the harness), and checks that its
order is exactly 2^32 - 1 (prime factors 3, 5, 17, 257, 65537).
"""
N = 32


def step(s):
    fb = ((s >> 31) ^ (s >> 21) ^ (s >> 1) ^ s) & 1
    return ((s << 1) & 0xFFFFFFFF) | fb


cols = [step(1 << b) for b in range(N)]


def apply(m, s):
    r = 0
    b = 0
    while s:
        if s & 1:
            r ^= m[b]
        s >>= 1
        b += 1
    return r


def square(m):
    return [apply(m, m[b]) for b in range(N)]


def power_apply(m, s, e):
    while e:
        if e & 1:
            s = apply(m, s)
        m = square(m)
        e >>= 1
    return s


# Linearity spot check against the direct step
import random
rnd = random.Random(696)
lin = all(apply(cols, x) == step(x) for x in (rnd.getrandbits(32) for _ in range(1000)))
P = (1 << 32) - 1
full = power_apply(cols, 1, P) == 1
proper = all(power_apply(cols, 1, P // q) != 1 for q in (3, 5, 17, 257, 65537))
assert 3 * 5 * 17 * 257 * 65537 == P
print(f"linear={lin} returns_after_2^32-1={full} no_shorter_divisor_period={proper}")
print("RESULT:", "maximal period 2^32-1" if lin and full and proper else "NOT MAXIMAL")
raise SystemExit(0 if lin and full and proper else 1)
