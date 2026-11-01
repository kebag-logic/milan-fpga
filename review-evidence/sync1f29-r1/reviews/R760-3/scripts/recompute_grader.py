#!/usr/bin/env python3
"""recompute_grader.py TREE RAWDIR: the three grade.py functions README line 846 names, plus records posted and released before each adp window opens."""
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
        s, e = marks['composed'], marks['composed_end']
        ps = grade.composed_passes(log, s, e)
        longest = max(p.cycles for p in ps)
        un = {k: v for k, v in grade.unreleased(log, s, e).items() if v}
        posted = sum(1 for c, w in log.records if c < s)
        tails = [v for c, w, v in log.writes if w == scenario.EVT_TAIL_WORD and c < s]
        rel = grade.unwrapped(tails) // EV
        print(f"{arm:8} {name:19} GM {grade.population(log, s, e).get('GM')} passes {len(ps)} longest_ms {longest/50000:.2f} unreleased {un} posted {posted} released {rel} held {posted-rel}")
