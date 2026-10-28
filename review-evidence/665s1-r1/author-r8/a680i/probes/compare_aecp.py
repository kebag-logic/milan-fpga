#!/usr/bin/env python3
"""The aecp group's probes, S2's recorded figures beside this run's, off two table.md files.
usage: compare_aecp.py <S2 table.md> <this run's table.md>
Each row: probe, then for S2 and for this run: CPU cycles, ms, taking-pass CPU cycles, mailbox
accesses in the taking pass; then the differences in ms and in accesses."""
import re
import sys
from pathlib import Path


def rows(path: str) -> dict[str, list[str]]:
    """The per-probe table's cells, by probe, for the aecp group's probes."""
    out = {}
    for line in Path(path).read_text().splitlines():
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) == 10 and re.fullmatch(r'`aecp\.[^`]+`', cells[1]):
            out[cells[1].strip('`')] = cells
    return out


def num(cell: str) -> float:
    """A table number, its thousands separators and model count removed."""
    return float(cell.split()[0].replace(',', ''))


s2, here = rows(sys.argv[1]), rows(sys.argv[2])
print(f'S2 rows {len(s2)}, this run {len(here)}, common {len(set(s2) & set(here))}')
print('| Probe | S2 cycles | S2 ms | S2 pass cycles | S2 accesses | cycles | ms | pass cycles | accesses | d ms | d accesses |')
print('|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|')
for probe in sorted(set(s2) | set(here)):
    a, b = s2.get(probe), here.get(probe)
    if not a or not b:
        print(f'| {probe} | {"missing" if not a else "present"} in S2 | {"missing" if not b else "present"} here |')
        continue
    da = num(b[8]) - num(a[8])
    print(f'| {probe} | {a[2]} | {a[3]} | {a[7]} | {a[8]} | {b[2]} | {b[3]} | {b[7]} | {b[8]} | '
          f'{num(b[3]) - num(a[3]):+.3f} | {da:+.0f} |')
