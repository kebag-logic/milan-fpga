#!/usr/bin/env python3
"""argv[1] = (mutated) KL_maap.sv; prints the bits-16..31 kernel of its first-draw
fold and a MAC pair (clock 0) that differs only in bits 16..31; argv[2] optional
file of 'mac clock' lines to model (prints the model's first offsets)."""
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
if len(sys.argv) > 2:
    for line in open(sys.argv[2]):
        mac, clk = (int(x, 16) for x in line.split())
        print("%012x %08x 0x%04x" % (mac, clk, first(((mac & 0xFFFFFFFF) + clk) & 0xFFFFFFFF)))
    sys.exit(0)
ker = [h for h in range(1, 65536) if fold(step(h << 16)) == 0]
print("kernel:", ["%04x" % h for h in ker[:4]], "count", len(ker))
if ker:
    a = 0x020000001234; b = a ^ (ker[0] << 16)
    print("pair %012x %012x" % (a, b))
