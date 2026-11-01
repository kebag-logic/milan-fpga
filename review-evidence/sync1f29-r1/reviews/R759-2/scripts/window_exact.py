#!/usr/bin/env python3
"""window_exact.py TREE RESULTS LABEL: exact window lengths in bus cycles, GM commit spacing, and the ring's records at open."""
import sys
from pathlib import Path
tree, results, label = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
sys.path[:0] = [str(tree / 'tb/verilator/ctrl_service_budget'), str(tree / 'sw/mailbox'), str(tree / 'sw/litex')]
import grade, scenario
EV = scenario.CONTRACT.ev_words
for name in ('backlog', 'backlog-owed', 'backlog-adp', 'backlog-adp-refill'):
    log = grade.parse((results / f'{name}.log').read_text(), 100_000_000, 50_000_000)
    marks = dict((n, c) for c, n in log.marks)
    start, end = marks['composed'], marks['composed_end']
    gm = [c for c, w in log.records if start <= c <= end and grade.EVENT.get(w[0] & 0xFF) == 'GM']
    before = [(c, w[0] & 0xFF) for c, w in log.records if c < start]
    tails = [v for c, w, v in log.writes if w == scenario.EVT_TAIL_WORD and c < start]
    done = grade.unwrapped(tails) // EV
    held = before[done:]
    print(f'{label} {name}: window {end - start} bus cycles = {(end - start) / 100000:.5f} ms; '
          f'GM commit gaps {[b - a for a, b in zip(gm, gm[1:])]}; ring at open types '
          f'{[(grade.EVENT.get(t, hex(t)), start - c) for c, t in held]}')
