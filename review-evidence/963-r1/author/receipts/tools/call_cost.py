#!/usr/bin/env python3
"""call_cost.py ELF LOG START_CPU CYCLES CALLEE CALLER: the inclusive cycles of each call of CALLEE made from CALLER
inside one traced pass (PC lines, BUDGET_TRACE_PCS): from the commit of CALLEE's first instruction to the next commit
back in CALLER. Prints the count, the total, and the first and last few calls. Read only."""
import bisect
import subprocess
import sys

elf, log, start, cycles, callee, caller = sys.argv[1:7]
start, cycles = int(start), int(cycles)
end = start + cycles
nm = __import__('os').environ.get('NM', 'riscv32-buildroot-linux-gnu-nm')  # the pinned RV32 SDK's nm, on PATH
syms = []
for line in subprocess.run([nm, '-n', elf], capture_output=True, text=True, check=True).stdout.splitlines():
    parts = line.split()
    if len(parts) == 3 and parts[1] in 'tTwW':
        syms.append((int(parts[0], 16), parts[2]))
starts = [a for a, _ in syms]


def name(pc):
    k = bisect.bisect_right(starts, pc) - 1
    return syms[k][1] if k >= 0 else '?'


entry = {a for a, s in syms if s == callee}
calls, open_at = [], None
with open(log, errors='replace') as f:
    for line in f:
        if not line.startswith('PC '):
            continue
        _, c, pc = line.split()
        c, pc = int(c), int(pc, 16)
        if not start <= c <= end:
            continue
        if open_at is None and pc in entry:
            open_at = c
        elif open_at is not None and name(pc) == caller:
            calls.append(c - open_at)
            open_at = None
print(f'{callee} from {caller}: {len(calls)} calls, {sum(calls):,} cycles inclusive'
      f' (first {calls[:3]}, last {calls[-3:]})')
