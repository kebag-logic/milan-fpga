#!/usr/bin/env python3
"""Prove tracked bytes, modes, index entries and required submodule pins."""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')
head = '166dfdc9fd2f22a9d2acd272bac4d1a5e3462f3e'
required = ['protocol-processor', 'gptp-processor', 'third_party/verilog-axis', 'third_party/tsn-c-stack']

def git(where, *args):
    return subprocess.check_output(['git', '-C', str(where), *args], env=env)

def verify(where, commit):
    assert git(where, 'rev-parse', 'HEAD').decode().strip() == commit
    index = {}
    for row in git(where, 'ls-files', '--stage', '-z').split(b'\0'):
        if not row: continue
        data, name = row.split(b'\t', 1)
        mode, oid, stage = data.decode().split()
        assert stage == '0'
        index[name] = (mode, oid)
    entries = {}
    count = 0
    for row in git(where, 'ls-tree', '-rz', commit).split(b'\0'):
        if not row: continue
        data, name = row.split(b'\t', 1)
        mode, kind, oid = data.decode().split()
        entries[name] = (mode, oid)
        if kind != 'blob': continue
        path = where / os.fsdecode(name)
        st = path.lstat()
        if mode == '120000':
            assert stat.S_ISLNK(st.st_mode), path
            content = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode), path
            actual_mode = '100755' if st.st_mode & 0o111 else '100644'
            assert actual_mode == mode, path
            content = path.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(content)).encode() + b'\0' + content).hexdigest()
        assert actual == oid, path
        count += 1
    assert index == entries, 'index differs from commit tree'
    print(('SUPERPROJECT' if where == root else str(where.relative_to(root))), commit,
          'tracked_blobs', count, 'bytes_modes_index=PASS')
    return entries

entries = verify(root, head)
assert git(root, 'rev-parse', 'HEAD^{tree}').decode().strip() == '08861f5484fad777532ecd5faa89af199e18a87a'
for name in required:
    mode, pin = entries[os.fsencode(name)]
    assert mode == '160000'
    path = root / name
    assert not path.is_symlink()
    assert (path / '.git').is_file(), 'required registered submodule missing'
    assert git(path, 'rev-parse', '--show-superproject-working-tree').decode().strip() == str(root)
    verify(path, pin)
print('INTEGRITY PASS: exact head, tree, tracked bytes, modes, index and four required gitlinks')
