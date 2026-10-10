#!/usr/bin/env python3
"""Independent check: the KL_maap step {r[30:0], r31^r21^r1^r0} has order 2^32-1
(x^32+x^22+x^2+x+1 family). Built from the RTL expression by hand, not from the harness."""
def step(r):
    fb = ((r >> 31) ^ (r >> 21) ^ (r >> 1) ^ r) & 1
    return ((r << 1) & 0xFFFFFFFF) | fb
cols = [step(1 << b) for b in range(32)]
def apply(m, s):
    out = 0
    for b in range(32):
        if s >> b & 1: out ^= m[b]
    return out
def mul(a, b):  # a after b
    return [apply(a, b[k]) for k in range(32)]
def power(m, n):
    res = [1 << b for b in range(32)]
    while n:
        if n & 1: res = mul(m, res)
        m = mul(m, m); n >>= 1
    return res
N = 2**32 - 1
ident = [1 << b for b in range(32)]
full = power(cols, N) == ident
proper = all(power(cols, N // q) != ident for q in (3, 5, 17, 257, 65537))
for s in (1, 0x12345678, 0xDEADBEEF):
    assert apply(cols, s) == step(s)
print("order divides 2^32-1:", full, " no proper divisor:", proper, " => maximal:", full and proper)
# the RTL seed sum vs B.3.6.1: low 32 bits of (48-bit MAC + clock) == mac[31:0] + clock mod 2^32
import random
ok = all(((m + c) & 0xFFFFFFFF) == (((m & 0xFFFFFFFF) + c) & 0xFFFFFFFF)
         for m, c in ((random.getrandbits(48), random.getrandbits(32)) for _ in range(10000)))
print("low-32 of full sum equals sum of low-32 operands:", ok)
raise SystemExit(0 if full and proper and ok else 1)
