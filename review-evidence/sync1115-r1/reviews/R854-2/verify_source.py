#!/usr/bin/env python3
"""Verify actual tracked bytes, modes and complete index against immutable trees."""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
expected = 'e2be92b0e0f9a8f0529dea252f23ed44a21e050a'
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')

def git(path, *args):
    return subprocess.check_output(['git', '-C', str(path), *args], env=env)

def verify(path, revision, recurse):
    assert git(path, 'rev-parse', 'HEAD').decode().strip() == revision
    entries = git(path, 'ls-tree', '-rz', '--full-tree', revision).split(b'\0')
    expected_index = set()
    blobs = links = 0
    for entry in filter(None, entries):
        meta, raw_name = entry.split(b'\t', 1)
        mode, kind, oid = meta.split()
        expected_index.add(mode + b' ' + oid + b' 0\t' + raw_name)
        name = os.fsdecode(raw_name)
        target = path / name
        if kind == b'commit':
            links += 1
            if recurse:
                if name == 'external':
                    print('GITLINK external', oid.decode(), 'uninitialized; excluded from required inputs')
                else:
                    assert (target / '.git').is_file(), name
                    verify(target, oid.decode(), False)
                    print('GITLINK', name, oid.decode(), 'verified')
            continue
        info = target.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(info.st_mode), name
            data = os.fsencode(os.readlink(target))
        else:
            assert stat.S_ISREG(info.st_mode), name
            actual_mode = b'100755' if info.st_mode & 0o111 else b'100644'
            assert mode == actual_mode, (name, mode, actual_mode)
            data = target.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert actual == oid.decode(), name
        blobs += 1
    actual_index = set(filter(None, git(path, 'ls-files', '--stage', '-z').split(b'\0')))
    assert actual_index == expected_index, 'index mismatch'
    print('TREE', revision, 'blobs', blobs, 'gitlinks', links, 'bytes/modes/index PASS')

print('HEAD', expected)
print('tree', git(root, 'rev-parse', 'HEAD^{tree}').decode().strip())
verify(root, expected, True)
assert not git(root, 'status', '--porcelain', '--untracked-files=all')
print('CLEAN: exact head bytes, modes, index and required submodule gitlinks; no restoration needed')
