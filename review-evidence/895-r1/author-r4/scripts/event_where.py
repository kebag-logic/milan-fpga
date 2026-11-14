#!/usr/bin/env python3
"""event_where.py KIND... -- RESULTS_DIR...: for each event KIND (eventcost.py's names, e.g. TIMER#3, TICK), the
groups whose largest cost of that kind is the most, by eventcost.py's own costs(); the top five per kind."""
import sys
from pathlib import Path
sys.path.insert(0, '$MANAGEMENT/2026-09-23/895-a775/scripts/costs')
import eventcost  # noqa: E402
sep = sys.argv.index('--')
kinds, dirs = sys.argv[1:sep], sys.argv[sep + 1:]
best = {k: [] for k in kinds}
for d in dirs:
    for path in sorted(Path(d).glob('*.log')):
        if 'RESULT' not in path.read_text(errors='replace')[-4000:]:
            continue
        got = {}
        for kind, spent in eventcost.costs(path):
            if kind in best:
                got[kind] = max(got.get(kind, 0), spent)
        for k, v in got.items():
            best[k].append((v, f'{Path(d).parent.name}/{path.stem}'))
for k in kinds:
    print(k, sorted(best[k], reverse=True)[:5])
