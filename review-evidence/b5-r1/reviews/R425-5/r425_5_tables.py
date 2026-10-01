#!/usr/bin/env python3
"""R425-5: per-table identity of the findings page across rounds.

Usage: r425_5_tables.py <repo> <rev>...   (last rev is the head under review)
Tables are maximal runs of lines starting with '|'. Prints, per table, its
header cells (no body text), its line count, and for each earlier rev whether
it is byte-identical to the head's table at the same position. For any table
that differs from the immediately preceding rev, prints which rows and which
columns differ (column names only).
"""
import hashlib, subprocess, sys

repo, revs = sys.argv[1], sys.argv[2:]
PAGE = 'docs/findings/117_AUDIO_CONTINUITY.md'

def tables(rev):
    t = subprocess.run(['git', '-C', repo, 'show', f'{rev}:{PAGE}'], check=True,
                       capture_output=True, text=True).stdout.splitlines()
    out, cur = [], []
    for line in t + ['']:
        if line.startswith('|'):
            cur.append(line)
        elif cur:
            out.append(cur); cur = []
    return out

T = {r: tables(r) for r in revs}
head = revs[-1]
H = T[head]
print('table counts:', ', '.join(f'{r[:8]}={len(T[r])}' for r in revs))
print('table lines:', ', '.join(f'{r[:8]}={sum(map(len, T[r]))}' for r in revs))
for i, tb in enumerate(H, 1):
    hdr = tb[0]
    sha = hashlib.sha256('\n'.join(tb).encode()).hexdigest()[:16]
    same = []
    for r in revs[:-1]:
        o = T[r][i - 1] if len(T[r]) >= i else None
        same.append(f'{r[:8]}:{"=" if o == tb else "DIFF"}')
    print(f'T{i:02d} {len(tb):3d} lines sha {sha} {hdr[:70]} | ' + ' '.join(same))
prev = revs[-2]
for i, (a, b) in enumerate(zip(T[prev], H), 1):
    if a == b:
        continue
    cols = [c.strip() for c in b[0].strip('|').split('|')]
    for k, (la, lb) in enumerate(zip(a, b)):
        if la != lb:
            ca = la.strip('|').split('|'); cb = lb.strip('|').split('|')
            diff = [cols[j] if j < len(cols) else str(j) for j in range(max(len(ca), len(cb)))
                    if j >= len(ca) or j >= len(cb) or ca[j] != cb[j]]
            print(f'T{i:02d} row {k}: changed columns vs {prev[:8]}: {diff}')
    if len(a) != len(b):
        print(f'T{i:02d}: row count {len(a)} -> {len(b)}')
