#!/usr/bin/env python3
"""A function-level CPU profile of one pass from a harness log's committed-PC trace (#665): each PC line's CPU-cycle
count less the one before it is the previous PC's function's; the pass is the PASS line whose start is START_CPU
(its third field). Symbols from the image's ELF through the RV32 nm.

usage: pcprofile.py LOG ELF START_CPU [TOP]
"""
import bisect
import subprocess
import sys

log, elf, start_cpu = sys.argv[1], sys.argv[2], int(sys.argv[3])
top = int(sys.argv[4]) if len(sys.argv) > 4 else 40
out = subprocess.run(['$WORKSPACE_HOME/br-milan-rv32/host/bin/riscv32-buildroot-linux-gnu-nm', '-n', '--defined-only',
                      elf], capture_output=True, text=True, check=True).stdout
syms = [(int(a, 16), n) for a, t, n in (l.split()[:3] for l in out.splitlines() if len(l.split()) >= 3)
        if t in 'tTwW']
addrs = [a for a, _ in syms]
cycles = None
for line in open(log, errors='replace'):
    if line.startswith('PASS ') and int(line.split()[3]) == start_cpu:
        cycles = int(line.split()[4])
        break
if cycles is None:
    raise SystemExit(f'no PASS starting at CPU cycle {start_cpu}')
end = start_cpu + cycles
per: dict[str, int] = {}
prev = None
for line in open(log, errors='replace'):
    if not line.startswith('PC '):
        continue
    _, cpu, pc = line.split()
    cpu, pc = int(cpu), int(pc, 16)
    if prev is not None and start_cpu <= prev[0] < end:
        i = bisect.bisect_right(addrs, prev[1]) - 1
        name = syms[i][1] if i >= 0 else '?'
        per[name] = per.get(name, 0) + (min(cpu, end) - prev[0])
    prev = (cpu, pc)
total = sum(per.values())
print(f'pass at CPU cycle {start_cpu}: {cycles:,} cycles, {total:,} attributed')
for name, c in sorted(per.items(), key=lambda x: -x[1])[:top]:
    print(f'{c:8,d}  {name}')
