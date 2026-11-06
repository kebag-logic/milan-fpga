#!/usr/bin/env python3
"""Every tracked file of CLONE rehashed against HEAD: blob bytes, modes, index, and the gitlinks.

usage: verify_clone.py CLONE HEAD TREE
"""
import hashlib, os, subprocess, sys
c, head, tree = sys.argv[1:4]
g = lambda *a: subprocess.run(['git', '-C', c, *a], capture_output=True, text=True, check=True).stdout
print('HEAD', g('rev-parse', 'HEAD').strip() == head, 'tree', g('rev-parse', 'HEAD^{tree}').strip() == tree,
      'index tree', g('write-tree').strip() == tree)
rows = [l.split('\t', 1) for l in g('ls-tree', '-r', '--full-tree', 'HEAD').splitlines()]
differ = 0; modes = {}; links = []
for meta, path in rows:
    mode, kind, sha = meta.split()
    modes[mode] = modes.get(mode, 0) + 1
    full = os.path.join(c, path)
    if kind == 'commit':
        links.append((path, sha)); continue
    if mode == '120000':
        data = os.readlink(full).encode()
    else:
        data = open(full, 'rb').read()
        if bool(os.stat(full).st_mode & 0o100) != (mode == '100755'): differ += 1; print('mode', path)
    if hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest() != sha: differ += 1; print('bytes', path)
print('tracked rehashed', len(rows), 'differ', differ, 'modes', modes)
stage = dict((l.split('\t')[1], l.split()[1]) for l in g('ls-files', '-s').splitlines() if l.startswith('160000'))
print('gitlinks vs index', all(stage.get(p) == s for p, s in links), len(links), [p for p, _ in links])
print('status lines', len(g('status', '--porcelain').splitlines()))
