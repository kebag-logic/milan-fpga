#!/usr/bin/env python3
"""Verify raw tracked bytes, file kinds/modes, index and required gitlinks.
Run: python3 -B verify_tree.py CHECKOUT
"""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')
def git(where, *args):
    return subprocess.check_output(['git', '-C', str(where), *args], env=env)

head = '7cfb8a0499941e56682f0c2f63326d120f5b7d9e'
expected_tree = 'eb5a313b02b3669d9529500c0369c62dca697b50'
assert git(root, 'rev-parse', 'HEAD').decode().strip() == head
assert git(root, 'rev-parse', 'HEAD^{tree}').decode().strip() == expected_tree
required = ['protocol-processor', 'gptp-processor', 'third_party/lwSRP',
            'third_party/tsn-c-stack', 'third_party/verilog-axis']
results = []

def verify(where, commit, label):
    tree = {}
    for record in git(where, 'ls-tree', '-rz', '--full-tree', commit).split(b'\0'):
        if not record:
            continue
        metadata, path = record.split(b'\t', 1)
        mode, kind, oid = metadata.split()
        tree[path] = (mode, oid)
        if kind == b'commit':
            continue
        file = where / os.fsdecode(path)
        st = file.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(st.st_mode), (label, path, 'kind')
            data = os.fsencode(os.readlink(file))
        else:
            assert stat.S_ISREG(st.st_mode), (label, path, 'kind')
            actual_mode = b'100755' if st.st_mode & 0o111 else b'100644'
            assert actual_mode == mode, (label, path, 'mode')
            data = file.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest().encode()
        assert actual == oid, (label, path, 'blob')
    index = {}
    for record in git(where, 'ls-files', '--stage', '-z').split(b'\0'):
        if not record:
            continue
        metadata, path = record.split(b'\t', 1)
        mode, oid, stage = metadata.split()
        assert stage == b'0' and path not in index, (label, path, 'index-stage')
        index[path] = (mode, oid)
    assert tree == index, (label, 'index differs from commit')
    results.append(dict(repository=label, commit=commit, entries=len(tree),
                        raw_blobs_modes_index='PASS'))
    return tree

tree = verify(root, head, '.')
for name in required:
    mode, oid = tree[name.encode()]
    assert mode == b'160000'
    sub = root / name
    assert (sub / '.git').is_file() and not sub.is_symlink(), (name, 'not registered checkout')
    assert git(sub, 'rev-parse', 'HEAD').strip() == oid, (name, 'head')
    verify(sub, oid.decode(), name)
print(json.dumps(dict(head=head, tree=expected_tree, results=results,
                     excluded_uninitialized_gitlink='external (not required by these checks)',
                     status='PASS'), indent=2))
