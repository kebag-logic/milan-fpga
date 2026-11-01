#!/usr/bin/env python3
"""recompute_windows.py TREE RAWDIR: per arm, each window's GM committed, ring occupancy at open, exact length, passes, longest pass, unreleased, from raw logs with the tree's own grade.py. Writes nothing."""
import sys
from pathlib import Path
tree, raw = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.dont_write_bytecode = True
sys.path[:0] = [str(tree / 'tb/verilator/ctrl_service_budget'), str(tree / 'sw/mailbox'), str(tree / 'sw/litex')]
import grade, scenario
EV = scenario.CONTRACT.ev_words
for arm in ('head', 'nostage', 'base'):
    for name in ('backlog', 'backlog-owed', 'backlog-adp', 'backlog-adp-refill'):
        log = grade.parse((raw / f'{arm}-xip64-{name}.log').read_text(), 100_000_000, 50_000_000)
        marks = dict((n, c) for c, n in log.marks)
        start, end = marks['composed'], marks['composed_end']
        gm = [c for c, w in log.records if start <= c <= end and grade.EVENT.get(w[0] & 0xFF) == 'GM']
        posted = sum(1 for c, w in log.records if c < start)
        tails = [v for c, w, v in log.writes if w == scenario.EVT_TAIL_WORD and c < start]
        held = posted - grade.unwrapped(tails) // EV
        ms = (end - start) / 100000
        print(f'{arm:8} {name:19} GM {len(gm):2} ring_at_open {held} window_cycles {end-start} ms {ms:.5f} round2 {ms:.2f}')
