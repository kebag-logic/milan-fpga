"""One span's cycles in four parts from a committed-PC trace: one a commit, the short stalls (under 60 cycles:
the pipeline's load-use, branch and multiply waits), the long stalls a fetch refill issued in the 260 cycles before
explains (the instruction cache's misses), and the other long stalls (the data cache's). Optionally per function.
usage: python3 -I budget.py FUNCTIONS.json TRACE START CYCLES [by-function]"""
import bisect
import collections
import json
import re
import sys

raw = json.load(open(sys.argv[1]))
funcs = sorted((a, s, n) for n, a, s in raw)
st = [a for a, _, _ in funcs]
S, C = int(sys.argv[3]), int(sys.argv[4])


def func(pc):
    k = bisect.bisect_right(st, pc) - 1
    return re.sub(r'@.*', '', funcs[k][2]) if k >= 0 and pc < funcs[k][0] + funcs[k][1] else '?'


pcs, fe = [], []
for ln in open(sys.argv[2], errors='replace'):
    if ln.startswith('PC '):
        _, c, p = ln.split()
        c = int(c)
        if S <= c <= S + C:
            pcs.append((c, int(p, 16)))
        elif c > S + C:
            break
    elif ln.startswith('FETCH '):
        c = int(ln.split()[1])
        if S - 300 <= c <= S + C:
            fe.append(c)
parts = collections.defaultdict(lambda: [0, 0, 0, 0])
for k in range(len(pcs) - 1):
    c, p = pcs[k]
    g = pcs[k + 1][0] - c
    row = parts[func(p) if len(sys.argv) > 5 else 'span']
    row[0] += 1
    if g >= 60:
        i = bisect.bisect_left(fe, pcs[k + 1][0] - 260)
        row[2 if i < len(fe) and fe[i] <= pcs[k + 1][0] else 3] += g - 1
    else:
        row[1] += g - 1
print(f"{'':22s} {'commits':>8s} {'short':>7s} {'fetch':>7s} {'data':>7s} {'total':>7s}")
for n, r in sorted(parts.items(), key=lambda kv: -sum(kv[1]))[:25]:
    print(f'{n:22s} {r[0]:8d} {r[1]:7d} {r[2]:7d} {r[3]:7d} {sum(r):7d}')
