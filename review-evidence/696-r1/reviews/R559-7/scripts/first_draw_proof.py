#!/usr/bin/env python3
"""Independent exhaustive check of the #696 first-draw claims from KL_maap.sv.

Usage: python3 -I first_draw_proof.py <path/to/KL_maap.sv>

Parses OFFSET_FOLD_C, PROBE_FOLD_C, POOL_SIZE_C and the lfsr_step taps from
the RTL text (no constant restated), then checks, for the stepped seed:
  A. every carry run d (bits i..j, 528 runs) against every 16-bit word w and
     every count 1..8: rand_offset(w) and rand_offset(w ^ W(d)) are >= count apart;
  B. every carry run draws a different first probe fold (P(step(d)) != 0);
  C. seed bits 16..31 map one-to-one onto the offset word (rank 16);
  D. the 16 offset rows and 6 probe rows after the step are independent (rank 22);
  E. the offset map has full rank 16 (every word reachable);
  F. empirical overlap rate of two independent uniform words, count 8.
Prints one PASS/FAIL line per property; exit 0 only if A-E pass.
"""
import re
import sys

import numpy as np

text = open(sys.argv[1]).read()


def rows(name, n):
    m = re.search(name + r"\s*=\s*\{[^}]*\}", text)
    vals = re.findall(r"32'h([0-9A-Fa-f_]+)", m.group(0))
    vals = [int(v.replace("_", ""), 16) for v in vals]
    assert len(vals) == n, (name, len(vals))
    return list(reversed(vals))  # listed rows n-1..0


OFF = rows("OFFSET_FOLD_C", 16)
PRB = rows("PROBE_FOLD_C", 6)
pool = int(re.search(r"POOL_SIZE_C\s*=\s*16'h([0-9A-Fa-f]+)", text).group(1), 16)
taps_expr = re.search(r"lfsr_step = \{s\[30:0\], ([^}]*)\};", text).group(1)
taps = [int(t) for t in re.findall(r"s\[(\d+)\]", taps_expr)]
print(f"[i] pool=0x{pool:04X} taps={taps} offset_rows={[hex(r) for r in OFF]} probe_rows={[hex(r) for r in PRB]}")


def par(x):
    return bin(x).count("1") & 1


def step(s):
    fb = 0
    for t in taps:
        fb ^= (s >> t) & 1
    return ((s << 1) & 0xFFFFFFFF) | fb


def fold(s, rws):
    return sum(par(s & r) << i for i, r in enumerate(rws))


def W(s):
    return fold(step(s), OFF)


def P(s):
    return fold(step(s), PRB)


def rank(vecs):
    basis = []
    for v in vecs:
        for b in basis:
            v = min(v, v ^ b)
        if v:
            basis.append(v)
    return len(basis)


def rand_offset(w, cnt):
    o = np.where(w >= pool, w - pool, w)
    lim = pool - cnt
    return np.where(o > lim, lim, o)


ok = True
words = np.arange(1 << 16, dtype=np.int64)
ro = {c: rand_offset(words, c) for c in range(1, 9)}
worst = 1 << 16
bad_a = 0
bad_b = 0
for i in range(32):
    for j in range(i, 32):
        d = ((1 << (j + 1)) - (1 << i)) & 0xFFFFFFFF
        D = W(d)
        if P(d) == 0:
            bad_b += 1
        for c in range(1, 9):
            gap = np.abs(ro[c] - ro[c][words ^ D])
            worst = min(worst, int(gap.min()) - c)
            bad_a += int((gap < c).sum())
print(f"{'PASS' if bad_a == 0 else 'FAIL'} A every carry run x every word x counts 1..8 disjoint "
      f"(violations {bad_a}, least spare {worst})")
print(f"{'PASS' if bad_b == 0 else 'FAIL'} B every carry run draws a different first probe fold (violations {bad_b})")
r16 = rank([W(1 << k) for k in range(16, 32)])
print(f"{'PASS' if r16 == 16 else 'FAIL'} C seed bits 16..31 -> offset word rank {r16}")
r22 = rank([W(1 << k) | (P(1 << k) << 16) for k in range(32)])
print(f"{'PASS' if r22 == 22 else 'FAIL'} D offset+probe joint rank {r22}")
rw = rank([W(1 << k) for k in range(32)])
print(f"{'PASS' if rw == 16 else 'FAIL'} E offset map rank {rw}")
ok = bad_a == 0 and bad_b == 0 and r16 == 16 and r22 == 22 and rw == 16
a = ro[8]
pairs = 0
rng = np.random.default_rng(696)
x = rng.integers(0, 1 << 16, 4_000_000)
y = rng.integers(0, 1 << 16, 4_000_000)
rate = float((np.abs(a[x] - a[y]) < 8).mean())
print(f"[i] F two independent words, count 8: overlap rate {rate:.6f} = {rate * 65024:.1f} in 65,024")
# Fixed pairs from the docs: MACs differing only in bits 32..47 share the seed.
print("[i] seed uses station_mac_i[31:0] only; MACs differing only in bits 32..47 share a seed at an equal clock")
sys.exit(0 if ok else 1)
