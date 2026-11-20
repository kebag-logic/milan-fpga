#!/usr/bin/env python3
"""fifo_util.py LABEL_A DIR_A LABEL_B DIR_B [STAGE]: every cdc_pair_fifo instance's utilisation (Vivado's hierarchical
utilisation report, STAGE synth or place) in two builds, by its full instance path, side by side, with each cell's
difference (RULING-1118c item 5: the default branch must map the same at every instance but the distributed one)."""
import re
import sys
from pathlib import Path


def rows(d: Path, stage: str) -> tuple[list[str], dict[str, tuple[str, list[str]]]]:
    rpt = next(d.glob(f'*_utilization_hierarchical_{stage}.rpt'))
    head, out, stack = None, {}, []
    for line in rpt.read_text(errors='replace').splitlines():
        if not line.startswith('|'):
            continue
        cells = [c for c in line.split('|')[1:-1]]
        if head is None and cells and cells[0].strip() == 'Instance':
            head = [c.strip() for c in cells]
            continue
        if head is None or len(cells) != len(head):
            continue
        name = cells[0].rstrip(); depth = len(name) - len(name.lstrip())
        stack = [(dep, n) for dep, n in stack if dep < depth] + [(depth, name.strip())]
        module = cells[1].strip()
        if module.startswith('cdc_pair_fifo'):
            out['/'.join(n for _, n in stack[1:])] = (module, [c.strip() for c in cells[2:]])
    return head[2:], out


la, da, lb, db = sys.argv[1], Path(sys.argv[2]), sys.argv[3], Path(sys.argv[4])
stage = sys.argv[5] if len(sys.argv) > 5 else 'synth'
head, a = rows(da, stage)
_, b = rows(db, stage)
print(f'# cdc_pair_fifo instances, {stage} hierarchical utilisation: {la} against {lb}; columns {", ".join(head)}')
same = 0
for path in sorted(set(a) | set(b)):
    ma, ca = a.get(path, ('-', []))
    mb, cb = b.get(path, ('-', []))
    eq = ca == cb
    same += eq
    print(f"{'EQUAL ' if eq else 'DIFFER'} {path}  [{la} {ma}: {' '.join(ca)}]  [{lb} {mb}: {' '.join(cb)}]")
print(f'{same} of {len(set(a) | set(b))} instances equal')
