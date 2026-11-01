#!/usr/bin/env python3
"""A results directory's SUMMARY lines, added over its groups: CPI and each region's access count, mean and range."""
import re, sys
from pathlib import Path
d = Path(sys.argv[1])
cpu = instr = 0
acc = {}
n = 0
for log in sorted(d.glob('*.log')):
    for line in log.read_text(errors='replace').splitlines():
        if not line.startswith('SUMMARY '):
            continue
        n += 1
        f = dict(x.split('=', 1) for x in line.split()[1:] if '=' in x)
        cpu += int(f['cpu']); instr += int(f['instr'])
        for k, v in f.items():
            m = re.fullmatch(r'(\d+)/(\d+)/(\d+)/(\d+)', v)
            if m:
                c, s, lo, hi = map(int, m.groups())
                if c:
                    a = acc.setdefault(k, [0, 0, lo, hi])
                    a[0] += c; a[1] += s; a[2] = min(a[2], lo); a[3] = max(a[3], hi)
print(f'{d}: {n} groups, CPI {cpu / instr:.2f}')
for k in ('fetch_rom', 'load_flash', 'fetch_flash'):
    if k in acc:
        c, s, lo, hi = acc[k]
        print(f'  {k}: count {c}, mean {s / c:.2f}, range {lo}-{hi}')
print('  regions seen:', sorted(k for k in acc if 'flash' in k))
