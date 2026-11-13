#!/usr/bin/env python3
"""Verify tracked raw bytes, modes, index stages, and required submodule pins."""
import hashlib
import os
from pathlib import Path
import stat
import subprocess

os.environ['GIT_NO_REPLACE_OBJECTS'] = '1'
HEAD = '084cf7a8455e9fa8e24a0e5bcf57c9557816c819'
REQUIRED = ['protocol-processor', 'gptp-processor', 'third_party/lwSRP',
            'third_party/tsn-c-stack', 'third_party/verilog-axis']

def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args])

def check(root, rev):
    assert git(root, 'rev-parse', 'HEAD').decode().strip() == rev
    tree = {}
    for rec in git(root, 'ls-tree', '-rz', rev).split(b'\0'):
        if not rec:
            continue
        meta, name = rec.split(b'\t', 1)
        mode, kind, oid = meta.split()
        tree[name] = (mode, oid)
        if kind == b'commit':
            continue
        path = root / os.fsdecode(name)
        info = path.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(info.st_mode), name
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(info.st_mode), name
            assert bool(info.st_mode & 0o111) == (mode == b'100755'), name
            data = path.read_bytes()
        digest = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest().encode()
        assert digest == oid, name
    index = {}
    for rec in git(root, 'ls-files', '--stage', '-z').split(b'\0'):
        if not rec:
            continue
        meta, name = rec.split(b'\t', 1)
        mode, oid, stage = meta.split()
        assert stage == b'0' and name not in index, name
        index[name] = (mode, oid)
    assert index == tree, str(root)
    print('PASS', str(root), rev, 'tracked entries', len(tree), 'raw blobs/modes and stage-0 index equal tree')
    return tree

tree = check(Path('.'), HEAD)
for name in REQUIRED:
    mode, oid = tree[name.encode()]
    assert mode == b'160000'
    root = Path(name)
    assert not root.is_symlink()
    assert (root / '.git').is_file()
    assert git(root, 'rev-parse', '--show-superproject-working-tree').strip()
    check(root, oid.decode())
assert not git(Path('.'), 'status', '--porcelain=v1', '--untracked-files=all').strip()
print('PASS clean candidate; external submodule intentionally uninitialized and unused')
print('RESULT: PASS')
