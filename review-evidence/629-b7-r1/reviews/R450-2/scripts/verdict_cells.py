#!/usr/bin/env python3
"""Print the Verdict/Result/Judgement cell of every B7 table row at two commits and diff them.
usage: verdict_cells.py <repo> <rev-a> <rev-b>"""
import subprocess, sys
repo, a, b = sys.argv[1:4]
def cells(rev):
    t = subprocess.run(['git', '-C', repo, 'show', f'{rev}:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md'], capture_output=True, text=True, check=True).stdout
    t = t[t.index('## Dev bbf704ec'):]
    out = {}; hdr = None
    for line in t.splitlines():
        if not line.startswith('|'):
            hdr = None; continue
        c = [x.strip() for x in line.strip('|').split('|')]
        if hdr is None:
            hdr = c; continue
        if set(line) <= set('|-'): continue
        for name in ('Verdict', 'Result', 'Judgement'):
            if name in hdr:
                out[(name, c[0])] = c[hdr.index(name)]
    return out
A, B = cells(a), cells(b)
for k in sorted(set(A) | set(B)):
    s = 'same' if A.get(k) == B.get(k) else 'CHANGED'
    print(f'{s:7s} {k[0]:9s} {k[1][:70]!r}\n         {a[:8]}: {A.get(k)!r}\n         {b[:8]}: {B.get(k)!r}' if s == 'CHANGED' else f'{s:7s} {k[0]:9s} {k[1][:70]!r} = {B.get(k)!r}')
