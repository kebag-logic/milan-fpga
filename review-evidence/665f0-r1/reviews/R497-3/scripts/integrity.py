#!/usr/bin/env python3
"""Verify raw tracked bytes, modes and index against a specified commit."""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys

HEAD = '3ebd6ca30106a006c20fd2879dcad9c79bf51dca'
TREE = '58f02a8d2be6f1d5605db8df5aeab173a9ea76f1'
REQUIRED = ('protocol-processor', 'gptp-processor', 'third_party/verilog-axis')

def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], env={**os.environ, 'GIT_NO_REPLACE_OBJECTS': '1'})

def verify(root, rev, label):
    entries = {}
    for record in git(root, 'ls-tree', '-rz', '--full-tree', rev).split(b'\0'):
        if not record:
            continue
        meta, name = record.split(b'\t', 1)
        mode, kind, oid = meta.split()
        entries[name] = (mode, oid)
        p = root / os.fsdecode(name)
        if kind == b'commit':
            continue
        st = p.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(st.st_mode), name
            data = os.fsencode(os.readlink(p))
        else:
            assert stat.S_ISREG(st.st_mode), name
            actual_mode = b'100755' if st.st_mode & 0o111 else b'100644'
            assert actual_mode == mode, name
            data = p.read_bytes()
        digest = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest().encode()
        assert digest == oid, name
    indexed = {}
    for record in git(root, 'ls-files', '--stage', '-z').split(b'\0'):
        if not record:
            continue
        meta, name = record.split(b'\t', 1)
        mode, oid, stage = meta.split()
        assert stage == b'0' and name not in indexed, name
        indexed[name] = (mode, oid)
    assert indexed == entries, 'Index differs from commit tree'
    print(f'PASS {label}: {len(entries)} tracked entries; raw bytes, kinds, modes and index match {rev}')
    return entries

root = Path(sys.argv[1]).resolve()
assert git(root, 'rev-parse', 'HEAD').decode().strip() == HEAD
assert git(root, 'rev-parse', 'HEAD^{tree}').decode().strip() == TREE
assert subprocess.run(['git', '-C', str(root), 'symbolic-ref', '-q', 'HEAD'], stdout=subprocess.DEVNULL).returncode == 1
entries = verify(root, HEAD, 'superproject')
for name in REQUIRED:
    sub = root / name
    mode, pin = entries[os.fsencode(name)]
    assert mode == b'160000' and (sub / '.git').is_file()
    assert git(sub, 'rev-parse', 'HEAD').strip() == pin
    assert git(sub, 'rev-parse', '--show-superproject-working-tree').decode().strip() == str(root)
    verify(sub, pin.decode(), name)
print(f'PASS exact detached head {HEAD}; tree {TREE}; all three required submodule gitlinks verified')
