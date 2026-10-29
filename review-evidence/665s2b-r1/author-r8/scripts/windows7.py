#!/usr/bin/env python3
"""Scratch: each backlog group's composed window (prof.window) for the trace runs: the group's first service
record's start and the last AECP and SRP records' ends, bus cycles. usage: windows7.py RESULTS_DIR"""
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import prof  # noqa: E402
d = Path(sys.argv[1])
for g in prof.GROUPS:
    res = json.loads((d / f'{g}.json').read_text())
    ends = {row: prof.window(res, row) for row, _ in prof.ROWS}
    start = min(w[0] for w in ends.values() if w)
    print(g, start, ' '.join(f'{row}={w[1]}' for row, w in ends.items() if w))
