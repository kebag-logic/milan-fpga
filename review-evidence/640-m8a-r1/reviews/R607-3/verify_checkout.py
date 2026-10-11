#!/usr/bin/env python3
"""Prove raw tracked bytes, executable bits, index entries and required gitlinks."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

HEAD = 'ce10328c3d89d81509e47836fa4a48b22ecdbc20'
TREE = '783d10c5ae40dad516d52e1fbf77b0e25680e4a3'
ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument('repo', type=Path)
args = ap.parse_args()
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')

def git(root, *words):
    return subprocess.check_output(['git', '-C', str(root), *words], env=env)

def prove(root, revision):
    records = {}
    for record in git(root, 'ls-tree', '-rz', revision).split(b'\0'):
        if not record:
            continue
        meta, name = record.split(b'\t', 1)
        mode, kind, oid = meta.split()
        records[name] = (mode, kind, oid)
    index = {}
    for record in git(root, 'ls-files', '--stage', '-z').split(b'\0'):
        if record:
            meta, name = record.split(b'\t', 1)
            mode, oid, stage = meta.split()
            assert stage == b'0', (name, 'unmerged')
            assert name not in index
            index[name] = (mode, oid)
    assert index == {n: (m, o) for n, (m, k, o) in records.items()}, 'index differs from commit'
    count = 0
    for name, (mode, kind, oid) in records.items():
        if kind == b'commit':
            continue
        path = root / os.fsdecode(name)
        info = path.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(info.st_mode), name
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(info.st_mode), name
            actual_mode = b'100755' if info.st_mode & 0o111 else b'100644'
            assert actual_mode == mode, (name, 'mode')
            data = path.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest().encode()
        assert actual == oid, (name, 'raw bytes')
        count += 1
    return records, count

root = args.repo.resolve()
assert git(root, 'rev-parse', 'HEAD').decode().strip() == HEAD
assert git(root, 'rev-parse', 'HEAD^{tree}').decode().strip() == TREE
records, count = prove(root, HEAD)
print(json.dumps({'head': HEAD, 'tree': TREE, 'parent_blobs_verified': count, 'index': 'exact'}))
for sub in ('protocol-processor', 'gptp-processor', 'third_party/verilog-axis'):
    mode, kind, oid = records[sub.encode()]
    assert (mode, kind) == (b'160000', b'commit')
    path = root / sub
    assert not path.is_symlink() and (path / '.git').is_file()
    assert git(path, 'rev-parse', 'HEAD').strip() == oid
    assert Path(git(path, 'rev-parse', '--show-superproject-working-tree').decode().strip()).resolve() == root
    _, count = prove(path, oid.decode())
    print(json.dumps({'submodule': sub, 'gitlink': oid.decode(), 'blobs_verified': count, 'index': 'exact'}))
print('PASS: tracked bytes, modes, index and all three required submodule populations equal the exact head')
