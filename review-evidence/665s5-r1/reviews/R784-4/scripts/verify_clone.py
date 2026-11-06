#!/usr/bin/env python3
"""The clone at the exact head: HEAD, tree, index tree, every tracked blob's bytes and mode, the gitlinks, the status.
usage: verify_clone.py <clone> <head> <tree>"""
import hashlib, os, stat, subprocess, sys
root, head, tree = sys.argv[1:4]
git = lambda *a: subprocess.run(['git', '-C', root, *a], capture_output=True, text=True, check=True).stdout
print('HEAD', git('rev-parse', 'HEAD').strip() == head, 'tree', git('rev-parse', 'HEAD^{tree}').strip() == tree, 'index tree', git('write-tree').strip() == tree)
n = differ = 0
modes, links = {}, []
for line in git('ls-files', '-s', '-z').split('\0'):
    if not line:
        continue
    meta, path = line.split('\t', 1)
    mode, sha, _ = meta.split()
    modes[mode] = modes.get(mode, 0) + 1
    if mode == '160000':
        links.append(path)
        continue
    p = os.path.join(root, path)
    data = os.readlink(p).encode() if mode == '120000' else open(p, 'rb').read()
    got = hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest()
    bad = got != sha or (mode == '100755') != bool(os.lstat(p).st_mode & stat.S_IXUSR) and mode != '120000'
    differ += bad
    n += 1
print('tracked rehashed', n, 'differ', differ, 'modes', dict(sorted(modes.items())))
print('gitlinks', len(links), links)
print('gitlinks match head', all(git('ls-tree', 'HEAD', p).split()[2] == git('ls-files', '-s', p).split()[1] for p in links))
print('status lines', len(git('status', '--porcelain', '--ignored').splitlines()))
