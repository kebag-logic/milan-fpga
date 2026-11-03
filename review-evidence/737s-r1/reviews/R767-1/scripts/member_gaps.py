#!/usr/bin/env python3
"""Per-member hosted seconds from gaps between consecutive LiteX runner result lines.
Usage: member_gaps.py <job log>...  The first member's gap starts at the runner
selftest's final 'RESULT: PASS' line. Prints per-log gaps and the per-member max."""
import re, sys, datetime as d
ts = lambda s: d.datetime.fromisoformat(s[:26] + '+00:00')
best = {}
for path in sys.argv[1:]:
    prev, gaps = None, {}
    for line in open(path, errors='replace'):
        m = re.search(r'(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d+)Z (.*)$', line)
        if not m: continue
        t, text = ts(m.group(1)), m.group(2)
        if text.startswith('run_litex_sims selftest:'): prev = t
        r = re.match(r'(PASS|FAIL|SKIP|TIMEOUT) +(test_\w+)', text)
        if r and prev:
            gaps[r.group(2)] = round((t - prev).total_seconds()); prev = t
    print(path.split('/')[-1], gaps)
    for k, v in gaps.items(): best[k] = max(best.get(k, 0), v)
print('max', dict(sorted(best.items())))
