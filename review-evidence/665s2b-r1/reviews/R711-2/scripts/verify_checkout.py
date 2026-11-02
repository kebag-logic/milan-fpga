#!/usr/bin/env python3
"""Verify a checkout against its HEAD: tracked blob bytes and modes, index flags and required submodule gitlinks.

usage: verify_checkout.py <checkout> <head> <tree>"""
import subprocess as sp, sys, hashlib, os, stat
root, head, tree = sys.argv[1:4]
git = lambda *a: sp.check_output(['git', '-C', root, *a], text=True)
assert git('rev-parse', 'HEAD').strip() == head and git('rev-parse', 'HEAD^{tree}').strip() == tree
bad = n = 0
links = {}
for line in git('ls-tree', '-r', 'HEAD').splitlines():
    meta, path = line.split('\t', 1)
    mode, kind, sha = meta.split()
    if kind == 'commit':
        links[path] = sha
        continue
    n += 1
    full = os.path.join(root, path)
    if mode == '120000':
        data = os.readlink(full).encode()
    else:
        data = open(full, 'rb').read()
        if bool(os.stat(full).st_mode & stat.S_IXUSR) != (mode == '100755'):
            print('MODE', path); bad += 1
    if hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest() != sha:
        print('BYTES', path); bad += 1
flags = [l for l in git('ls-files', '-v').splitlines() if l[0] != 'H']
index = git('ls-files', '-s')
print(f'{n} tracked files, {bad} differ, {len(flags)} masked index entries, status lines {len(git("status", "--porcelain").splitlines())}')
for path in ('protocol-processor', 'gptp-processor', 'third_party/lwSRP', 'third_party/tsn-c-stack', 'third_party/verilog-axis'):
    now = sp.check_output(['git', '-C', os.path.join(root, path), 'rev-parse', 'HEAD'], text=True).strip()
    print(path, links[path], 'OK' if now == links[path] else f'HEAD {now}')
sys.exit(1 if bad or flags else 0)
