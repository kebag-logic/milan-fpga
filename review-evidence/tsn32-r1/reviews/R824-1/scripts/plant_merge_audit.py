#!/usr/bin/env python3
"""Audit the merged plant table: name sets, per-plant provenance and both parents' order.
usage: plant_merge_audit.py REPO BASE OURS THEIRS HEAD"""
import json, subprocess, sys
repo, base, ours, theirs, head = sys.argv[1:6]
def table(rev):
    out = subprocess.run(['git', '-C', repo, 'show', rev + ':tests/mutations.json'], check=True,
                         capture_output=True, text=True).stdout
    return json.loads(out)
B, O, T, H = (table(r) for r in (base, ours, theirs, head))
idx = lambda t: {m['name']: m for m in t}
b, o, t, h = idx(B), idx(O), idx(T), idx(H)
print('counts base %d ours %d theirs %d head %d' % (len(B), len(O), len(T), len(H)))
print('head unique names:', len(h) == len(H))
print('head == ours|theirs names:', set(h) == set(o) | set(t))
print('dropped from base (ours, theirs):', sorted(set(b) - set(o)), sorted(set(b) - set(t)))
print('in head but neither parent:', sorted(set(h) - set(o) - set(t)))
print('missing from head:', sorted((set(o) | set(t)) - set(h)))
both, one, same = [], [], 0
for n, m in h.items():
    vo, vt, vb = o.get(n), t.get(n), b.get(n)
    if vo == m and (vt is None or vt == m): same += 1; continue
    if vt == m and (vo is None or vo == m): same += 1; continue
    co = vb is not None and vo is not None and vo != vb
    ct = vb is not None and vt is not None and vt != vb
    if m == vo and not ct: one.append((n, 'ours')); continue
    if m == vt and not co: one.append((n, 'theirs')); continue
    both.append((n, co, ct))
print('plants equal to an unconflicted parent version:', same + len(one))
print('plants differing from every parent version (hand-merged or re-anchored):')
for n, co, ct in both:
    print('  %s changed-ours=%s changed-theirs=%s' % (n, co, ct))
    for side, v in (('base', b.get(n)), ('ours', o.get(n)), ('theirs', t.get(n)), ('head', h[n])):
        if v: print('    %-6s old=%r\n           new=%r' % (side, v['old'], v['new']))
    kh = h[n]['kills']; print('    kills head == ours:', kh == (o.get(n) or {}).get('kills'), ' == theirs:', kh == (t.get(n) or {}).get('kills'))
def subseq(sub, full):
    pos = {n: i for i, n in enumerate(full)}
    seq = [pos[n] for n in sub if n in pos]
    return seq == sorted(seq)
names = [m['name'] for m in H]
print('ours order kept:', subseq([m['name'] for m in O], names))
print('theirs order kept:', subseq([m['name'] for m in T], names))
print('last three:', names[-3:])
print('last three paths:', [m['path'] for m in H[-3:]])
walk = [n for n in names if n.startswith('walk-')]
print('walk- plants:', len(walk), 'contiguous:', names.index(walk[-1]) - names.index(walk[0]) + 1 == len(walk))
print('index first walk', names.index(walk[0]), 'neighbours', names[names.index(walk[0]) - 1], '|', names[names.index(walk[-1]) + 1])
