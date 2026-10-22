#!/usr/bin/env python3
"""Verify tracked bytes, modes, stage-zero index, and initialized gitlinks."""
import hashlib
import os
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args])
def audit(repo, label, expected):
    assert git(repo, 'rev-parse', 'HEAD').decode().strip() == expected
    entries = []
    for raw in git(repo, 'ls-tree', '-rz', 'HEAD').split(b'\0'):
        if raw:
            info, name = raw.split(b'\t', 1)
            mode, kind, oid = info.split()
            entries.append((mode, kind, oid, name))
    expected_index = {mode + b' ' + oid + b' 0\t' + name for mode, kind, oid, name in entries}
    actual_index = set(git(repo, 'ls-files', '--stage', '-z').split(b'\0')) - {b''}
    assert actual_index == expected_index, (label, 'index mismatch')
    blobs = 0
    for mode, kind, oid, name in entries:
        path = repo / os.fsdecode(name)
        if kind == b'commit':
            print('GITLINK', label + '/' + os.fsdecode(name), oid.decode())
            if (path / '.git').exists():
                audit(path, label + '/' + os.fsdecode(name), oid.decode())
            else:
                print('UNINITIALIZED (index verified)', label + '/' + os.fsdecode(name))
            continue
        assert kind == b'blob'
        if mode == b'120000':
            assert path.is_symlink()
            data = os.fsencode(os.readlink(path))
        else:
            assert path.is_file() and not path.is_symlink()
            assert bool(path.stat().st_mode & 0o111) == (mode == b'100755'), (label, name, 'mode')
            data = path.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest().encode()
        assert actual == oid, (label, name, 'bytes')
        blobs += 1
    print('PASS', label, expected, 'tracked blobs', blobs, 'index and modes exact')

head = 'a97aea01449492b1f640924f5a34726f602cabed'
assert git(root, 'rev-parse', 'HEAD^{tree}').decode().strip() == 'ea69f3b4c4c4b2f50a38a868b5f1dba56b248249'
audit(root, 'parent', head)
assert git(root, 'status', '--porcelain', '--untracked-files=no') == b''
print('PASS final parent tracked status clean')
