#!/usr/bin/env python3
"""Check raw tracked bytes, modes, index entries and required gitlinks."""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys

HEAD = '4dab80ae4564ef8d6e1030564dcea4ba19235ee6'
TREE = 'bcca74ee4dd8c8a4a45b26e0b7accda5131f9ce1'
REQUIRED = ['protocol-processor', 'gptp-processor', 'third_party/verilog-axis']
ENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1', GIT_OPTIONAL_LOCKS='0')

def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], env=ENV)

def check(root, revision, label):
    assert git(root, 'rev-parse', 'HEAD').decode().strip() == revision
    expected = {}
    for record in git(root, 'ls-tree', '-rz', revision).split(b'\0'):
        if not record:
            continue
        meta, name = record.split(b'\t', 1)
        mode, kind, oid = meta.split()
        expected[name] = (mode, oid)
        if kind == b'commit':
            continue
        path = root / os.fsdecode(name)
        for parent in path.parents:
            if parent == root:
                break
            assert not parent.is_symlink(), f'{label}: symlink ancestor {name!r}'
        info = path.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(info.st_mode)
            content = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(info.st_mode), f'{label}: wrong kind {name!r}'
            actual_mode = b'100755' if info.st_mode & 0o111 else b'100644'
            assert actual_mode == mode, f'{label}: mode mismatch {name!r}'
            content = path.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(content)).encode() + b'\0' + content).hexdigest().encode()
        assert actual == oid, f'{label}: blob mismatch {name!r}'
    index = {}
    for record in git(root, 'ls-files', '--stage', '-z').split(b'\0'):
        if not record:
            continue
        meta, name = record.split(b'\t', 1)
        mode, oid, stage = meta.split()
        assert stage == b'0' and name not in index
        index[name] = (mode, oid)
    assert index == expected, f'{label}: index differs from commit'
    assert not git(root, 'status', '--porcelain', '--untracked-files=all'), f'{label}: worktree is not clean'
    print(f'PASS {label}: {revision}; {len(expected)} tracked entries; raw bytes, kinds, modes and index match')
    print(f'index-flags-sha256 {label}: ' + hashlib.sha256(git(root, 'ls-files', '-v', '-z')).hexdigest())
    return expected

root = Path(sys.argv[1]).resolve()
assert git(root, 'rev-parse', 'HEAD^{tree}').decode().strip() == TREE
assert subprocess.run(['git', '-C', str(root), 'symbolic-ref', '-q', 'HEAD'], stdout=subprocess.DEVNULL).returncode == 1
entries = check(root, HEAD, 'root')
for name in REQUIRED:
    sub = root / name
    assert not sub.is_symlink() and (sub / '.git').is_file()
    assert Path(git(sub, 'rev-parse', '--show-toplevel').decode().strip()).resolve() == sub
    assert Path(git(sub, 'rev-parse', '--show-superproject-working-tree').decode().strip()).resolve() == root
    mode, oid = entries[name.encode()]
    assert mode == b'160000'
    check(sub, oid.decode(), name)
print(f'PASS exact tree {TREE}; external gitlink checked in root index, optional external checkout not required')
