#!/usr/bin/env python3
# [R558] R558-7: model the first Begin! offset/probe draw from the RTL fold rows for
# R558-6's four MAC pairs (clock 0, count 8); compare with the PR body's figures.
import re, sys
src = open(sys.argv[1]).read()
def rows(name):
    m = re.search(name + r"\s*=\s*\{[^\n]*\n(.*?)\};", src, re.S)
    return list(reversed([int(x.replace("_", ""), 16) for x in re.findall(r"32'h([0-9A-Fa-f_]+)", m.group(1))]))
OFF, PRB = rows("OFFSET_FOLD_C"), rows("PROBE_FOLD_C")
M = 0xFFFFFFFF
step = lambda s: ((s << 1) & M) | (((s >> 31) ^ (s >> 21) ^ (s >> 1) ^ s) & 1)
fold = lambda r, s: sum((bin(s & x).count("1") & 1) << i for i, x in enumerate(r))
def first(mac, clock=0, cnt=8):
    seed = (mac + clock) & M or 0xACE1
    w = fold(OFF, step(seed)); o = w - 0xFE00 if w >= 0xFE00 else w
    return min(o, 0xFE00 - cnt), 518 + fold(PRB, step(seed))
pairs = [(0x020000000001, 0x020000000002), (0x020000000001, 0x020000010001),
         (0x0200000a1234, 0x0200005b1234), (0x020011001234, 0x020022001234)]
for a, b in pairs:
    (oa, pa), (ob, pb) = first(a), first(b)
    print(f"{a:012x}/{b:012x}: offsets 0x{oa:04x}/0x{ob:04x} {'disjoint' if abs(oa-ob) >= 8 else 'OVERLAP'}; first probe ms {pa}/{pb}")
