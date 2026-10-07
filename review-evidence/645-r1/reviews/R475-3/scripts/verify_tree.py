#!/usr/bin/env python3
"""Verify raw tracked blobs, executable modes, index entries and gitlinks."""
import hashlib
import os
from pathlib import Path
import stat
import subprocess

HEAD = '2525eae9567865a8bc741901914bdf5a1caf2c26'
TREE = 'a0545d5d4f4e098464fbd6a6a7a21fb4c735a423'
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')
def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], env=env)
def verify(root, rev, sub=False):
    records = git(root, 'ls-tree', '-rz', rev).split(b'\0')
    expected = {}
    count = 0
    links = []
    for record in records:
        if not record:
            continue
        meta, name = record.split(b'\t', 1)
        mode, kind, oid = meta.split()
        expected[name] = (mode, oid)
        p = root / os.fsdecode(name)
        if kind == b'commit':
            links.append((name, oid))
            continue
        st = p.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(st.st_mode), name
            data = os.fsencode(os.readlink(p))
        else:
            assert stat.S_ISREG(st.st_mode), name
            assert bool(st.st_mode & 0o111) == (mode == b'100755'), name
            data = p.read_bytes()
        digest = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest().encode()
        assert digest == oid, name
        count += 1
    actual = {}
    for entry in git(root, 'ls-files', '--stage', '-z').split(b'\0'):
        if not entry:
            continue
        meta, name = entry.split(b'\t', 1)
        mode, oid, stage = meta.split()
        assert stage == b'0', name
        actual[name] = (mode, oid)
    assert actual == expected, 'index mismatch'
    print(('submodule' if sub else 'source'), root.name, rev, 'blobs/modes/index PASS', count)
    for name, oid in links:
        print('gitlink', os.fsdecode(name), oid.decode())
    return links

root = Path.cwd()
assert git(root, 'rev-parse', 'HEAD').strip().decode() == HEAD
assert git(root, 'rev-parse', 'HEAD^{tree}').strip().decode() == TREE
links = verify(root, HEAD)
required = {b'third_party/verilog-axis', b'protocol-processor', b'gptp-processor'}
for name, oid in links:
    if name not in required:
        continue
    subroot = root / os.fsdecode(name)
    assert not subroot.is_symlink()
    assert (subroot / '.git').is_file()
    assert git(subroot, 'rev-parse', 'HEAD').strip() == oid
    assert Path(git(subroot, 'rev-parse', '--show-superproject-working-tree').decode().strip()).resolve() == root.resolve()
    verify(subroot, oid.decode(), sub=True)
print('PASS exact head/tree; tracked raw bytes, modes, index and all three required submodules')
