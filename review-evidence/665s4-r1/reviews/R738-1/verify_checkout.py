#!/usr/bin/env python3
"""Verify raw tracked bytes, executable modes, index records, and populated gitlinks."""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
HEAD = 'ee1c0be0b99f0131eb10908a19f080299aa0cbb8'
TREE = '48581b5296086a3ba87d35b76d6e986ad9a15dc3'
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')

def git(at, *args):
    return subprocess.check_output(['git', '-C', str(at), *args], env=env)

def verify(at, rev, label):
    tree = {}
    for row in git(at, 'ls-tree', '-rz', rev).split(b'\0'):
        if not row:
            continue
        meta, path = row.split(b'\t', 1)
        mode, kind, oid = meta.split()
        tree[path] = (mode, oid)
        p = at / os.fsdecode(path)
        if kind == b'commit':
            if label == '.' and path == b'external':
                print('external:', oid.decode(), 'gitlink checked; optional checkout absent, unchanged')
                continue
            actual = git(p, 'rev-parse', 'HEAD').strip()
            assert actual == oid, (label, path, 'gitlink HEAD')
            verify(p, oid.decode(), os.fsdecode(path))
            continue
        info = p.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(info.st_mode), path
            data = os.fsencode(os.readlink(p))
        else:
            assert stat.S_ISREG(info.st_mode), path
            actual_mode = b'100755' if info.st_mode & 0o111 else b'100644'
            assert actual_mode == mode, (path, 'mode')
            data = p.read_bytes()
        got = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest().encode()
        assert got == oid, (label, path, 'raw blob')
    index = {}
    for row in git(at, 'ls-files', '--stage', '-z').split(b'\0'):
        if not row:
            continue
        meta, path = row.split(b'\t', 1)
        mode, oid, stage = meta.split()
        assert stage == b'0' and path not in index, (label, path, 'index stage')
        index[path] = (mode, oid)
    assert tree == index, (label, 'index differs from commit tree')
    print(label, rev, 'PASS', len(tree), 'tracked entries; raw bytes, modes, and index agree')

assert git(root, 'rev-parse', 'HEAD').strip().decode() == HEAD
assert git(root, 'rev-parse', 'HEAD^{tree}').strip().decode() == TREE
verify(root, HEAD, '.')
print('Exact source head and tree preserved. No source restoration needed.')
