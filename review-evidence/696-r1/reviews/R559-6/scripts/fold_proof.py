#!/usr/bin/env python3
"""Exhaustive check of the KL_maap first-draw fold claims (#696 round 6).

Reads OFFSET_FOLD_C / PROBE_FOLD_C from the RTL given as argv[1] and checks:
 A. for every carry run d = bits i..j (s and s+2^i mod 2^32 differ by d),
    D = offset_fold(step(d)); for EVERY 16-bit word X and every count 1..8,
    rand_offset(X) and rand_offset(X^D) give disjoint [o, o+count) blocks;
 B. probe_fold(step(d)) != 0 for every such d (first intervals differ);
 C. the map seed bits 16..31 -> offset_fold(step(seed)) is a bijection;
 D. the 22 fold rows are linearly independent over GF(2).
The step is linear over GF(2), so step(s)^step(s') = step(s^s').
"""
import re, sys
import numpy as np

src = open(sys.argv[1]).read()
def rows(name, n):
    m = re.search(name + r"\s*=\s*\{[^\n]*\n(.*?)\};", src, re.S)
    words = [int(w.replace("_", ""), 16) for w in re.findall(r"32'h([0-9A-Fa-f_]+)", m.group(1))]
    assert len(words) == n, (name, len(words))
    return list(reversed(words))  # listed rows n-1..0
OFF = rows("OFFSET_FOLD_C", 16); PRB = rows("PROBE_FOLD_C", 6)
par = lambda x: bin(x).count("1") & 1
step = lambda s: ((s << 1) & 0xFFFFFFFF) | (((s >> 31) ^ (s >> 21) ^ (s >> 1) ^ s) & 1)
fold = lambda s, R: sum(par(s & r) << i for i, r in enumerate(R))
POOL = 0xFE00
X = np.arange(65536, dtype=np.int64)
def ro(v, cnt):
    o = np.where(v >= POOL, v - POOL, v)
    return np.minimum(o, POOL - cnt)
bad = 0; probe_bad = 0; runs = 0; mind = 1 << 20
for i in range(32):
    for j in range(i, 32):
        d = ((1 << (j + 1)) - 1) ^ ((1 << i) - 1); runs += 1
        D = fold(step(d), OFF)
        for cnt in range(1, 9):
            gap = np.abs(ro(X, cnt) - ro(X ^ D, cnt))
            mind = min(mind, int(gap.min()) - cnt)
            if (gap < cnt).any():
                bad += 1; print("OVERLAP run", i, j, "D=%04x cnt %d" % (D, cnt)); break
        if fold(step(d), PRB) == 0:
            probe_bad += 1; print("PROBE EQUAL run", i, j)
words = {fold(step(h << 16), OFF) for h in range(65536)}
def rank(vs):
    vs = list(vs); r = 0
    for bit in range(31, -1, -1):
        piv = next((k for k in range(r, len(vs)) if vs[k] >> bit & 1), None)
        if piv is None: continue
        vs[r], vs[piv] = vs[piv], vs[r]
        for k in range(len(vs)):
            if k != r and vs[k] >> bit & 1: vs[k] ^= vs[r]
        r += 1
    return r
print("A carry runs checked:", runs, "overlapping runs:", bad, "min spare gap:", mind)
print("B probe-equal runs:", probe_bad)
print("C distinct offset words from bits 16..31:", len(words), "(bijective)" if len(words) == 65536 else "(NOT bijective)")
print("D rank of 22 rows:", rank(OFF + PRB))
sys.exit(0 if (bad == 0 and probe_bad == 0 and len(words) == 65536 and rank(OFF + PRB) == 22) else 1)
