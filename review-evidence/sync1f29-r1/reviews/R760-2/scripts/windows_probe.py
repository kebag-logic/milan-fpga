#!/usr/bin/env python3
"""windows_probe.py TREE RESULTS: each backlog window's GM commits, ring occupancy at open, passes and
longest pass, read from a run's logs with that tree's own grade.py. Independent of any author script."""
import sys
from pathlib import Path
tree, results = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(tree / 'tb/verilator/ctrl_service_budget'))
import grade, scenario
EV = scenario.CONTRACT.ev_words
for name in ('backlog', 'backlog-owed', 'backlog-adp', 'backlog-adp-refill'):
    log = grade.parse((results / f'{name}.log').read_text(), 100_000_000, 50_000_000)
    marks = {n: c for c, n in log.marks}
    start, end = marks['composed'], marks['composed_end']
    pop = grade.population(log, start, end)
    passes = grade.composed_passes(log, start, end)
    longest = max(p.cycles for p in passes)
    posted = sum(1 for c, _ in log.records if c < start)
    tail = [v for c, w, v in log.writes if w == scenario.EVT_TAIL_WORD and c < start]
    done = grade.unwrapped(tail) // EV
    gm = [c for c, w in log.records if start <= c <= end and grade.EVENT.get(w[0] & 0xFF) == 'GM']
    pulses = [c for c, kind, *_ in log.pads if start <= c <= end and kind.startswith('GM')] if log.pads else []
    gaps = [b - a for a, b in zip(gm, gm[1:])]
    print(f'{name}: GM committed {pop["GM"]} of defined {grade.defined_load(name)["GM"]}; ring depth {scenario.CONTRACT.evt_words // EV}; '
          f'occupancy at open {posted - done}; passes {len(passes)}; longest {longest:,} CPU cycles ({longest / 50_000:.3f} ms); '
          f'window {(end - start) / 100_000:.3f} ms; unreleased {grade.unreleased(log, start, end)}')
    print(f'  GM commit gaps, bus cycles: {gaps}')
