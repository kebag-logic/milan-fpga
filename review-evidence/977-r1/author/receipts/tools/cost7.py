#!/usr/bin/env python3
"""cost7.py: each group's cost in round 6's every-arm runs: the simulated ms its finished log reached (its MS lines, the
copy the regrade read), by point and variant, into r7/cost.json; prints each arm's total."""
import json, os, subprocess
from pathlib import Path
T = Path('<scratch>')
out = {}
for p in ('1x1', '8x8-1if'):
    for d in sorted((T / 'r6/regrade' / p).iterdir()):
        if not d.is_dir():
            continue
        c = {}
        for log in d.glob('*.log'):
            n = subprocess.run(['grep', '-c', '^MS ', os.path.realpath(log)], capture_output=True, text=True).stdout.strip()
            c[log.stem] = int(n or 0)
        out[f'{p}/{d.name}'] = c
        print(p, d.name, len(c), sum(c.values()) / 1000)
(T / 'r7/cost.json').write_text(json.dumps(out, indent=1))
print('ALL', sum(sum(c.values()) for c in out.values()) / 1000)
