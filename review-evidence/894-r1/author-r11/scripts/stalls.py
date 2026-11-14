"""One span's cycles split three ways from a committed-PC trace: one cycle per commit, the stalls in which an
instruction-fetch refill was outstanding (a FETCH line at or after the stalled commit and before the next), and the
other stalls (data-side: loads and stores waiting on the bus, multiplies, branches). Per function, by the commit
that stalled. usage: python3 -I stalls.py FUNCTIONS.json TRACE START CYCLES"""
import bisect
import collections
import json
import re
import sys

raw = json.load(open(sys.argv[1]))
funcs = sorted((a, s, n) for n, a, s in raw)
starts = [a for a, _, _ in funcs]
start, cycles = int(sys.argv[3]), int(sys.argv[4])


def func(pc):
    k = bisect.bisect_right(starts, pc) - 1
    return re.sub(r'@.*', '', funcs[k][2]) if k >= 0 and pc < funcs[k][0] + funcs[k][1] else '?'


pcs, fetch = [], []
for ln in open(sys.argv[2], errors='replace'):
    if ln.startswith('PC '):
        _, c, p = ln.split()
        c = int(c)
        if start <= c <= start + cycles:
            pcs.append((c, int(p, 16)))
        elif c > start + cycles:
            break
    elif ln.startswith('FETCH '):
        c = int(ln.split()[1])
        if start <= c <= start + cycles:
            fetch.append(c)
by = collections.defaultdict(lambda: [0, 0, 0])
for k in range(len(pcs) - 1):
    c, p = pcs[k]
    gap = pcs[k + 1][0] - c
    f = by[func(p)]
    f[0] += 1
    if gap > 1:
        i = bisect.bisect_left(fetch, c)
        (f.__setitem__(1, f[1] + gap - 1) if i < len(fetch) and fetch[i] < pcs[k + 1][0] else
         f.__setitem__(2, f[2] + gap - 1))
tot = [sum(v[i] for v in by.values()) for i in range(3)]
print(f'span {cycles}: {tot[0]} commit cycles, {tot[1]} fetch-stall cycles ({len(fetch)} refills), {tot[2]} other stalls')
print(f"{'function':22s} {'commits':>7s} {'fetch':>6s} {'other':>6s}")
for n, v in sorted(by.items(), key=lambda kv: -(kv[1][1] + kv[1][2]))[:22]:
    print(f'{n:22s} {v[0]:7d} {v[1]:6d} {v[2]:6d}')
