#!/usr/bin/env python3
"""argv[1] = KL_maap.sv. Finds MAC pairs (clock 0, MAC bits 0..15 = 0x1234) that differ
only in bits 16..31 and claim IDENTICAL first 8-address blocks under the RTL model,
and prints the count and the first pair as 'mac clock' lines to argv[2]."""
import re, sys
src = open(sys.argv[1]).read()
m = re.search(r"OFFSET_FOLD_C\s*=\s*\{[^\n]*\n(.*?)\};", src, re.S)
OFF = list(reversed([int(w.replace("_", ""), 16) for w in re.findall(r"32'h([0-9A-Fa-f_]+)", m.group(1))]))
par = lambda x: bin(x).count("1") & 1
step = lambda s: ((s << 1) & 0xFFFFFFFF) | (((s >> 31) ^ (s >> 21) ^ (s >> 1) ^ s) & 1)
fold = lambda s: sum(par(s & r) << i for i, r in enumerate(OFF))
def first(seed):
    o = fold(step(seed)); o = o - 0xFE00 if o >= 0xFE00 else o
    return min(o, 0xFE00 - 8)
by = {}
for h in range(65536):
    by.setdefault(first((h << 16) | 0x1234), []).append(h)
coll = [v for v in by.values() if len(v) > 1]
print("first offsets shared by >1 high half:", len(coll))
h1, h2 = coll[0][:2]
with open(sys.argv[2], "w") as f:
    for h in (h1, h2): f.write("%012x 00000000\n" % (0x020000000000 | (h << 16) | 0x1234))
print("pair: %012x %012x" % (0x020000000000 | (h1 << 16) | 0x1234, 0x020000000000 | (h2 << 16) | 0x1234))
