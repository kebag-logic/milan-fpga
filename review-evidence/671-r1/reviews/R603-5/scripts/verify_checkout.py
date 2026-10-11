#!/usr/bin/env python3
"""Verify tree/index identities and on-disk blob bytes, kinds and modes."""
import argparse
import hashlib
import os
from pathlib import Path
import stat
import subprocess

HEAD = '0c276b621d638c9a83e82f71fbf07bc153517bf7'
TREE = '85eb43d180dc240f5fa838e05dc6cbae6c7dd67a'
REQUIRED = ('protocol-processor', 'gptp-processor', 'third_party/verilog-axis')
p = argparse.ArgumentParser()
p.add_argument('root', type=Path)
a = p.parse_args()
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')

def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], env=env)

def verify(root, commit):
    entries = {}
    for row in git(root, 'ls-tree', '-rz', commit).split(b'\0'):
        if row:
            fields, name = row.split(b'\t', 1)
            mode, kind, oid = fields.split()
            entries[name] = (mode, kind, oid)
    index = {}
    for row in git(root, 'ls-files', '--stage', '-z').split(b'\0'):
        if row:
            fields, name = row.split(b'\t', 1)
            mode, oid, stage = fields.split()
            assert stage == b'0', (name, stage)
            index[name] = (mode, oid)
    assert index == {name:(mode,oid) for name,(mode,kind,oid) in entries.items()}
    count = 0
    for name, (mode,kind,oid) in entries.items():
        if kind != b'blob':
            continue
        path = root / os.fsdecode(name)
        st = path.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(st.st_mode), name
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode), name
            assert bool(st.st_mode & 0o111) == (mode == b'100755'), name
            data = path.read_bytes()
        digest = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest().encode()
        assert digest == oid, name
        count += 1
    return count, entries

assert git(a.root, 'rev-parse', 'HEAD').decode().strip() == HEAD
assert git(a.root, 'rev-parse', 'HEAD^{tree}').decode().strip() == TREE
detached = subprocess.run(['git', '-C', str(a.root), 'symbolic-ref', '-q', 'HEAD'],
                          env=env, capture_output=True)
assert detached.returncode == 1, 'HEAD must stay detached'
n, entries = verify(a.root, HEAD)
print('HEAD', HEAD, '\nTREE', TREE)
print(f'PASS parent: {n} tracked blobs: raw bytes, file kinds, executable modes, index')
for name in REQUIRED:
    mode,kind,oid = entries[name.encode()]
    assert mode == b'160000' and kind == b'commit'
    root = a.root / name
    assert not root.is_symlink()
    assert (root / '.git').is_file()
    assert git(root, 'rev-parse', 'HEAD').strip() == oid
    assert git(root, 'rev-parse', '--show-superproject-working-tree').decode().strip() == str(a.root.resolve())
    n, _ = verify(root, oid.decode())
    print(f'PASS {name}: {oid.decode()}, {n} pinned blobs, raw bytes/modes/index')
assert not git(a.root, 'status', '--porcelain', '--untracked-files=no').strip()
print('PASS detached HEAD and no tracked changes')
