#!/usr/bin/env python3
"""Compare a reviewer run's per-group grades, table.md and raw logs with the published receipts.
Usage: compare_published.py MY_RESULTS_DIR PUBLISHED_RUN_DIR"""
import json, sys
from pathlib import Path
mine, pub = Path(sys.argv[1]), Path(sys.argv[2])
same = diff = 0
for pj in sorted(pub.glob('*.json')):
    m = mine / pj.name
    ok = m.is_file() and json.loads(m.read_text()) == json.loads(pj.read_text())
    same += ok; diff += not ok
    if not ok: print('DIFF', pj.name)
print(f'{mine.parent.name} vs published {pub.name}: {same} group grades equal, {diff} differ;',
      'table.md', 'identical' if (pub / 'table.md').is_file() and (mine / 'table.md').read_bytes() == (pub / 'table.md').read_bytes() else 'DIFFERS/absent',
      '; logs', ', '.join(f'{l.name} {"identical" if (mine / l.name).read_bytes() == l.read_bytes() else "DIFFERS"}' for l in sorted(pub.glob('*.log'))))
