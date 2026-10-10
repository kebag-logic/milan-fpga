#!/usr/bin/env python3
"""argv[1] = KL_maap.sv, argv[2] = i: find a seed s (bit i clear, so s+2^i flips only
bit i) whose first block overlaps that of s+2^i; print 'mac clock' lines (clock 0)."""
import re, sys
src = open(sys.argv[1]).read(); i = int(sys.argv[2])
m = re.search(r"OFFSET_FOLD_C\s*=\s*\{[^\n]*\n(.*?)\};", src, re.S)
OFF = list(reversed([int(w.replace("_", ""), 16) for w in re.findall(r"32'h([0-9A-Fa-f_]+)", m.group(1))]))
par = lambda x: bin(x).count("1") & 1
step = lambda s: ((s << 1) & 0xFFFFFFFF) | (((s >> 31) ^ (s >> 21) ^ (s >> 1) ^ s) & 1)
def first(seed):
    o = sum(par(step(seed) & r) << k for k, r in enumerate(OFF)); o = o - 0xFE00 if o >= 0xFE00 else o
    return min(o, 0xFE00 - 8)
for s in range(1, 1 << 24):
    s = (s * 2654435761) & 0xFFFFFFFF & ~(1 << i)
    if s and abs(first(s) - first(s + (1 << i))) < 8:
        for v in (s, s + (1 << i)): print("%012x 00000000" % (0x020000000000 | v))
        break
