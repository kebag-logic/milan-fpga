#!/usr/bin/env python3
"""spans_cmp.py LABEL LOG=... : per log, the maap_mbx:poll span (CPU cycles) distribution, and every pass's cycles
(PASS lines), over the sys range the shortest log reached. Read-only; logs may be partial."""
import sys
logs = [a.split('=', 1) for a in sys.argv[1:]]
data = {}
for name, path in logs:
    spans, passes, last = [], [], 0
    for l in open(path, errors='replace'):
        f = l.split()
        if not f: continue
        if f[0] == 'SPAN' and len(f) >= 6:
            last = max(last, int(f[1]))
            if f[5] == 'maap_mbx:poll': spans.append((int(f[1]), int(f[3])))
        elif f[0] == 'PASS' and len(f) >= 5:
            passes.append((int(f[2]), int(f[4])))
    data[name] = (spans, passes, last)
reach = min(v[2] for v in data.values())
def q(xs, p): return xs[min(len(xs) - 1, int(len(xs) * p))] if xs else None
for name, (spans, passes, last) in data.items():
    s = sorted(c for t, c in spans if t <= reach); p = sorted(c for t, c in passes if t <= reach)
    print(f"{name}: to sys {reach}: maap_mbx:poll n {len(s)} min {s[0] if s else None} p50 {q(s, .5)} p90 {q(s, .9)} max {s[-1] if s else None};"
          f" passes n {len(p)} p50 {q(p, .5)} p99 {q(p, .99)} max {p[-1] if p else None}")
