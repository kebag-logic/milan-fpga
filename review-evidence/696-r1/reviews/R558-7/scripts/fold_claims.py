#!/usr/bin/env python3
# [R558] R558-7 independent check of the KL_maap first-draw fold claims.
# Reads the fold rows from the RTL given as argv[1] (no repository code is run).
# Checks, exhaustively where the claim is universal:
#  C1 LFSR x^32+x^22+x^2+x+1 has period 2^32-1 (primitive polynomial test)
#  C2 the 22 fold rows (16 offset + 6 probe) are linearly independent
#  C3 seed bits 16..31 map one-to-one onto the offset word (via the step)
#  C4 for every carry run d (528), every offset word w (65536), count 1..8:
#     rand_offset(w) and rand_offset(w ^ delta) blocks share no address
#  C5 every carry run gives a different first probe fold
#  C6 Monte-Carlo overlap rate of pairs not a power of two apart (count 8)
import re, sys, random

src = open(sys.argv[1]).read()
def rows(name, n):
    m = re.search(name + r"\s*=\s*\{[^\n]*\n(.*?)\};", src, re.S)
    vals = [int(v.replace("_", ""), 16) for v in re.findall(r"32'h([0-9A-Fa-f_]+)", m.group(1))]
    assert len(vals) == n, (name, len(vals))
    return list(reversed(vals))  # listed rows n-1..0 -> index i = row i
OFF = rows("OFFSET_FOLD_C", 16)
PRB = rows("PROBE_FOLD_C", 6)
M32 = 0xFFFFFFFF
def step(s): return ((s << 1) & M32) | (((s >> 31) ^ (s >> 21) ^ (s >> 1) ^ s) & 1)
def fold(rws, s): return sum((bin(s & r).count("1") & 1) << i for i, r in enumerate(rws))
POOL = 0xFE00
def rand_offset(w, c):
    o = w - POOL if w >= POOL else w
    return min(o, POOL - c)

ok = True
def report(name, cond, detail=""):
    global ok
    ok &= cond
    print(f"[{'PASS' if cond else 'FAIL'}] {name} {detail}")

# C1: order of x in GF(2)[x]/(p) is 2^32-1 iff x^(2^32-1)=1 and x^((2^32-1)/q)!=1
P = (1 << 32) | (1 << 22) | (1 << 2) | (1 << 1) | 1
def mulmod(a, b):
    r = 0
    while b:
        if b & 1: r ^= a
        b >>= 1; a <<= 1
        if a >> 32: a ^= P
    return r
def powx(e):
    r, b = 1, 2
    while e:
        if e & 1: r = mulmod(r, b)
        b = mulmod(b, b); e >>= 1
    return r
N = (1 << 32) - 1
primes = [3, 5, 17, 257, 65537]
report("C1 period 2^32-1", powx(N) == 1 and all(powx(N // q) != 1 for q in primes))
# also confirm the RTL step is the companion of that polynomial: walk 2^20 states, no repeat of seed
s0 = 0xACE1; s = s0; rep = False
for _ in range(1 << 20):
    s = step(s)
    if s == s0: rep = True; break
report("C1b no short cycle within 2^20 steps from 0xACE1", not rep)

def rank(vecs):
    basis = []
    for v in vecs:
        for b in basis: v = min(v, v ^ b)
        if v: basis.append(v)
    return len(basis)
report("C2 22 rows independent", rank(OFF + PRB) == 22, f"rank={rank(OFF + PRB)}")

# the composite linear map seed -> offset word: column k = fold(step(e_k)) (step is linear)
def offmap(d): return fold(OFF, step(d))
def prbmap(d): return fold(PRB, step(d))
cols_hi = [offmap(1 << k) for k in range(16, 32)]
report("C3 bits 16..31 one-to-one onto offset word", rank(cols_hi) == 16, f"rank={rank(cols_hi)}")

runs = []
for i in range(32):
    for j in range(i, 32):
        runs.append(((1 << (j + 1)) - (1 << i)) & M32)
deltas = sorted({offmap(d) for d in runs})
import numpy as np
W = np.arange(65536, dtype=np.int64)
def ro_vec(w, c):
    o = np.where(w >= POOL, w - POOL, w)
    return np.minimum(o, POOL - c)
bad = []
for d in runs:
    delta = offmap(d)
    for c in range(1, 9):
        diff = np.abs(ro_vec(W, c) - ro_vec(W ^ delta, c))
        idx = np.nonzero(diff < c)[0]
        if idx.size:
            bad.append((hex(d), hex(delta), c, hex(int(idx[0])), int(idx.size))); break
report("C4 all 528 carry runs x 65536 words x count 1..8 disjoint", not bad,
       f"violations(first per run)={len(bad)} {bad[:5]}")
pz = [hex(d) for d in runs if prbmap(d) == 0]
report("C5 all 528 carry runs change first probe fold", not pz, f"zero={pz[:5]}")

# C6 Monte-Carlo, count 8, seed pairs s, s+k with k not a power of two (k != 0)
rnd = random.Random(696)
trials = 400000; hits = 0
for _ in range(trials):
    s = rnd.getrandbits(32) or 1
    while True:
        k = rnd.getrandbits(32)
        if k and (k & (k - 1)): break
    t = (s + k) & M32
    if t == 0: continue
    a = rand_offset(offmap(s), 8); b = rand_offset(offmap(t), 8)
    hits += abs(a - b) < 8
rate = hits / trials
print(f"[INFO] C6 overlap rate non-power-of-two pairs: {hits}/{trials} = {rate*65024:.2f} per 65024 (doc: about 15)")
report("C6 rate within 10..20 per 65024", 10 <= rate * 65024 <= 20)
print("RESULT:", "ALL PASS" if ok else "FAILURES")
sys.exit(0 if ok else 1)
