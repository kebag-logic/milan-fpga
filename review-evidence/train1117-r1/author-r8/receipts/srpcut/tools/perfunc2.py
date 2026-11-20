"""perfunc2.py MAP PCS CPU_START CYCLES [N]: one span of a traced group split by function (#665's ruling of
2026-11-20, item 3: where 8x8/1if's SRP record and reclaim cycles go). Each committed PC (sim_main.cpp's PC lines:
CPU cycle, address) is charged the CPU cycles to the next one, and each is put to the `.text.<function>` section of
the image's link map holding it, marked hot (inside _ctrl_hot_start.._ctrl_hot_end) or cold. Prints the N dearest
functions by cycles, with instructions and calls (entries from another function), and the cold total."""
import bisect
import re
import sys
from collections import Counter

SECTION = re.compile(r"^ \.text\.(\S+)\s+(0x[0-9a-f]+)\s+(0x[0-9a-f]+)\s+\S*/"
                     r"(?:\d+-([A-Za-z0-9_]+)\.o|([A-Za-z0-9_.]+\.a)\(([A-Za-z0-9_]+)\.o\))$", re.M)
text = open(sys.argv[1]).read()
body = text[text.index('Linker script and memory map'):]
hs = re.search(r'0x([0-9a-f]+)\s+_ctrl_hot_start = \.', body)
he = re.search(r'0x([0-9a-f]+)\s+_ctrl_hot_end = \.', body)
hot = (int(hs[1], 16), int(he[1], 16))
spans = sorted((int(a, 16), int(a, 16) + int(n, 16), (s or f'{ar}:{m}') + ' ' + f)
               for f, a, n, s, ar, m in SECTION.findall(body) if int(n, 16))
starts = [x[0] for x in spans]


def fn(pc):
    k = bisect.bisect_right(starts, pc) - 1
    return spans[k][2] if k >= 0 and spans[k][0] <= pc < spans[k][1] else f'?{pc:08x}'


start, cycles = int(sys.argv[3]), int(sys.argv[4])
top = int(sys.argv[5]) if len(sys.argv) > 5 else 40
pcs = []
for line in open(sys.argv[2]):
    f = line.split()
    if len(f) == 3 and f[0] == 'PC':
        pcs.append((int(f[1]), int(f[2], 16)))
cpus = [c for c, _ in pcs]
a, b = bisect.bisect_left(cpus, start), bisect.bisect_left(cpus, start + cycles)
ins, cyc, calls, where = Counter(), Counter(), Counter(), {}
last = None
for k in range(a, b):
    pc = pcs[k][1]
    f = fn(pc)
    ins[f] += 1
    cyc[f] += (pcs[k + 1][0] if k + 1 < len(pcs) else start + cycles) - pcs[k][0]
    where[f] = 'hot' if hot[0] <= pc < hot[1] else 'cold'
    if f != last:
        k2 = bisect.bisect_right(starts, pc) - 1
        if k2 >= 0 and spans[k2][0] == pc:
            calls[f] += 1
    last = f
print(f'span at cpu {start}: {cycles} cycles; {b - a} instructions traced, {sum(cyc.values())} cycles charged; '
      f'trace covers {pcs[0][0]}..{pcs[-1][0]}')
for f, n in cyc.most_common(top):
    print(f'  {n:7d} cyc {ins[f]:6d} instr {calls[f]:5d} calls cpi {n / ins[f]:5.2f} {where[f]:4s} {f}')
print(f"cold: {sum(c for f, c in cyc.items() if where[f] == 'cold')} cycles, "
      f"{sum(i for f, i in ins.items() if where[f] == 'cold')} instructions")
