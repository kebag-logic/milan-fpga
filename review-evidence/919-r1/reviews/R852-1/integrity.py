#!/usr/bin/env python3
"""Verify tracked bytes, executable/symlink modes, index and required gitlinks without editing source."""
import hashlib
import os
from pathlib import Path
import stat
import subprocess

HEAD = 'afa3ea19d6a1075382c63e4fc1e188a9aadf33bb'
TREE = '406dc4ba57ae0b7e1f06f5e400356872cabc32af'
root = Path.cwd()

def git(path, *args):
    return subprocess.check_output(['git', '-C', str(path), *args])

def verify(path, expected):
    assert git(path, 'rev-parse', 'HEAD').decode().strip() == expected
    tree = git(path, 'rev-parse', 'HEAD^{tree}').decode().strip()
    if path == root:
        assert tree == TREE
    assert git(path, 'write-tree').decode().strip() == tree, f'index differs: {path}'
    entries = git(path, 'ls-tree', '-rz', '--full-tree', 'HEAD').split(b'\0')
    count = 0
    links = []
    for entry in entries:
        if not entry:
            continue
        desc, name = entry.split(b'\t', 1)
        mode, kind, oid = desc.decode().split()
        relative = os.fsdecode(name)
        p = path / relative
        if kind == 'commit':
            links.append((p, oid))
            continue
        st = p.lstat()
        if mode == '120000':
            assert stat.S_ISLNK(st.st_mode), p
            data = os.fsencode(os.readlink(p))
        else:
            assert stat.S_ISREG(st.st_mode), p
            assert bool(st.st_mode & 0o111) == (mode == '100755'), p
            data = p.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert actual == oid, f'blob differs: {p}'
        count += 1
    print(f'PASS {path.relative_to(root) or "."}: head={expected} tree={tree}; {count} tracked blobs/modes; index identical')
    for p, oid in links:
        if (p / '.git').exists():
            print('gitlink', p.relative_to(root), oid)
            verify(p, oid)
        else:
            assert p == root / 'external', f'required submodule absent: {p}'
            print('UNINITIALIZED legacy external gitlink retained:', oid)

verify(root, HEAD)
print('Root status (including untracked files):')
print(git(root, 'status', '--porcelain=v1', '--untracked-files=all').decode() or 'clean')
print('PASS exact tracked-byte/mode/index/gitlink integrity')
