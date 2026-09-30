#!/usr/bin/env python3
"""Compare every Markdown table block of each page between two commits.
usage: table_identity.py <repo> <old> <new> <page>..."""
import hashlib, subprocess, sys
repo, old, new, pages = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
def tables(rev, page):
    text = subprocess.run(['git', '-C', repo, 'show', f'{rev}:{page}'], capture_output=True, text=True, check=True).stdout
    out, cur, start = [], [], 0
    for i, line in enumerate(text.splitlines(), 1):
        if line.startswith('|'):
            if not cur: start = i
            cur.append(line)
        elif cur:
            out.append((start, cur)); cur = []
    if cur: out.append((start, cur))
    return out
for page in pages:
    a, b = tables(old, page), tables(new, page)
    print(f'{page}: {len(a)} tables at {old[:8]}, {len(b)} at {new[:8]}')
    for n, ((la, ta), (lb, tb)) in enumerate(zip(a, b), 1):
        ha = hashlib.sha256('\n'.join(ta).encode()).hexdigest()[:16]
        hb = hashlib.sha256('\n'.join(tb).encode()).hexdigest()[:16]
        state = 'IDENTICAL' if ta == tb else 'CHANGED'
        print(f'  table {n}: old L{la} new L{lb} rows {len(ta)}/{len(tb)} {ha} {hb} {state}')
        if ta != tb:
            for x, y in zip(ta, tb):
                if x != y:
                    diffs = [i for i, (p, q) in enumerate(zip(x, y)) if p != q]
                    print(f'    row differs at {len(diffs)} char(s), len {len(x)}/{len(y)}: {[(i, x[i], y[i]) for i in diffs][:6]}')
            for y in tb[len(ta):]: print(f'    added row: {y[:120]}')
