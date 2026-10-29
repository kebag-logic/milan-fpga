#!/usr/bin/env python3
"""Scratch: icache_geometry.py on each traced window: the trace's PC and FETCH stamps are CPU cycles, the window's
bus cycles, the two clocks equal (100 MHz); the offset is the first traced PC's stamp against BUDGET_TRACE_AFTER.
usage: model7.py LEG ... (traces/<LEG>-<group>/<group>.log, builds/<LEG>/results)"""
import json
import subprocess
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import prof  # noqa: E402
T = Path('$VALIDATION_STORAGE/665s2b-a683k')
for leg in sys.argv[1:]:
    for g in prof.GROUPS:
        res = json.loads((T / 'builds' / leg / 'results' / f'{g}.json').read_text())
        log = T / 'traces' / f'{leg}-{g}' / f'{g}.log'
        start = min(prof.window(res, row)[0] for row, _ in prof.ROWS if prof.window(res, row))
        after = start - 300000
        c0 = next(int(l.split()[1]) for l in open(log) if l.startswith('PC '))
        for row, _ in prof.ROWS:
            w = prof.window(res, row)
            if w is None or (g == 'backlog-owed' and row == 'aecp'):
                continue
            off = c0 - after
            out = subprocess.run([sys.executable, str(Path(__file__).parent / 'icache_geometry.py'), str(log),
                                  str(w[0] + off), str(w[1] + off)], capture_output=True, text=True, check=True)
            print(f'{leg} {g} {row} window {(w[1] - w[0]) / 1e5:.2f} ms (offset {off}): {out.stdout.strip()}', flush=True)
