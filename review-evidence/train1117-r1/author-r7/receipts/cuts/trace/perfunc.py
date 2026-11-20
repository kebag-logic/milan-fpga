#!/usr/bin/env python3
"""perfunc.py MAP LOG PCS [N]: the dearest N aecp_mbx:frame record spans of a group log, each split by function:
committed instructions (PC lines inside the span) and cycles (each PC charged the CPU cycles to the next PC), per
`.text.<function>` section of the image's link map, by its object stem."""
import bisect
import re
import sys
from collections import Counter

SECTION = re.compile(r"^ \.text\.(\S+)\s+(0x[0-9a-f]+)\s+(0x[0-9a-f]+)\s+\S*/"
                     r"(?:\d+-([A-Za-z0-9_]+)\.o|([A-Za-z0-9_.]+\.a)\(([A-Za-z0-9_]+)\.o\))$", re.M)
text = open(sys.argv[1]).read()
body = text[text.index('Linker script and memory map'):]
spans = sorted((int(a, 16), int(a, 16) + int(n, 16), (s or f'{ar}:{m}') + ' ' + name)
               for name, a, n, s, ar, m in SECTION.findall(body) if int(n, 16))
starts = [s[0] for s in spans]
def fn(pc):
    k = bisect.bisect_right(starts, pc) - 1
    return spans[k][2] if k >= 0 and spans[k][0] <= pc < spans[k][1] else f'?{pc:08x}'
recs = [(int(l.split()[3]), int(l.split()[2])) for l in open(sys.argv[2]) if l.startswith('SPAN') and l.split()[-1] == 'aecp_mbx:frame']
pcs = [(int(f[1]), int(f[2], 16)) for f in (l.split() for l in open(sys.argv[3])) if len(f) == 3 and f[0] == 'PC']
cpus = [c for c, _ in pcs]
for cycles, start in sorted(recs, reverse=True)[:int(sys.argv[4]) if len(sys.argv) > 4 else 2]:
    a, b = bisect.bisect_left(cpus, start), bisect.bisect_left(cpus, start + cycles)
    if b - a < 10:
        print(f'record at {start}: {cycles} cycles, not in the trace'); continue
    ins, cyc = Counter(), Counter()
    for k in range(a, b):
        f = fn(pcs[k][1]); ins[f] += 1
        cyc[f] += (pcs[k + 1][0] if k + 1 < len(pcs) else start + cycles) - pcs[k][0]
    print(f'record at cpu {start}: {cycles} cycles, {b - a} instructions traced, {sum(cyc.values())} cycles charged')
    for f, n in ins.most_common(30):
        print(f'  {n:7d} instr {cyc[f]:8d} cyc  cpi {cyc[f] / n:5.2f}  {f}')
