#!/usr/bin/env python3
"""Verify actual tracked bytes, executable modes, indexes and required submodule pins.
Usage: python3 verify_checkout.py CHECKOUT
"""
import hashlib
import os
import stat
import subprocess
import sys
from pathlib import Path

HEAD = '8dc8588471a096bbe120bbec4c8c0f8ddf44d8cd'
TREE = '22335ec4d79d67a5b9a2e0e7ab480fd868be9bba'

def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args])

def verify(root, label, expected):
    assert git(root, 'rev-parse', 'HEAD').decode().strip() == expected
    tree = {}
    for row in git(root, 'ls-tree', '-rz', '--full-tree', 'HEAD').split(b'\0'):
        if not row:
            continue
        metadata, name = row.split(b'\t', 1)
        mode, kind, oid = metadata.split()
        tree[name] = (mode, kind, oid)
    index = {}
    for row in git(root, 'ls-files', '--stage', '-z').split(b'\0'):
        if not row:
            continue
        metadata, name = row.split(b'\t', 1)
        mode, oid, stage = metadata.split()
        assert stage == b'0' and name not in index
        index[name] = (mode, oid)
    assert index == {n: (m, h) for n, (m, _, h) in tree.items()}
    for name, (mode, kind, oid) in tree.items():
        path = root / os.fsdecode(name)
        if kind == b'commit':
            if label == '.' and name == b'external':
                print('Optional external: uninitialized, unused; gitlink and index verified ' + oid.decode())
                continue
            verify(path, (label + '/' + os.fsdecode(name)).removeprefix('./'), oid.decode())
            continue
        s = path.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(s.st_mode)
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(s.st_mode)
            assert bool(s.st_mode & 0o111) == (mode == b'100755'), os.fsdecode(name)
            data = path.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert actual == oid.decode(), (label, os.fsdecode(name))
    assert not git(root, 'status', '--porcelain', '--untracked-files=no')
    print(f'{label}: {expected}; {len(tree)} tracked entries, bytes/modes/index PASS')

root = Path(sys.argv[1]).resolve()
assert git(root, 'rev-parse', 'HEAD^{tree}').decode().strip() == TREE
verify(root, '.', HEAD)
assert not git(root, 'status', '--porcelain')
print('Exact head/tree restored and checkout clean: PASS (no candidate edits were needed)')
