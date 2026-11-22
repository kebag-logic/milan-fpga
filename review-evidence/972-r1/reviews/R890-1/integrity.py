#!/usr/bin/env python3
"""Verify raw tracked bytes, executable modes, index entries, and initialized gitlinks."""
import hashlib
import os
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
def git(at, *args):
    return subprocess.check_output(['git', '-C', str(at), *args])
def check(at, name):
    entries = git(at, 'ls-tree', '-r', '-z', 'HEAD').split(b'\0')
    expected = {}
    count = 0
    for entry in filter(None, entries):
        meta, path = entry.split(b'\t')
        mode, kind, oid = meta.split()
        expected[path] = (mode, oid)
        file = at / os.fsdecode(path)
        if kind == b'commit':
            if not (file / '.git').exists():
                print(f'{name}/{os.fsdecode(path)} uninitialized gitlink {oid.decode()}')
                continue
            actual = git(file, 'rev-parse', 'HEAD').strip()
            assert actual == oid, (path, 'gitlink mismatch')
            check(file, name + '/' + os.fsdecode(path))
            continue
        data = os.fsencode(os.readlink(file)) if mode == b'120000' else file.read_bytes()
        blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest().encode()
        assert blob == oid, (path, 'raw blob mismatch')
        actual_mode = b'120000' if file.is_symlink() else b'100755' if file.stat().st_mode & 0o111 else b'100644'
        assert mode == actual_mode, (path, 'mode mismatch')
        count += 1
    indexed = {}
    for entry in filter(None, git(at, 'ls-files', '--stage', '-z').split(b'\0')):
        meta, path = entry.split(b'\t')
        mode, oid, stage = meta.split()
        assert stage == b'0', (path, 'unmerged index')
        indexed[path] = (mode, oid)
    assert indexed == expected, (name, 'index mismatch')
    print(f'{name}: {count} raw tracked blobs/modes and full index match HEAD {git(at,"rev-parse","HEAD").decode().strip()}')
assert git(root, 'rev-parse', 'HEAD').strip() == b'0f508a01b5d02fbf192ab08e4d8a5bf514b32a3b'
assert git(root, 'rev-parse', 'HEAD^{tree}').strip() == b'4a0fc0a2ee1159adffb276c1c00ef936c51b313f'
check(root, 'candidate')
print('PASS: tracked blobs, modes, index and all initialized submodule pins unchanged')
