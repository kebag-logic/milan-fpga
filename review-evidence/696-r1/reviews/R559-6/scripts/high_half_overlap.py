#!/usr/bin/env python3
"""Count MAC pairs (equal clock 0, equal MAC bits 0..15) differing only in
bits 16..31 whose first 8-address blocks overlap, and print one example.
argv[1] = KL_maap.sv. Model of the RTL first draw: rand_offset(offset_fold(step(seed)), 8)."""
import re, sys
src = open(sys.argv[1]).read()
m = re.search(r"OFFSET_FOLD_C\s*=\s*\{[^\n]*\n(.*?)\};", src, re.S)
OFF = list(reversed([int(w.replace("_", ""), 16) for w in re.findall(r"32'h([0-9A-Fa-f_]+)", m.group(1))]))
par = lambda x: bin(x).count("1") & 1
step = lambda s: ((s << 1) & 0xFFFFFFFF) | (((s >> 31) ^ (s >> 21) ^ (s >> 1) ^ s) & 1)
fold = lambda s: sum(par(s & r) << i for i, r in enumerate(OFF))
def first(seed):
    seed = seed or 0xACE1
    o = fold(step(seed)); o = o - 0xFE00 if o >= 0xFE00 else o
    return min(o, 0xFE00 - 8)
low = 0x1234
base = first((0x0001 << 16) | low)
hits = [h for h in range(65536) if h != 1 and abs(first((h << 16) | low) - base) < 8]
print("pairs vs 02:00:00:01:12:34 overlapping:", len(hits), "of 65535")
if hits:
    h = hits[0]
    print("example: 02:00:00:01:12:34 -> 0x%04x ; 02:00:%02x:%02x:12:34 -> 0x%04x" % (base, h >> 8, h & 255, first((h << 16) | low)))
