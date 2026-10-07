#!/usr/bin/env python3
"""Prove raw tracked bytes, modes, index entries and initialized gitlinks."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], env={**os.environ, 'GIT_NO_REPLACE_OBJECTS': '1'})

def verify(root, revision):
    tree = git(root, 'ls-tree', '-rz', revision)
    expected = []
    files = 0
    links = []
    for entry in tree.split(b'\0'):
        if not entry:
            continue
        header, name = entry.split(b'\t', 1)
        mode, kind, oid = header.split()
        path = root / os.fsdecode(name)
        expected.append(mode + b' ' + oid + b' 0\t' + name)
        if kind == b'commit':
            if not (path / '.git').exists():
                assert name == b'external', ('missing required submodule', name)
                links.append({'path': os.fsdecode(name), 'pin': oid.decode(), 'state': 'uninitialized optional external'})
            else:
                assert git(path, 'rev-parse', 'HEAD').strip() == oid
                links.append({'path': os.fsdecode(name), 'pin': oid.decode(), 'state': 'verified', 'contents': verify(path, oid.decode())})
            continue
        info = path.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(info.st_mode), name
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(info.st_mode), name
            assert bool(info.st_mode & stat.S_IXUSR) == (mode == b'100755'), name
            data = path.read_bytes()
        digest = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest().encode()
        assert digest == oid, ('blob mismatch', name)
        files += 1
    index = git(root, 'ls-files', '--stage', '-z').split(b'\0')
    assert sorted(x for x in index if x) == sorted(expected), 'index mismatch'
    return {'revision': revision, 'tree': git(root, 'rev-parse', revision + '^{tree}').decode().strip(), 'verified_blobs': files, 'gitlinks': links}

if __name__ == '__main__':
    root = Path(sys.argv[1]).resolve()
    print(json.dumps(verify(root, sys.argv[2]), indent=2))
