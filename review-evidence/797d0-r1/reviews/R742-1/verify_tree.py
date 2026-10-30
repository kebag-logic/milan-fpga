#!/usr/bin/env python3
"""Prove tracked bytes, file kinds, executable modes, index and gitlinks."""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')
head = 'bd16b371ae5de1c4d36ea2a018e7d756c62d4b5a'
tree = '3a039c9e8d8fc05fa9e54a3976edba9f84b21819'
def git(where, *args):
    return subprocess.check_output(['git', '-C', str(where), *args], env=env)
assert git(root, 'rev-parse', 'HEAD').decode().strip() == head
assert git(root, 'rev-parse', 'HEAD^{tree}').decode().strip() == tree

def verify(where, revision, label):
    expected = {}
    for row in git(where, 'ls-tree', '-rz', revision).split(b'\0'):
        if not row:
            continue
        metadata, rawpath = row.split(b'\t', 1)
        mode, kind, oid = metadata.decode().split()
        expected[os.fsdecode(rawpath)] = (mode, oid)
    actual_index = {}
    for row in git(where, 'ls-files', '--stage', '-z').split(b'\0'):
        if not row:
            continue
        metadata, rawpath = row.split(b'\t', 1)
        mode, oid, stage = metadata.decode().split()
        assert stage == '0'
        actual_index[os.fsdecode(rawpath)] = (mode, oid)
    assert expected == actual_index, label + ': index differs from commit'
    count = 0
    for path, (mode, oid) in expected.items():
        file = where / path
        if mode == '160000':
            if (file / '.git').exists():
                assert git(file, 'rev-parse', 'HEAD').decode().strip() == oid, path
                verify(file, oid, path)
            else:
                assert label == 'root' and path == 'external', path
                print(f'{path}: uninitialized optional gitlink {oid}; index verified')
            continue
        info = file.lstat()
        if mode == '120000':
            assert stat.S_ISLNK(info.st_mode), path
            data = os.fsencode(os.readlink(file))
        else:
            assert stat.S_ISREG(info.st_mode), path
            assert bool(info.st_mode & 0o111) == (mode == '100755'), path
            data = file.read_bytes()
        digest = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert digest == oid, label + '/' + path
        count += 1
    print(f'{label}: {count} tracked blobs match bytes, kinds and executable modes; index exact; revision {revision}')

verify(root, head, 'root')
print(f'HEAD {head}; TREE {tree}; verification PASS')
