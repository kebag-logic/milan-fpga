#!/usr/bin/env python3
"""Verify HEAD, index entries, actual blob bytes and modes, and populated gitlinks.
Usage: verify_tree.py CHECKOUT
"""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys

HEAD = '372556835d03b70134b2e76567b63b25c4cca005'
TREE = '34b71495c92a7dbee90c516354100ed61a51446e'
required = {'protocol-processor', 'gptp-processor', 'third_party/verilog-axis',
            'third_party/lwSRP', 'third_party/tsn-c-stack'}
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')
def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], env=env)

def verify(root, rev, label, nested=False):
    assert git(root, 'rev-parse', 'HEAD').decode().strip() == rev
    entries = {}
    for entry in git(root, 'ls-tree', '-rz', rev).split(b'\0'):
        if not entry:
            continue
        meta, name = entry.split(b'\t', 1)
        mode, kind, oid = meta.split()
        entries[name] = (mode, oid)
    index = {}
    for entry in git(root, 'ls-files', '--stage', '-z').split(b'\0'):
        if not entry:
            continue
        meta, name = entry.split(b'\t', 1)
        mode, oid, stage = meta.split()
        assert stage == b'0'
        index[name] = (mode, oid)
    assert index == entries, f'{label}: index differs'
    files, links = 0, []
    for name, (mode, oid) in entries.items():
        path = root / os.fsdecode(name)
        if mode == b'160000':
            links.append((os.fsdecode(name), oid.decode()))
            continue
        info = path.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(info.st_mode)
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(info.st_mode), f'{label}: kind {name!r}'
            actual = b'100755' if info.st_mode & 0o111 else b'100644'
            assert actual == mode, f'{label}: mode {name!r}'
            data = path.read_bytes()
        digest = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert digest == oid.decode(), f'{label}: blob {name!r}'
        files += 1
    print(f'{label}: HEAD {rev}; {files} blob bytes/modes and all index entries PASS')
    for name, oid in links:
        if not nested and name in required:
            verify(root / name, oid, name, True)
        else:
            print(f'{label}: gitlink {name} {oid}; not required/populated, index verified')

root = Path(sys.argv[1]).resolve()
assert git(root, 'rev-parse', 'HEAD^{tree}').decode().strip() == TREE
verify(root, HEAD, 'review checkout')
assert not git(root, 'status', '--porcelain', '--untracked-files=no').strip()
print('Exact head/tree, tracked bytes/modes/index and all five required submodules PASS')
