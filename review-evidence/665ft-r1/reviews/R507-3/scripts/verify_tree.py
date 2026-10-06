#!/usr/bin/env python3
"""Verify raw tracked bytes, modes and index entries without trusting stat caches."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
env = {**os.environ, 'GIT_NO_REPLACE_OBJECTS': '1'}
HEAD = '6ca834a782a1bd5574d44998c8e214cf16df3441'
TREE = '79a9a6b116e9b839e744af76960a10588381a1bb'
PINS = {
    'protocol-processor': 'ead8036035affd53ef4b29979190f2f4f67084c0',
    'gptp-processor': '5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d',
    'third_party/verilog-axis': '48ff7a7e2ef782cf778d47910cf85835c64b1bce',
}

def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args], env=env)

def verify(repo, pin):
    assert git(repo, 'rev-parse', 'HEAD').decode().strip() == pin
    tree = {}
    for entry in git(repo, 'ls-tree', '-r', '-z', pin).split(b'\0'):
        if not entry:
            continue
        meta, name = entry.split(b'\t', 1)
        mode, kind, oid = meta.split()
        tree[name] = mode, kind, oid
    index = {}
    for entry in git(repo, 'ls-files', '--stage', '-z').split(b'\0'):
        if not entry:
            continue
        meta, name = entry.split(b'\t', 1)
        mode, oid, stage = meta.split()
        assert stage == b'0' and name not in index, ('unmerged/duplicate', name)
        index[name] = mode, oid
    assert index == {name: (mode, oid) for name, (mode, _, oid) in tree.items()}, 'index differs'
    count = 0
    digest = hashlib.sha256()
    for name, (mode, kind, oid) in sorted(tree.items()):
        if kind == b'commit':
            continue
        p = repo / os.fsdecode(name)
        st = p.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(st.st_mode), name
            data = os.fsencode(os.readlink(p))
        else:
            assert stat.S_ISREG(st.st_mode), name
            actual_mode = b'100755' if st.st_mode & 0o111 else b'100644'
            assert mode == actual_mode, ('mode', name)
            data = p.read_bytes()
        actual_oid = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest().encode()
        assert actual_oid == oid, ('bytes', name)
        digest.update(mode + b' ' + oid + b'\t' + name + b'\0')
        count += 1
    return {'head': pin, 'tracked_blobs_verified': count, 'index_entries_verified': len(index),
            'mode_and_blob_inventory_sha256': digest.hexdigest(), 'mismatches': 0}

assert git(root, 'rev-parse', 'HEAD^{tree}').decode().strip() == TREE
assert subprocess.run(['git', '-C', str(root), 'symbolic-ref', '-q', 'HEAD'],
                      env=env, capture_output=True).returncode == 1, 'checkout is not detached'
result = {'superproject': verify(root, HEAD), 'tree': TREE, 'required_submodules': {}}
for path, pin in PINS.items():
    actual = git(root, 'ls-tree', HEAD, '--', path).decode().split()
    assert actual[:3] == ['160000', 'commit', pin]
    sub = root / path
    assert not sub.is_symlink() and (sub / '.git').is_file()
    assert Path(git(sub, 'rev-parse', '--show-superproject-working-tree').decode().strip()) == root
    result['required_submodules'][path] = verify(sub, pin)
print(json.dumps(result, indent=2))
