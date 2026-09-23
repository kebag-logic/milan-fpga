#!/usr/bin/env python3
"""Search the published tree for base64 (all three alignments) and decimal
byte-array encodings of the recovered peer-identity tokens (length >= 4),
printing classes and file paths only.

usage: encoded_forms_sweep.py REPO ORIG_ROOT PUB_ROOT
"""
import sys, os, base64, hashlib
here = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(here, 'identity_sweep.py')).read().split("\ndef forms(")[0]
ns = {'__name__': 'x'}
repo, o, p = sys.argv[1:4]
sys.argv = ['x', repo, o, p]
exec(compile(src, 'identity_sweep.py', 'exec'), ns)
tokens = {t: c for t, c in ns['tokens'].items() if len(t) >= 4}


def b64forms(t):
    out = set()
    for pad in range(3):
        e = base64.b64encode(b'\0' * pad + t)
        # drop the chars influenced by the padding prefix and the tail
        start = ((pad * 4) + 2) // 3 + 1
        core = e[start:len(e) - 3]
        if len(core) >= 6:
            out.add(core)
    return out


hits = []
for dp, dn, fn in os.walk(p):
    for f in fn:
        path = os.path.join(dp, f)
        data = open(path, 'rb').read()
        for t, c in tokens.items():
            for core in b64forms(t):
                if core in data:
                    hits.append((c, len(t), 'base64', os.path.relpath(path, p)))
            arr = ', '.join(str(b) for b in t).encode()
            arr2 = ','.join(str(b) for b in t).encode()
            if arr in data or arr2 in data:
                hits.append((c, len(t), 'decimal-array', os.path.relpath(path, p)))
print('tokens checked (len>=4):', sorted((c, len(t), ns['ids'][t]) for t, c in tokens.items()))
print('hits:', len(hits))
for h in sorted(set(hits)):
    print('  ', h)
