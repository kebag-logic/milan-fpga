#!/usr/bin/env python3
"""pass_funcs.py ELF LOG START_CPU CYCLES [N]: the committed-PC trace (PC lines, BUDGET_TRACE_PCS) of one pass of a
CPU service-budget harness log, its cycles grouped by the function that holds each pc (nm -n: the last text symbol at
or below it), the N dearest, and the entries of each function (a commit at its first instruction). Read only."""
import bisect
import collections
import re
import subprocess
import sys

elf, log, start, cycles = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
n = int(sys.argv[5]) if len(sys.argv) > 5 else 40
end = start + cycles
nm = __import__('os').environ.get('NM', 'riscv32-buildroot-linux-gnu-nm')  # the pinned RV32 SDK's nm, on PATH
syms = []
for line in subprocess.run([nm, '-n', elf], capture_output=True, text=True, check=True).stdout.splitlines():
    parts = line.split()
    if len(parts) == 3 and parts[1] in 'tTwW':
        syms.append((int(parts[0], 16), parts[2]))
starts = [a for a, _ in syms]
first = {a for a, _ in syms}
pcs = []
with open(log, errors='replace') as f:
    for line in f:
        if line.startswith('PC '):
            _, c, pc = line.split()
            c = int(c)
            if start <= c <= end:
                pcs.append((c, int(pc, 16)))
by_fn = collections.Counter()
entries = collections.Counter()
for (c, pc), (c2, _) in zip(pcs, pcs[1:] + [(end, 0)]):
    k = bisect.bisect_right(starts, pc) - 1
    name = syms[k][1] if k >= 0 else '?'
    by_fn[name] += c2 - c
    if pc in first:
        entries[name] += 1
seen = sum(by_fn.values())
print(f'pass at cpu {start:,}, {cycles:,} cycles: {len(pcs):,} commits traced, {seen:,} cycles attributed')
for fn, c in by_fn.most_common(n):
    print(f'{100 * c / cycles:5.1f}%  {c:>9,}  {entries[fn]:>5} entries  {fn}')
