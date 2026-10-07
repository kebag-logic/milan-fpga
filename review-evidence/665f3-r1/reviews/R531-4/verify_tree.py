#!/usr/bin/env python3
"""Verify raw tracked bytes, executable modes, index and required gitlinks.

Usage: python3 verify_tree.py REPOSITORY
"""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys

HEAD = '39adc58f8e63c7f41e12c79207a45bcc91a658d0'
TREE = '6e677bcdf9e401d538e362e6e1ef534cb084eb7d'
root = Path(sys.argv[1]).resolve()
env = {**os.environ, 'GIT_NO_REPLACE_OBJECTS': '1'}

def git(path, *args):
    return subprocess.check_output(['git', '-C', str(path), *args], env=env)

assert git(root, 'rev-parse', 'HEAD').decode().strip() == HEAD
assert git(root, 'rev-parse', 'HEAD^{tree}').decode().strip() == TREE

def verify(path, revision):
    expected = {}
    count = 0
    for row in git(path, 'ls-tree', '-rz', revision).split(b'\0'):
        if not row:
            continue
        meta, name = row.split(b'\t', 1)
        mode, kind, oid = meta.split()
        expected[name] = (mode, oid, b'0')
        if kind == b'commit':
            continue
        file = path / os.fsdecode(name)
        st = file.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(st.st_mode), name
            data = os.fsencode(os.readlink(file))
        else:
            assert stat.S_ISREG(st.st_mode), name
            actual_mode = b'100755' if st.st_mode & 0o111 else b'100644'
            assert actual_mode == mode, name
            data = file.read_bytes()
        digest = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest().encode()
        assert digest == oid, name
        count += 1
    actual = {}
    for row in git(path, 'ls-files', '--stage', '-z').split(b'\0'):
        if row:
            meta, name = row.split(b'\t', 1)
            assert name not in actual, name
            actual[name] = tuple(meta.split())
    assert actual == expected, 'index differs from pinned tree'
    print(f'PASS {path.name}: {count} raw blobs, modes and complete index equal {revision}')
    return expected

entries = verify(root, HEAD)
for name in ('protocol-processor', 'gptp-processor', 'third_party/verilog-axis'):
    mode, pin, stage = entries[name.encode()]
    assert (mode, stage) == (b'160000', b'0')
    sub = root / name
    assert (sub / '.git').is_file() and not sub.is_symlink(), name
    assert git(sub, 'rev-parse', 'HEAD').strip() == pin, name
    assert Path(git(sub, 'rev-parse', '--show-superproject-working-tree').decode().strip()).resolve() == root
    print(f'gitlink {name}: {pin.decode()}')
    verify(sub, pin.decode())
assert not git(root, 'status', '--porcelain', '--untracked-files=all').strip()
print('PASS exact HEAD/tree, raw tracked bytes/modes/index, required registered submodules, clean status')
