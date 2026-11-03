#!/usr/bin/env python3
"""Probe P1's analysis (review R711-4): for each window group's log, the passes that carry the store's step
between the window's opening (mark composed) and the commit-to-response of its last SRP record, and the graded
rows of the group (its <group>.json), the last SRP record's first among them.

usage: python3 -I analyse_aged_window.py <tree> <results dir> <group>...
"""
import json
import sys
from pathlib import Path

tree, results, groups = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3:]
sys.path.insert(0, str(tree / 'tb/verilator/ctrl_service_budget'))
import grade  # noqa: E402  (the probe tree's own grader)

SYS_HZ = CPU_HZ = 100_000_000
for name in groups:
    text = (results / f'{name}.log').read_text()
    log = grade.parse(text, SYS_HZ, CPU_HZ)
    marks = {m: c for c, m in log.marks}
    start, end = marks.get('composed'), marks.get('composed_end')
    result = json.loads((results / f'{name}.json').read_text())
    rows = {}
    for row in result.get('probes', []):
        if isinstance(row, dict) and 'probe' in row:
            rows[row['probe']] = row
    srp = {k: v for k, v in rows.items() if 'srp.last' in k}
    srp_ms = [(k, v.get('ms'), v.get('within_budget'), v.get('start_sys'), v.get('end_sys')) for k, v in srp.items()]
    # every pass that carried a step: the quiet ones (STEPPASS) and the work ones (step=1)
    quiet = [(s, c, st) for s, c, st in log.step_passes]
    work = [(p.start_sys, p.cycles, p.count('store')) for p in log.passes if p.fields.get('step')]
    floods = log.floods
    print(f'== {name}')
    print(f'   floods {floods}  composed {start}  composed_end {end}')
    if start is not None:
        inside = sorted(q for q in quiet + work if start <= q[0] <= (end or 1 << 62))
        print(f'   step-carrying quiet passes in the window: {len(inside)}',
              ' '.join(f'{(s - start) / 1e5:.3f}ms/{c}cyc/store{st}' for s, c, st in inside[:8]))
        before = sorted(q for q in quiet + work if q[0] < start)
        if before:
            print(f'   last step-carrying pass before the window: {(start - before[-1][0]) / 1e5:.3f} ms before it')
    for k, ms, verdict, s0, s1 in sorted(srp_ms):
        print(f'   {k}: {ms} ms within={verdict} start {s0} end {s1} (end {(s1 - start) / 1e5 if start and s1 else None} ms after composed)')
