#!/usr/bin/env python3
"""check_delta.py TREE RAW_DIR: re-derive the two refused windows from the published round-2 raw logs and compare README lines 840-858 with them."""
import re
import sys
from pathlib import Path

tree, raw = Path(sys.argv[1]), Path(sys.argv[2])
sys.path[:0] = [str(tree / 'tb/verilator/ctrl_service_budget'), str(tree / 'sw/mailbox'), str(tree / 'sw/litex')]
import grade
import scenario

EV = scenario.CONTRACT.ev_words
lines = (tree / 'tb/verilator/ctrl_service_budget/README.md').read_text().splitlines()
rows = {}
for line in lines[849:858]:
    cells = [c.strip(' `') for c in line.strip('|').split('|')]
    if len(cells) == 8 and cells[0].startswith('backlog'):
        rows[(cells[0], cells[1])] = cells
bad = 0
for tag, stage in (('head', 'staged'), ('nostage', 'none'), ('base', None)):
    for name in ('backlog-adp', 'backlog-adp-refill'):
        text = (raw / f'{tag}-{name}.log').read_text()
        log = grade.parse(text, 100_000_000, 50_000_000)
        marks = dict((n, c) for c, n in log.marks)
        start, end = marks['composed'], marks['composed_end']
        gm = [c for c, w in log.records if start <= c <= end and grade.EVENT.get(w[0] & 0xFF) == 'GM']
        before = [c for c, w in log.records if c < start]
        done = grade.unwrapped([v for c, w, v in log.writes if w == scenario.EVT_TAIL_WORD and c < start]) // EV
        ring = len(before) - done
        cycles = end - start
        window = f'{cycles / 100000:.2f}'
        msg = f'{tag} {name}: {cycles} bus cycles, window {window} ms, ring at open {ring}, GM committed {len(gm)}'
        if stage:
            cell = rows[(name, stage)]
            same = cell[2] == str(len(gm)) and cell[4] == window
            bad += not same
            msg += f'; README row: GM {cell[2]}, window {cell[4]} -> {"match" if same else "MISMATCH"}'
        print(msg)
print(f'README line 843: {lines[842]}')
print(f'README line 846: {lines[845]}')
print(f'README line 854: {lines[853]}')
sys.exit(1 if bad else 0)
