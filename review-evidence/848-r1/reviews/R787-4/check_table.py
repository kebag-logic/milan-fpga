#!/usr/bin/env python3
"""Three-way compare of ci/image/command-table.json across dev, the two merge parents and the head."""
import json, subprocess, sys
revs = dict(dev='3f6bef88bd8a78cb2833a12572b9c4a9013f9bdf', pr849='171fd56b2c50a44ed75a32c1b9bbd7ae818f2c22',
            pr842='8ab3a930d6e2d217caf729d38c5ef17e98e292b3', head='9d5a5af78f95f655e5104056c2c0ee2cca689279')
def load(r):
    return json.loads(subprocess.check_output(['git', 'show', r + ':ci/image/command-table.json']))
T = {k: load(v) for k, v in revs.items()}
def flat(o, p=''):
    out = {}
    if isinstance(o, dict):
        for k, v in o.items():
            out.update(flat(v, p + '/' + str(k)))
    elif isinstance(o, list):
        # lists are compared by canonical member, so an insert does not shift every index
        for v in o:
            s = json.dumps(v, sort_keys=True)
            out[p + '[]' + s] = True
        if not o:
            out[p + '[]'] = True
    else:
        out[p] = o
    return out
F = {k: flat(v) for k, v in T.items()}
print('top keys', {k: sorted(v)[:12] for k, v in T.items() if k == 'head'})
print('leaf counts', {k: len(v) for k, v in F.items()})
bad = 0
keys = set().union(*[set(v) for v in F.values()])
for key in sorted(keys):
    d, a, b, h = (F[n].get(key, '<absent>') for n in ('dev', 'pr849', 'pr842', 'head'))
    if a == d and b == d:
        want = d
    elif a != d and b == d:
        want = a
    elif b != d and a == d:
        want = b
    elif a == b:
        want = a
    else:
        print('BOTH-CHANGED', key[:150], d, a, b, h); want = None
    if want is not None and h != want:
        bad += 1; print('MISMATCH', key[:170], 'dev', d, '849', a, '842', b, 'head', h)
    if not (a == d and b == d):
        print('changed', key[:170], '|dev', str(d)[:20], '|849', str(a)[:20], '|842', str(b)[:20], '|head', str(h)[:20])
print('mismatches', bad)
sys.exit(1 if bad else 0)
