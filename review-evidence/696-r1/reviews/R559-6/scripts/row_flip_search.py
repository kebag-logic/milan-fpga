#!/usr/bin/env python3
"""For every single-bit flip of OFFSET_FOLD_C in argv[1], compare (a) the universal
claim 'seeds 2^i apart (any carry) claim disjoint first 8-address blocks' (all X) and
the bits-16..31 bijection with (b) a model of the suite's section [12] sampled pairs
(same LCG and pair construction as tb/verilator/maap/sim_main.cpp). Lists flips that
break (a) while (b) still passes."""
import re, sys
import numpy as np
src = open(sys.argv[1]).read()
m = re.search(r"OFFSET_FOLD_C\s*=\s*\{[^\n]*\n(.*?)\};", src, re.S)
OFF0 = list(reversed([int(w.replace("_", ""), 16) for w in re.findall(r"32'h([0-9A-Fa-f_]+)", m.group(1))]))
M32 = 0xFFFFFFFF
par = lambda x: bin(x).count("1") & 1
step = lambda s: ((s << 1) & M32) | (((s >> 31) ^ (s >> 21) ^ (s >> 1) ^ s) & 1)
def first(seed, R):
    seed = seed or 0xACE1
    o = sum(par(step(seed) & r) << i for i, r in enumerate(R)); o = o - 0xFE00 if o >= 0xFE00 else o
    return min(o, 0xFE00 - 8)
# suite pairs as seeds
pairs = [(0x1, 0x2), (0x10001, 0x00001), (0x0a1234 + 7, 0x5b1234 + 7), (0x11001234, 0x22001234)]
s = 0x2545f491
for i in range(32):
    for j in range(i, 32):
        s = (s * 1664525 + 1013904223) & M32
        ones = ((1 << j) - (1 << i)) & M32
        seed = (s | ones) & ~(1 << j) & M32
        pairs.append((seed, (seed + (1 << i)) & M32))
X = np.arange(65536, dtype=np.int64)
def ro(v): o = np.where(v >= 0xFE00, v - 0xFE00, v); return np.minimum(o, 0xFE00 - 8)
def universal(R):
    for i in range(32):
        for j in range(i, 32):
            d = ((1 << (j + 1)) - 1) ^ ((1 << i) - 1)
            D = sum(par(step(d) & r) << k for k, r in enumerate(R))
            if (np.abs(ro(X) - ro(X ^ D)) < 8).any(): return f"overlap run {i}..{j}"
    if len({sum(par(step(h << 16) & r) << k for k, r in enumerate(R)) for h in range(65536)}) != 65536:
        return "bits 16..31 not one-to-one"
    return None
def suite_ok(R):
    return all(abs(first(a, R) - first(b, R)) >= 8 for a, b in pairs)
assert universal(OFF0) is None and suite_ok(OFF0)
escapes = []
for row in range(16):
    for bit in range(32):
        R = list(OFF0); R[row] ^= 1 << bit
        u = universal(R)
        if u and suite_ok(R): escapes.append((row, bit, u))
print("single-bit row flips:", 16 * 32, "breaking a universal claim yet passing the sampled pairs:", len(escapes))
for e in escapes[:10]: print("  row %d bit %d: %s" % e)
