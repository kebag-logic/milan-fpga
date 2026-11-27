#!/usr/bin/env python3
"""eta7.py: the every-arm pool's progress by round 6's cost: finished, in flight (its log's MS lines), queued."""
import json, subprocess
from pathlib import Path
T = Path('<scratch>/r7')
c = json.loads((T / 'cost.json').read_text())
tot = sum(sum(v.values()) for v in c.values()); done = fly = 0; nf = 0
for p in ('1x1', '8x8-1if'):
    for vd in (T / 'arms' / p).iterdir():
        for d in vd.glob('s-*'):
            if not d.is_dir():
                continue
            g = d.name[2:]; cost = c.get(f'{p}/{vd.name}', {}).get(g, 0)
            if (d / 'DONE').exists():
                done += cost
            else:
                nf += 1
                log = d / f'{g}.log'
                if log.exists():
                    fly += int(subprocess.run(['grep', '-c', '^MS ', str(log)], capture_output=True, text=True).stdout.strip() or 0)
print(f'done {done/1000:.0f} s, in flight {nf} groups {fly/1000:.0f} s, left {(tot-done-fly)/1000:.0f} of {tot/1000:.0f} s')
