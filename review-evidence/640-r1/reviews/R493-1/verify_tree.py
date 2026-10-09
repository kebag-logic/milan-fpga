#!/usr/bin/env python3
"""Verify actual tracked bytes, modes, index entries and required gitlinks."""
import hashlib
import json
import os
import stat
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')
HEAD = 'c4b8b7d373c9233bc9e71c6ed32eae9ad2b3f970'
TREE = 'a95adb1ad43e09865509188697ec4a96f42d7a83'
required = ['protocol-processor', 'gptp-processor', 'third_party/verilog-axis']

def git(path, *args):
    return subprocess.check_output(['git', '-C', str(path), *args], env=env)

def verify(path, revision):
    tree = git(path, 'ls-tree', '-rz', '--full-tree', revision)
    expected_index = []
    count = 0
    links = {}
    for entry in tree.split(b'\0'):
        if not entry:
            continue
        meta, name = entry.split(b'\t', 1)
        mode, kind, oid = meta.split()
        expected_index.append(mode + b' ' + oid + b' 0\t' + name)
        filename = path / os.fsdecode(name)
        if kind == b'commit':
            links[os.fsdecode(name)] = oid.decode()
            continue
        info = filename.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(info.st_mode), name
            data = os.fsencode(os.readlink(filename))
        else:
            assert stat.S_ISREG(info.st_mode), name
            actual_mode = b'100755' if info.st_mode & 0o111 else b'100644'
            assert actual_mode == mode, (name, actual_mode, mode)
            data = filename.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert actual.encode() == oid, (name, actual, oid)
        count += 1
    index = git(path, 'ls-files', '--stage', '-z')
    assert sorted(index.rstrip(b'\0').split(b'\0')) == sorted(expected_index), 'index/tree mismatch'
    assert git(path, 'rev-parse', 'HEAD').decode().strip() == revision
    return {'revision':revision, 'tree':git(path, 'rev-parse', revision+'^{tree}').decode().strip(),
            'verified_blobs':count, 'verified_index_sha256':hashlib.sha256(index).hexdigest(), 'gitlinks':links}

result = {'root': verify(root, HEAD)}
assert result['root']['tree'] == TREE
for name in required:
    path = root / name
    assert not path.is_symlink()
    assert (path / '.git').is_file(), 'required submodule must be initialized'
    result[name] = verify(path, result['root']['gitlinks'][name])
result['status'] = git(root, 'status', '--short', '--untracked-files=normal').decode()
print(json.dumps(result, indent=2))
