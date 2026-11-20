#!/bin/bash
# trace_item.sh BUILD PART GROUP START_SYS CYCLES LABEL: one poll item of a measured leg traced by committed PC
# (from 2,000 bus cycles before its start for 40,000 PCs) and split by function over [start, start + cycles), the
# CPU's cycle being the bus cycle less 64 (the SPAN lines' two columns). Scratch only.
set -u
T=<scratch>; . $T/bin/env.sh
B=$1 K=$2 G=$3 S=$4 N=$5 L=$6
(cd $B/gateware && BUDGET_TRACE_AFTER=$((S - 2000)) BUDGET_TRACE_PCS=40000 $B/native/Vsim $B/$K/$G.txt - | grep '^PC ' > $T/cut/$L.pcs)
echo "$(wc -l < $T/cut/$L.pcs) PCs $(date +%T)"
python3 -I - "$B/image/ctrl_app.map" "$T/cut/$L.pcs" $((S - 64)) $N > $T/cut/$L.perfunc.txt <<'PY'
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
start, cycles = int(sys.argv[3]), int(sys.argv[4])
pcs = [(int(f[1]), int(f[2], 16)) for f in (l.split() for l in open(sys.argv[2])) if len(f) == 3]
cpus = [c for c, _ in pcs]; a, b = bisect.bisect_left(cpus, start), bisect.bisect_left(cpus, start + cycles)
ins, cyc, where = Counter(), Counter(), {}
for k in range(a, b):
    f = fn(pcs[k][1]); ins[f] += 1; cyc[f] += (pcs[k + 1][0] if k + 1 < len(pcs) else start + cycles) - pcs[k][0]
    where[f] = 'hot' if hot[0] <= pcs[k][1] < hot[1] else 'cold'
print(f'item at cpu {start}: {cycles} cycles, {b - a} instructions traced, {sum(cyc.values())} cycles charged; hot region {hot[1]-hot[0]} B')
for f, n in cyc.most_common(30):
    print(f'  {ins[f]:6d} instr {n:7d} cyc  {where[f]:4s}  {f}')
print(f"in cold code: {sum(c for f, c in cyc.items() if where[f] == 'cold')} cycles, {sum(i for f, i in ins.items() if where[f] == 'cold')} instructions")
PY
head -40 $T/cut/$L.perfunc.txt
