#!/usr/bin/env python3
"""Compare raw tracked bytes, modes, index entries and required submodule pins."""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
HEAD = 'c7d0ad63510cf1aaee41ef440675d110ad2730d7'
TREE = '06f494ec738a0c0eb0147a22b7b57c3545f5d6f9'
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')
def git(at, *args):
    return subprocess.check_output(['git', '-C', str(at), *args], env=env)
def verify(at, rev):
    entries = {}
    for row in git(at, 'ls-tree', '-rz', '--full-tree', rev).split(b'\0'):
        if not row: continue
        fields, name = row.split(b'\t', 1)
        mode, kind, oid = fields.split()
        entries[name] = (mode, oid)
        if kind == b'commit': continue
        path = os.fsencode(at) + b'/' + name
        info = os.lstat(path)
        if mode == b'120000':
            assert stat.S_ISLNK(info.st_mode), name
            data = os.readlink(path)
        else:
            assert stat.S_ISREG(info.st_mode), name
            actual_mode = b'100755' if info.st_mode & 0o111 else b'100644'
            assert actual_mode == mode, name
            with open(path, 'rb') as f: data = f.read()
        actual_oid = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest().encode()
        assert actual_oid == oid, name
    indexed = {}
    for row in git(at, 'ls-files', '--stage', '-z').split(b'\0'):
        if not row: continue
        fields, name = row.split(b'\t', 1)
        mode, oid, stage = fields.split()
        assert stage == b'0' and name not in indexed, name
        indexed[name] = (mode, oid)
    assert entries == indexed, 'index differs from commit tree'
    return len(entries), entries

assert git(root, 'rev-parse', 'HEAD').decode().strip() == HEAD
assert git(root, 'rev-parse', 'HEAD^{tree}').decode().strip() == TREE
detached = subprocess.run(['git', '-C', str(root), 'symbolic-ref', '-q', 'HEAD'], capture_output=True)
assert detached.returncode == 1
count, entries = verify(root, HEAD)
print('HEAD', HEAD, 'TREE', TREE, 'detached')
print('Parent: raw blob bytes, modes and complete index MATCH;', count, 'entries')
for sub in ('protocol-processor', 'gptp-processor', 'third_party/verilog-axis'):
    mode, pin = entries[sub.encode()]
    assert mode == b'160000'
    at = root / sub
    assert (at / '.git').is_file() and not at.is_symlink()
    assert git(at, 'rev-parse', 'HEAD').strip() == pin
    superproject = git(at, 'rev-parse', '--show-superproject-working-tree').decode().strip()
    assert Path(superproject).resolve() == root
    total, _ = verify(at, pin.decode())
    print(sub, pin.decode(), 'raw blob bytes, modes and complete index MATCH;', total, 'entries')
print('PASS')
