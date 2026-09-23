#!/usr/bin/env python3
"""Report, by class/length/SHA prefix only, whether each recovered token occurs
in the tracked files of a Git tree (raw bytes, exact case, and hex).

usage: token_in_tree.py REPO ORIG_ROOT PUB_ROOT GIT_DIR REV
"""
import sys, os, subprocess, hashlib
repo, orig_root, pub_root, gitdir, rev = sys.argv[1:6]
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'identity_sweep.py')).read().split("\ndef forms(")[0]
ns = {'__name__': 'x'}
sys.argv = ['x', repo, orig_root, pub_root]
exec(compile(src, 'identity_sweep.py', 'exec'), ns)
tokens = ns['tokens']
ls = subprocess.run(['git', '--git-dir', gitdir, 'ls-tree', '-r', '-z', rev], capture_output=True, check=True).stdout
hits = {}
for ent in ls.split(b'\0'):
    if not ent:
        continue
    meta, path = ent.split(b'\t', 1)
    mode, typ, oid = meta.split()
    if typ != b'blob':
        continue
    data = subprocess.run(['git', '--git-dir', gitdir, 'cat-file', 'blob', oid], capture_output=True, check=True).stdout
    for t, c in tokens.items():
        if len(t) < 4:
            continue
        if t in data or t.hex().encode() in data.lower():
            hits.setdefault((c, len(t), ns['ids'][t]), []).append(path.decode(errors='replace'))
print('tree', rev)
for t, c in tokens.items():
    k = (c, len(t), ns['ids'][t])
    if len(t) < 4:
        print('  skip short token', k)
        continue
    v = hits.get(k, [])
    print('  ', k, 'files', len(v), v[:8])
