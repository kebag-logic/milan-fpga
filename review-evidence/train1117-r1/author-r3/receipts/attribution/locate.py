#!/usr/bin/env python3
"""locate.py LEGROOT: for each kind of interest, the log (variant/part/group) whose event cost is the most, by
eventcost.py's own costs() (read-only copy of #665 round 28's tool)."""
import sys
from pathlib import Path
sys.path.insert(0, '<scratch>/tools/survey')
import eventcost  # noqa: E402
KINDS = ('TIMER#3', 'TIMER#2', 'AS_PATH_CHANGED', 'AVB_INFO_CHANGED')
best = {k: (0, '-') for k in KINDS}
top = {k: [] for k in KINDS}
for log in sorted(Path(sys.argv[1]).glob('*/part*/*.log')):
    if 'RESULT' not in log.read_text(errors='replace')[-4000:]:
        continue
    for kind, spent in eventcost.costs(log):
        if kind in best:
            top[kind].append((spent, str(log.relative_to(sys.argv[1]))))
for k in KINDS:
    t = sorted(top[k], reverse=True)
    print(k, t[:4], 'groups:', sorted({w for _, w in t})[:12])
