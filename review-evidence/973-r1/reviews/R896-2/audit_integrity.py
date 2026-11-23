#!/usr/bin/env python3
"""Prove raw tracked bytes, kinds, modes, index entries and initialized gitlinks."""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
expected = '5759780f2251ef25221c6a395250312dce656ca4'
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')

def git(where, *args):
    return subprocess.check_output(['git', '-C', str(where), *args], env=env)

assert git(root, 'rev-parse', 'HEAD').decode().strip() == expected
assert git(root, 'rev-parse', 'HEAD^{tree}').decode().strip() == '68f513cdd17297261b34f7601b0f95e8185f5c84'

def audit(where, revision, label):
    tree = {}
    links = []
    for rec in git(where, 'ls-tree', '-rz', revision).split(b'\0'):
        if not rec:
            continue
        header, name = rec.split(b'\t', 1)
        mode, kind, oid = header.split()
        tree[name] = (mode, oid, b'0')
        path = where / os.fsdecode(name)
        if mode == b'160000':
            links.append((name, oid.decode()))
            continue
        st = path.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(st.st_mode), (label, name, 'not symlink')
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode), (label, name, 'not regular')
            assert bool(st.st_mode & 0o111) == (mode == b'100755'), (label, name, 'mode')
            data = path.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest().encode()
        assert actual == oid, (label, name, 'blob')
    index = {}
    for rec in git(where, 'ls-files', '--stage', '-z').split(b'\0'):
        if not rec:
            continue
        fields, name = rec.split(b'\t', 1)
        mode, oid, stage = fields.split()
        assert name not in index, (label, name, 'multiple stages')
        index[name] = (mode, oid, stage)
    assert tree == index, (label, 'index differs')
    print(f'PASS {label}: {len(tree)} tracked entries; raw blob bytes/kinds/modes and index equal {revision}')
    return links

links = audit(root, expected, 'superproject')
required = {'protocol-processor', 'gptp-processor', 'third_party/verilog-axis',
            'third_party/tsn-c-stack', 'third_party/lwSRP'}
for name, oid in links:
    name = os.fsdecode(name)
    if name not in required:
        print(f'UNCHANGED gitlink {name}: {oid}; uninitialized, outside required population')
        continue
    path = root / name
    assert not path.is_symlink()
    assert (path / '.git').is_file(), (name, 'not registered submodule')
    assert git(path, 'rev-parse', 'HEAD').decode().strip() == oid
    audit(path, oid, name)
    required.remove(name)
assert not required
assert not git(root, 'status', '--porcelain', '--untracked-files=no').strip()
print('PASS exact head/tree and all five required submodule gitlinks; no tracked source restoration needed')
