#!/usr/bin/env python3
"""Per grid: early (pre-burst) head slips by class, with phase, lateness, time after
the first PDU and the bind's lowest primed margin. usage: early_detail.py <head dir>..."""
import re, sys
from pathlib import Path
res = re.compile(r"RESULT-645-BIND: B17 cycle (\d+) phase ([0-9.]+) at INTERNAL: first PDU \+([0-9.]+) ms after the bind, "
                 r"primed margin ([-0-9.e+]+)\.\.([-0-9.e+]+) us \((inside|OUTSIDE)")
sl = re.compile(r"info: B17 cycle (\d+): slip \((dup|skip)\) ([-+0-9.]+) s after the bind, ([-+0-9.]+) s from")
for d in sys.argv[1:]:
    rows = []; jit = set()
    for log in sorted(Path(d).glob('bind_*.log')):
        cur = None
        for line in log.read_text().splitlines():
            m = res.search(line)
            if m:
                cur = (log.stem, int(m.group(1)), float(m.group(2)), float(m.group(3)), float(m.group(4)), m.group(6)); continue
            m = sl.search(line)
            if m and cur and int(m.group(1)) == cur[1] and float(m.group(4)) < 0:
                rows.append(cur + ((float(m.group(3)) * 1e3 - cur[3]),))
        jit.add(log.stem.split('_')[1])
    print('==', Path(d).name, 'lateness sets', sorted(jit))
    for cls in ('inside', 'OUTSIDE'):
        r = [x for x in rows if x[5] == cls]
        if not r: print(cls, 0); continue
        print(cls, len(r), 'phases', sorted({x[2] for x in r}), 'lateness', sorted({x[0].split('_')[1] for x in r}),
              'ms after first PDU %.3f..%.3f' % (min(x[6] for x in r), max(x[6] for x in r)),
              'lowest primed %.3f..%.3f us' % (min(x[4] for x in r), max(x[4] for x in r)))
