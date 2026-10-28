#!/usr/bin/env python3
"""One group's probes, a reference run's figures beside this run's, off two table.md files.
usage: compare_rows.py <prefix> <reference table.md> <this run's table.md>
Each row: probe, then for the reference and for this run: CPU cycles, ms, verdict, taking-pass CPU
cycles, mailbox accesses in the taking pass; then the differences in ms and in accesses."""
import re
import sys
from pathlib import Path


def rows(prefix: str, path: str) -> dict[str, list[str]]:
    """The per-probe table's cells, by probe, for the probes whose name starts with prefix."""
    out = {}
    for line in Path(path).read_text().splitlines():
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) == 10 and re.fullmatch(rf'`{re.escape(prefix)}\.[^`]+`', cells[1]):
            out[cells[1].strip('`')] = cells
    return out


def num(cell: str) -> float:
    """A table number, its thousands separators and model count removed."""
    return float(cell.split()[0].replace(',', ''))


prefix, ref_path, here_path = sys.argv[1:4]
ref, here = rows(prefix, ref_path), rows(prefix, here_path)
print(f'reference rows {len(ref)}, this run {len(here)}, common {len(set(ref) & set(here))}')
print('| Probe | ref cycles | ref ms | ref verdict | ref pass cycles | ref accesses | cycles | ms | verdict | pass cycles | accesses | d ms | d accesses |')
print('|---|---:|---:|---|---:|---:|---:|---:|---|---:|---:|---:|---:|')
for probe in sorted(set(ref) | set(here)):
    a, b = ref.get(probe), here.get(probe)
    if not a or not b:
        print(f'| {probe} | {"missing" if not a else "present"} in the reference | {"missing" if not b else "present"} here |')
        continue
    print(f'| {probe} | {a[2]} | {a[3]} | {a[6]} | {a[7]} | {a[8]} | {b[2]} | {b[3]} | {b[6]} | {b[7]} | {b[8]} | '
          f'{num(b[3]) - num(a[3]):+.3f} | {num(b[8]) - num(a[8]):+.0f} |')
