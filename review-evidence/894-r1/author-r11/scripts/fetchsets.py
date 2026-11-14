"""The instruction-fetch refills of one span (sim_main.cpp's FETCH lines, BUDGET_TRACE_PCS): each line's address and
its set in the split CPU's fetch L1 (milan_soc.CTRL_FETCH_L1, 128 sets x 2 ways, 64-byte lines), the lines refetched
inside the span, the sets that more than two of the span's lines share, and the functions each line holds.

usage: python3 -I fetchsets.py FUNCTIONS.json TRACE START CYCLES"""
import bisect
import collections
import json
import sys

raw = json.load(open(sys.argv[1]))
funcs = sorted((a, s, n) for n, a, s in raw)
start, cycles = int(sys.argv[3]), int(sys.argv[4])
lines = []
for ln in open(sys.argv[2], errors='replace'):
    if ln.startswith('FETCH '):
        _, cpu, addr = ln.split()
        if start <= int(cpu) < start + cycles:
            lines.append(int(addr, 16) & ~63)


def held(line):
    return sorted({n for a, s, n in funcs if a < line + 64 and a + s > line})


count = collections.Counter(lines)
sets = collections.defaultdict(set)
for line in lines:
    sets[(line >> 6) & 127].add(line)
print(f'{len(lines)} refills, {len(count)} distinct lines, {sum(c - 1 for c in count.values())} refetched')
for line, c in sorted(count.items()):
    if c > 1:
        print(f'  refetched x{c}: {line:08x} set {(line >> 6) & 127:3d} {",".join(held(line))}')
print('sets holding more than two of the span\'s lines:')
for s, ls in sorted(sets.items()):
    if len(ls) > 2:
        print(f'  set {s:3d}: ' + '; '.join(f'{l:08x} {",".join(held(l))}' for l in sorted(ls)))
