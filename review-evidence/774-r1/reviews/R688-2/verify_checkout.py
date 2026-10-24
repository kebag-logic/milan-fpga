#!/usr/bin/env python3
"""Prove tracked bytes, executable modes, indexes and populated gitlinks."""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
env = os.environ.copy()
env['GIT_NO_REPLACE_OBJECTS'] = '1'
def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args], env=env)
def verify(repo, revision, label):
    tree = {}
    for record in git(repo, 'ls-tree', '-rz', revision).split(b'\0'):
        if not record:
            continue
        metadata, path = record.split(b'\t', 1)
        mode, kind, oid = metadata.split()
        tree[path] = (mode, oid)
        f = repo / os.fsdecode(path)
        if kind == b'commit':
            continue
        s = f.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(s.st_mode), path
            data = os.fsencode(os.readlink(f))
        else:
            assert stat.S_ISREG(s.st_mode), path
            expected = b'100755' if s.st_mode & 0o111 else b'100644'
            assert mode == expected, path
            data = f.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest().encode()
        assert actual == oid, path
    index = {}
    for record in git(repo, 'ls-files', '--stage', '-z').split(b'\0'):
        if not record:
            continue
        metadata, path = record.split(b'\t', 1)
        mode, oid, stage = metadata.split()
        assert stage == b'0', path
        assert path not in index, path
        index[path] = (mode, oid)
    assert index == tree, label
    print(f'PASS {label}: {len(tree)} tracked entries; exact bytes/modes and index match {revision}')
    return tree

head = git(root, 'rev-parse', 'HEAD').decode().strip()
assert head == '01fc54756f1ffb0a3aa836681215e8321ee7e86c'
print('HEAD', head)
print('TREE', git(root, 'rev-parse', 'HEAD^{tree}').decode().strip())
tree = verify(root, head, 'superproject')
for path, (mode, oid) in tree.items():
    if mode != b'160000':
        continue
    sub = root / os.fsdecode(path)
    name = os.fsdecode(path)
    if not (sub / '.git').exists():
        assert name == 'external', name
        print(f'UNCHANGED uninitialized optional gitlink {name}: {oid.decode()}')
        continue
    assert git(sub, 'rev-parse', 'HEAD').strip() == oid, name
    verify(sub, oid.decode(), name)
assert not git(root, 'diff', '--raw', 'HEAD').strip()
assert not git(root, 'diff', '--cached', '--raw', 'HEAD').strip()
print('PASS required submodule pins and all tracked checkout/index entries are unchanged.')
