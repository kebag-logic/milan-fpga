#!/usr/bin/env python3
"""Each backlog window's longest pass and whether it released its load, per arm, from the graded
group JSONs (the composed window grade.composed() records); nothing is measured.
usage: composed_windows.py REGRADE ARM..."""
import json
import sys
from pathlib import Path

ROWS = ('backlog', 'backlog-adp', 'backlog-adp-refill', 'backlog-owed')
root = Path(sys.argv[1])
print('| Window | ' + ' | '.join(sys.argv[2:]) + ' |')
for row in ROWS:
    cells = []
    for arm in sys.argv[2:]:
        path = root / arm / f'{row}.json'
        if not path.exists():
            cells.append('not run')
            continue
        c = json.loads(path.read_text())['passes']['composed']
        released = c.get('serviced', True)
        cells.append(f"{c['cycles']:,} ({c['ms']:.2f}){'' if released else ', unreleased ' + str(c.get('unreleased'))}")
    print(f'| `{row}` | ' + ' | '.join(cells) + ' |')
