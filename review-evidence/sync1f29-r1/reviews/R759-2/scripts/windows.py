#!/usr/bin/env python3
"""windows.py TREE RESULTS LABEL: each backlog window's load, ring state at open and GM commit times, read from
a run's raw group logs with that tree's own grade.py functions, without its refusal."""
import sys
from pathlib import Path
tree, results, label = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
sys.path[:0] = [str(tree / 'tb/verilator/ctrl_service_budget'), str(tree / 'sw/mailbox'), str(tree / 'sw/litex')]
import grade, scenario
EV = scenario.CONTRACT.ev_words
SYS, CPU = 100_000_000, 50_000_000
for name in ('backlog', 'backlog-owed', 'backlog-adp', 'backlog-adp-refill'):
    log = grade.parse((results / f'{name}.log').read_text(), SYS, CPU)
    marks = dict((n, c) for c, n in log.marks)
    start, end = marks['composed'], marks['composed_end']
    pop = grade.population(log, start, end)
    inside = grade.composed_passes(log, start, end)
    top = max(inside, key=lambda p: p.cycles)
    posted = sum(1 for c, _ in log.records if c < start)
    tails = [v for c, w, v in log.writes if w == scenario.EVT_TAIL_WORD and c < start]
    occ = posted - grade.unwrapped(tails) // EV
    gm = [c - start for c, w in log.records if start <= c <= end and grade.EVENT.get(w[0] & 0xFF) == 'GM']
    burst = sum(1 for c in gm if c < gm[0] + 15 * 8 + 16)
    print(f'{label} {name}: GM {pop["GM"]}, ring at open {occ}, GM in first burst {burst}, '
          f'last GM at +{(gm[-1] - gm[0]) * 1000.0 / SYS:.3f} ms after the first, window {(end - start) * 1000.0 / SYS:.2f} ms, '
          f'passes {len(inside)}, longest {top.cycles * 1000.0 / CPU:.2f} ms, unreleased {grade.unreleased(log, start, end)}')
