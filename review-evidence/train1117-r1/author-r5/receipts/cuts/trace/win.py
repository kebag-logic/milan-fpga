"""win.py MAP PCS START_CPU CYCLES [N]: committed PCs in [START, START+CYCLES) split by function, hot or cold."""
import bisect, re, sys
from collections import Counter
SECTION = re.compile(r"^ \.text\.(\S+)\s+(0x[0-9a-f]+)\s+(0x[0-9a-f]+)\s+\S*/(?:\d+-([A-Za-z0-9_]+)\.o|([A-Za-z0-9_.]+\.a)\(([A-Za-z0-9_]+)\.o\))$", re.M)
text = open(sys.argv[1]).read(); body = text[text.index('Linker script and memory map'):]
hs = re.search(r'0x([0-9a-f]+)\s+_ctrl_hot_start = \.', body); he = re.search(r'0x([0-9a-f]+)\s+_ctrl_hot_end = \.', body)
hot = (int(hs[1], 16), int(he[1], 16))
spans = sorted((int(a, 16), int(a, 16) + int(n, 16), (s or f'{ar}:{m}') + ' ' + f) for f, a, n, s, ar, m in SECTION.findall(body) if int(n, 16))
starts = [x[0] for x in spans]
def fn(pc):
    k = bisect.bisect_right(starts, pc) - 1
    return spans[k][2] if k >= 0 and spans[k][0] <= pc < spans[k][1] else f'?{pc:08x}'
start, cycles = int(sys.argv[3]), int(sys.argv[4]); top = int(sys.argv[5]) if len(sys.argv) > 5 else 30
pcs = [(int(f[1]), int(f[2], 16)) for f in (l.split() for l in open(sys.argv[2])) if len(f) == 3]
cpus = [c for c, _ in pcs]; a, b = bisect.bisect_left(cpus, start), bisect.bisect_left(cpus, start + cycles)
ins, cyc, where = Counter(), Counter(), {}
for k in range(a, b):
    f = fn(pcs[k][1]); ins[f] += 1; cyc[f] += (pcs[k + 1][0] if k + 1 < len(pcs) else start + cycles) - pcs[k][0]
    where[f] = 'hot' if hot[0] <= pcs[k][1] < hot[1] else 'cold'
print(f'window {start}+{cycles}: {b - a} instructions, {sum(cyc.values())} cycles; cold {sum(c for f, c in cyc.items() if where[f] == "cold")} cycles')
for f, n in cyc.most_common(top):
    print(f'  {ins[f]:6d} instr {n:7d} cyc cpi {n / ins[f]:5.2f} {where[f]:4s} {f}')
