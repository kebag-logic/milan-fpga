#!/usr/bin/env python3
"""Hash actual tracked bytes, executable modes and complete indexes recursively."""
import hashlib
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
HEAD = '8dc8588471a096bbe120bbec4c8c0f8ddf44d8cd'
TREE = '22335ec4d79d67a5b9a2e0e7ab480fd868be9bba'
def git(root, *args):
    return subprocess.check_output(['git', '--no-replace-objects', '-C', str(root), *args])
def verify(root, rev, label):
    assert git(root, 'rev-parse', 'HEAD').decode().strip() == rev
    rows = {}
    for record in git(root, 'ls-tree', '-rz', rev).split(b'\0'):
        if not record:
            continue
        meta, path = record.split(b'\t', 1)
        mode, kind, oid = meta.decode().split()
        name = os.fsdecode(path)
        rows[name] = (mode, oid)
        p = root / name
        if mode == '160000':
            if name == 'external':
                print(label, 'optional external gitlink', oid, '(not initialized or used)')
            else:
                verify(p, oid, label + '/' + name)
            continue
        if mode == '120000':
            assert p.is_symlink(), name
            data = os.fsencode(os.readlink(p))
        else:
            assert p.is_file() and not p.is_symlink(), name
            data = p.read_bytes()
            actual = '100755' if p.stat().st_mode & 0o111 else '100644'
            assert actual == mode, (name, mode, actual)
        digest = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert digest == oid, (label, name, digest, oid)
    index = {}
    for record in git(root, 'ls-files', '--stage', '-z').split(b'\0'):
        if not record:
            continue
        meta, path = record.split(b'\t', 1)
        mode, oid, stage = meta.decode().split()
        assert stage == '0'
        index[os.fsdecode(path)] = (mode, oid)
    assert index == rows, label
    assert not git(root, 'status', '--porcelain', '--untracked-files=all'), label
    print(label, rev, len(rows), 'entries: bytes, modes, index and clean status PASS')

assert git(ROOT, 'rev-parse', 'HEAD^{tree}').decode().strip() == TREE
verify(ROOT, HEAD, 'checkout')
print('Exact head and tree restored; all five required submodules verified')
