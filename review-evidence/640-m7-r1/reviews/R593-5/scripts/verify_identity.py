#!/usr/bin/env python3
"""Prove raw tracked bytes, modes, stage-zero index and required gitlinks."""
import hashlib
import os
import stat
import subprocess
import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
HEAD = '4c5d70b50230fbd5da347852d39daf7f23b3df0b'
TREE = '8156e281ac181efc76139470e3cf5c530ae17793'
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')

def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], env=env)

def verify(root, revision):
    entries = {}
    for record in git(root, 'ls-tree', '-rz', revision).split(b'\0'):
        if not record:
            continue
        meta, path = record.split(b'\t', 1)
        mode, kind, oid = meta.split()
        entries[path] = (mode, kind, oid)
    indexed = {}
    for record in git(root, 'ls-files', '--stage', '-z').split(b'\0'):
        if not record:
            continue
        meta, path = record.split(b'\t', 1)
        mode, oid, stage = meta.split()
        assert stage == b'0', (root.name, path, stage)
        assert path not in indexed
        indexed[path] = (mode, b'commit' if mode == b'160000' else b'blob', oid)
    assert entries == indexed, f'index differs: {root.name}'
    count = 0
    for name, (mode, kind, oid) in entries.items():
        path = root / os.fsdecode(name)
        if kind == b'commit':
            continue
        info = path.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(info.st_mode)
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(info.st_mode), (path, 'not regular')
            assert bool(info.st_mode & stat.S_IXUSR) == (mode == b'100755'), (path, 'mode')
            data = path.read_bytes()
        got = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest().encode()
        assert got == oid, (path, 'blob mismatch')
        count += 1
    return entries, count

assert git(repo, 'rev-parse', 'HEAD').decode().strip() == HEAD
assert git(repo, 'rev-parse', 'HEAD^{tree}').decode().strip() == TREE
entries, count = verify(repo, HEAD)
print(f'PASS parent {HEAD}, tree {TREE}: {count} raw blobs, modes and full stage-zero index')
dependencies = 0
for name, (mode, kind, oid) in entries.items():
    if kind != b'commit':
        continue
    path = repo / os.fsdecode(name)
    if name == b'external':
        assert not (path / '.git').exists()
        print('PASS external gitlink', oid.decode(), '(unused checkout remains uninitialized)')
        continue
    assert path.is_dir() and not path.is_symlink()
    assert (path / '.git').is_file(), (name, 'not an initialized submodule')
    assert git(path, 'rev-parse', '--show-toplevel').decode().strip() == str(path)
    assert git(path, 'rev-parse', 'HEAD').strip() == oid
    _, files = verify(path, oid.decode())
    dependencies += files
    print('PASS gitlink', os.fsdecode(name), oid.decode(), f'{files} raw blobs, modes and index')
assert not git(repo, 'diff', '--raw', '412e3f6c', HEAD, '--', 'hdl', 'gptp-processor')
print(f'PASS dependencies: {dependencies} raw blobs; all root gitlinks verified; RTL and donor unchanged in delta')
print('status:', git(repo, 'status', '--porcelain=v1', '--untracked-files=normal').decode().strip() or 'clean')
