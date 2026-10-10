#!/usr/bin/env python3
# [R558] R558-7: do the fold properties also hold WITHOUT the generator step?
# If yes, an unstepped-fold defect is property-equivalent and only a golden
# value can grade the step. argv[1] = KL_maap.sv
import re, sys
import numpy as np
src = open(sys.argv[1]).read()
def rows(name, n):
    m = re.search(name + r"\s*=\s*\{[^\n]*\n(.*?)\};", src, re.S)
    v = [int(x.replace("_", ""), 16) for x in re.findall(r"32'h([0-9A-Fa-f_]+)", m.group(1))]
    return list(reversed(v))
OFF = rows("OFFSET_FOLD_C", 16); PRB = rows("PROBE_FOLD_C", 6)
def fold(rws, s): return sum((bin(s & r).count("1") & 1) << i for i, r in enumerate(rws))
POOL = 0xFE00
W = np.arange(65536, dtype=np.int64)
def ro(w, c): return np.minimum(np.where(w >= POOL, w - POOL, w), POOL - c)
runs = [((1 << (j + 1)) - (1 << i)) & 0xFFFFFFFF for i in range(32) for j in range(i, 32)]
bad = 0
for d in runs:
    delta = fold(OFF, d)
    for c in range(1, 9):
        if (np.abs(ro(W, c) - ro(W ^ delta, c)) < c).any(): bad += 1; break
pz = sum(fold(PRB, d) == 0 for d in runs)
print(f"unstepped offset fold: carry runs violating disjointness: {bad}/528")
print(f"unstepped probe fold: carry runs with equal first probe draw: {pz}/528")
