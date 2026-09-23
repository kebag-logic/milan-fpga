#!/usr/bin/env python3
"""Per capture file: occurrences of each recovered token (by class, length and
SHA-256 prefix, never the text) in the ORIGINAL and the PUBLISHED copy.

usage: pcap_token_counts.py REPO ORIG_ROOT PUB_ROOT
"""
import sys, os, hashlib
repo, orig_root, pub_root = sys.argv[1:4]
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'identity_sweep.py')).read().split("\ndef forms(")[0]
ns = {'__name__': 'x'}
sys.argv = ['x', repo, orig_root, pub_root]
exec(compile(src, 'identity_sweep.py', 'exec'), ns)
tokens = ns['tokens']
for dp, dn, fn in os.walk(pub_root):
    for f in sorted(fn):
        p = os.path.join(dp, f)
        rel = os.path.relpath(p, pub_root)
        b = open(p, 'rb').read()
        po = os.path.join(orig_root, rel)
        a = open(po, 'rb').read() if os.path.exists(po) else b''
        for t, c in tokens.items():
            na, nb = a.count(t), b.count(t)
            ha, hb = a.lower().count(t.hex().encode()), b.lower().count(t.hex().encode())
            if na or nb or ha or hb:
                print(rel, c, 'len', len(t), ns['ids'][t],
                      'raw orig', na, 'pub', nb, '| hex orig', ha, 'pub', hb)
