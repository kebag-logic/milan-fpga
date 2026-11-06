#!/usr/bin/env python3
"""Rehash every tracked regular file and check head, tree, index tree, modes, gitlinks and stray files. Usage: verify_clone.py <clone> <head> <tree>"""
import hashlib, os, subprocess, sys
root, head, tree = sys.argv[1:4]
git = lambda *a: subprocess.run(['git', '-C', root, *a], capture_output=True, text=True, check=True).stdout
print('HEAD', git('rev-parse', 'HEAD').strip() == head, 'tree', git('rev-parse', 'HEAD^{tree}').strip() == tree, 'index tree', git('write-tree').strip() == tree)
bad = n = 0; modes = {}; links = []
for line in git('ls-files', '-s').splitlines():
    meta, path = line.split('\t', 1); mode, sha, stage = meta.split()
    modes[mode] = modes.get(mode, 0) + 1
    if mode == '160000':
        links.append((path, sha, stage)); continue
    p = os.path.join(root, path)
    data = os.readlink(p).encode() if mode == '120000' else open(p, 'rb').read()
    ok = hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest() == sha
    if mode in ('100644', '100755'):
        ok = ok and bool(os.stat(p).st_mode & 0o100) == (mode == '100755')
    n += 1; bad += not ok
    if not ok: print('DIFFERS', path)
print('tracked files rehashed', n, 'differ', bad, 'modes', modes)
print('gitlinks vs HEAD tree', all(git('rev-parse', f'HEAD:{p}').strip() == s and st == '0' for p, s, st in links), len(links))
print('status lines', len(git('status', '--porcelain', '--ignored').splitlines()))
