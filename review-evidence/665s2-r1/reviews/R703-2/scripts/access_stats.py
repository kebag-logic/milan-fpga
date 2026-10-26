#!/usr/bin/env python3
"""Per-access, idle-pass, fetch-share and code-size figures from raw logs (SUMMARY, IDLE, PASS, CODE lines).
Usage: access_stats.py RESULTS_DIR [GROUP ...]  (CPU cycles; stats are count/sum/min/max)"""
import json, sys
from pathlib import Path
res = Path(sys.argv[1]); only = set(sys.argv[2:])
agg = {}
idle = []
share = []
code = {}
for log in sorted(res.glob('*.log')):
    if only and log.stem not in only:
        continue
    for line in log.read_text().splitlines():
        if line.startswith('SUMMARY'):
            for kv in line.split()[1:]:
                k, v = kv.split('=')
                if '/' in v:
                    c, s, lo, hi = (int(x) for x in v.split('/'))
                    a = agg.setdefault(k, [0, 0, 1 << 62, 0])
                    a[0] += c; a[1] += s; a[2] = min(a[2], lo) if c else a[2]; a[3] = max(a[3], hi)
        elif line.startswith('IDLE'):
            _, n, lo, hi = line.split()
            if int(lo):
                idle.append((int(lo), int(hi)))
        elif line.startswith('PASS'):
            f = dict(kv.split('=', 1) for kv in line.split(' W')[0].split()[5:] if '=' in kv)
            fe = sum(int(v.split('/')[0]) for k, v in f.items() if k.startswith('fetch_'))
            ls = sum(int(v) for k, v in f.items() if k.startswith(('load_', 'store_')))
            if fe + ls:
                share.append(fe / (fe + ls))
        elif line.startswith('CODE'):
            kv = dict(x.split('=') for x in line.split()[1:])
            code[log.stem] = (int(kv['boot_bytes']), int(kv['service_bytes']))
out = {k: dict(count=v[0], mean=round(v[1] / v[0], 3) if v[0] else None, min=v[2] if v[0] else None, max=v[3])
       for k, v in agg.items() if v[0]}
print(json.dumps(dict(access=out, idle_min=min(i[0] for i in idle), idle_max=max(i[1] for i in idle),
                      fetch_share_min=round(min(share), 3), fetch_share_max=round(max(share), 3),
                      code_boot_max=max(c[0] for c in code.values()), code_service_max=max(c[1] for c in code.values())),
                 indent=1))
