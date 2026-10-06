#!/usr/bin/env python3
"""Prove tracked bytes, modes, index entries and required submodule pins."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
head = '26bd6334a7b8b2a8582b36ae4729a71620546c14'
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')

def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args], env=env)

def verify(repo, revision):
    assert git(repo, 'rev-parse', 'HEAD').decode().strip() == revision
    tree = {}
    for entry in git(repo, 'ls-tree', '-rz', '--full-tree', revision).split(b'\0'):
        if not entry:
            continue
        meta, path = entry.split(b'\t', 1)
        mode, kind, oid = meta.split()
        tree[path] = (mode, oid)
    index = {}
    for entry in git(repo, 'ls-files', '--stage', '-z').split(b'\0'):
        if not entry:
            continue
        meta, path = entry.split(b'\t', 1)
        mode, oid, stage = meta.split()
        assert stage == b'0' and path not in index, ('index stage', path)
        index[path] = (mode, oid)
    assert index == tree, 'index differs from committed tree'
    count = 0
    for path, (mode, oid) in tree.items():
        if mode == b'160000':
            continue
        full = repo / os.fsdecode(path)
        st = full.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(st.st_mode), path
            data = os.fsencode(os.readlink(full))
        else:
            assert stat.S_ISREG(st.st_mode), path
            actual = b'100755' if st.st_mode & 0o111 else b'100644'
            assert actual == mode, ('mode', path)
            data = full.read_bytes()
        digest = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert digest.encode() == oid, ('blob', path)
        count += 1
    return tree, count

tree, count = verify(root, head)
print(json.dumps({'repository': 'candidate', 'head': head,
                  'tree': git(root, 'rev-parse', 'HEAD^{tree}').decode().strip(),
                  'verified_blobs': count, 'index': 'exact', 'bytes_modes': 'exact'}))
for name in ('third_party/verilog-axis', 'protocol-processor', 'gptp-processor'):
    mode, pin = tree[name.encode()]
    assert mode == b'160000'
    sub = root / name
    assert not sub.is_symlink() and (sub / '.git').is_file()
    assert Path(git(sub, 'rev-parse', '--show-superproject-working-tree').decode().strip()).resolve() == root
    _, count = verify(sub, pin.decode())
    print(json.dumps({'submodule': name, 'pin': pin.decode(), 'verified_blobs': count,
                      'index': 'exact', 'bytes_modes': 'exact'}))
print('PASS: candidate and all three required submodules match committed entries')
