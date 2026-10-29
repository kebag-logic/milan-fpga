#!/usr/bin/env python3
"""Prove raw worktree blobs, modes, stage-zero index and initialized submodule gitlinks."""
import hashlib
import os
from pathlib import Path
import stat
import subprocess

HEAD = '99de3a023abfda5604a70832e23baf7ff73481a3'
TREE = '715917bbb3c732168a35124b1571a3d2f8401580'
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')

def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], env=env)

def verify(root, expected, label):
    assert git(root, 'rev-parse', 'HEAD').decode().strip() == expected, label
    records = git(root, 'ls-tree', '-rz', '--full-tree', expected).split(b'\0')
    expected_index = []
    submodules = []
    count = 0
    for record in filter(None, records):
        meta, name = record.split(b'\t',1)
        mode, kind, oid = meta.split()
        expected_index.append(mode + b' ' + oid + b' 0\t' + name)
        path = root / os.fsdecode(name)
        if kind == b'commit':
            submodules.append((path, oid.decode(), os.fsdecode(name)))
            continue
        st = path.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(st.st_mode), name
            content = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode), name
            assert bool(st.st_mode & 0o111) == (mode == b'100755'), name
            content = path.read_bytes()
        digest = hashlib.sha1(b'blob ' + str(len(content)).encode() + b'\0' + content).hexdigest()
        assert digest == oid.decode(), (label, name)
        count += 1
    actual_index = list(filter(None, git(root, 'ls-files', '--stage', '-z').split(b'\0')))
    assert sorted(actual_index) == sorted(expected_index), label + ' index mismatch'
    print(label, expected, 'raw blobs/modes and exact stage-zero index PASS;', count, 'blobs')
    for path, oid, name in submodules:
        if label == 'superproject' and name == 'external':
            print('external gitlink retained', oid, '; intentionally uninitialized, no gate reads it')
            continue
        assert (path / '.git').exists() and not path.is_symlink(), name
        verify(path, oid, label + '/' + name)

root = Path.cwd()
assert git(root, 'rev-parse', 'HEAD^{tree}').decode().strip() == TREE
verify(root, HEAD, 'superproject')
print('Exact head/tree and all required submodule gitlinks verified.')
status = git(root, 'status', '--porcelain=v1').decode()
print('Git status:', status if status else 'clean')
assert not status
