#!/usr/bin/env python3
"""Compare two RV32 ELF images: section table, symbol table, and every differing byte of each loaded section,
each differing byte named by the symbol that holds it (and, in .text, the instruction there on both sides).

usage: compare_images.py BINDIR A.elf B.elf     (BINDIR: the RV32 SDK's bin directory)
Prints one verdict line: SAME-BYTES, or DATA-ONLY (layout and symbols identical) with the differing spans.
"""
import subprocess
import sys
from pathlib import Path

bindir, a, b = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])


def tool(name, *args):
    return subprocess.run([str(bindir / f'riscv32-linux-{name}'), *args], capture_output=True, text=True,
                          check=True).stdout


def sections(elf):
    rows = []
    for line in tool('readelf', '-SW', str(elf)).splitlines():
        line = line.strip()
        if line.startswith('[') and ']' in line and not line.startswith('[Nr]'):
            f = line.split(']', 1)[1].split()
            if len(f) >= 6:
                rows.append((f[0], f[1], int(f[2], 16), int(f[3], 16), int(f[4], 16), f[6] if len(f) > 6 else ''))
    return rows


def symbols(elf):
    out = []
    for line in tool('nm', '-n', '-S', str(elf)).splitlines():
        f = line.split()
        if len(f) == 4:
            out.append((int(f[0], 16), int(f[1], 16), f[2], f[3]))
    return out


def holder(syms, addr):
    best = None
    for start, size, kind, name in syms:
        if start <= addr < start + max(size, 1):
            best = name
    return best or '?'


sa, sb = sections(a), sections(b)
ya, yb = symbols(a), symbols(b)
layout_same = sa == sb
syms_same = ya == yb
da, db = a.read_bytes(), b.read_bytes()
spans = []
for name, kind, addr, off, size, flags in sa:
    if kind == 'NOBITS' or 'A' not in flags or size == 0:
        continue
    x, y = da[off:off + size], db[off:off + size]
    diff = [i for i in range(min(len(x), len(y))) if x[i] != y[i]]
    for i in diff:
        spans.append((name, addr + i, x[i], y[i], holder(ya, addr + i)))
print(f'A {a}\nB {b}')
print(f'sections identical: {layout_same}; symbols (address, size, kind, name) identical: {syms_same}; '
      f'file sizes {len(da)} {len(db)}')
seen = set()
for name, addr, x, y, sym in spans:
    print(f'  {name} 0x{addr:05x} {x:02x}->{y:02x} in {sym}')
    if name == '.text' and (addr & ~3) not in seen:
        seen.add(addr & ~3)
        for elf in (a, b):
            dis = tool('objdump', '-d', f'--start-address=0x{addr & ~3:x}', f'--stop-address=0x{(addr & ~3) + 4:x}',
                       str(elf)).strip().splitlines()[-1]
            print(f'      {elf.parent.name}: {dis.strip()}')
if da == db:
    print('VERDICT SAME-BYTES')
elif layout_same and syms_same:
    print(f'VERDICT DATA-ONLY {len(spans)} byte(s) in {sorted({s[4] for s in spans})}')
else:
    print('VERDICT LAYOUT-DIFFERS')
