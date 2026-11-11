#!/usr/bin/env python3
"""Compare tests/mutations.json across merge base, both parents and head: names, order, and per-plant equality."""
import json, subprocess, sys
repo, base, ours, theirs, head = sys.argv[1:6]
def load(rev):
    return json.loads(subprocess.run(['git', '-C', repo, 'show', f'{rev}:tests/mutations.json'], check=True, capture_output=True, text=True).stdout)
B, O, T, H = (load(r) for r in (base, ours, theirs, head))
idx = lambda L: {p['name']: p for p in L}
b, o, t, h = idx(B), idx(O), idx(T), idx(H)
print('counts base/ours(walk)/theirs(main)/head:', len(B), len(O), len(T), len(H))
print('duplicate names in head:', len(H) - len(h))
order = [p['name'] for p in H]
def kept(L):
    names = [p['name'] for p in L if p['name'] in h]
    pos = [order.index(n) for n in names]
    return pos == sorted(pos)
print('ours order kept:', kept(O), ' theirs order kept:', kept(T))
print('missing from head (ours):', sorted(set(o) - set(h)))
print('missing from head (theirs):', sorted(set(t) - set(h)))
print('in head but neither parent:', sorted(set(h) - set(o) - set(t)))
for n in order:
    p = h[n]
    src = []
    if n in o and o[n] == p: src.append('=ours')
    if n in t and t[n] == p: src.append('=theirs')
    if n in b and b[n] == p: src.append('=base')
    changed_o = n in o and n in b and o[n] != b[n]
    changed_t = n in t and n in b and t[n] != b[n]
    if not src or (changed_o and changed_t):
        print('HAND/CHANGED', n, 'changed in ours' if changed_o else '', 'changed in theirs' if changed_t else '', src)
print('last three plants:', order[-3:])
