#!/usr/bin/env python3
"""ring_at_open.py TREE RESULTS: which event records sit unreleased at the backlog-adp window's opening."""
import sys
from pathlib import Path
tree, results = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(tree / 'tb/verilator/ctrl_service_budget'))
import grade, scenario
log = grade.parse((results / 'backlog-adp.log').read_text(), 100_000_000, 50_000_000)
start = dict((n, c) for c, n in log.marks)['composed']
recs = [(c, w[0] & 0xFF) for c, w in log.records if c < start]
tail = grade.unwrapped([v for c, w, v in log.writes if w == scenario.EVT_TAIL_WORD and c < start]) // scenario.CONTRACT.ev_words
print('open', start, 'posted', len(recs), 'released', tail, 'held', [(start - c, grade.EVENT.get(t, hex(t))) for c, t in recs[tail:]])
last = [p for p in log.passes if p.start_sys < start][-1]
print('last pass before open: start', start - last.start_sys, 'bus cycles before, cpu cycles', last.cycles)
