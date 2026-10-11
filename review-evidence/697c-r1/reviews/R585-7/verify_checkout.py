#!/usr/bin/env python3
"""Verify canonical tracked bytes, executable/symlink modes, index, and required gitlinks."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

ap = argparse.ArgumentParser()
ap.add_argument('checkout', type=Path)
a = ap.parse_args()
root = a.checkout.resolve()
HEAD = '4cab445aa2475903b6cf8b87566d2c8a1e15e391'
TREE = '52c4164caae5e10e56f80313b5e556827da30d94'
pins = {
    'third_party/tsn-c-stack': '1a9f651cdf7846b8e10ac246a6ef6916960fbb92',
    'third_party/lwSRP': '9197193e47a6bb1c45a56d90a18c1784123aba44',
    'protocol-processor': '2ad2f845dd583f8310075fa2380cb60a04fd091a',
    'gptp-processor': '5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d',
    'third_party/verilog-axis': '48ff7a7e2ef782cf778d47910cf85835c64b1bce',
}
env = {**os.environ, 'GIT_NO_REPLACE_OBJECTS': '1'}

def git(where, *args):
    return subprocess.check_output(['git', '-C', str(where), *args], env=env)

def check(where, expected, label):
    assert git(where, 'rev-parse', 'HEAD').decode().strip() == expected
    assert not git(where, 'for-each-ref', '--format=%(refname)', 'refs/replace/')
    rows = {}
    for item in git(where, 'ls-tree', '-r', '-z', '--full-tree', expected).split(b'\0'):
        if not item:
            continue
        meta, name = item.split(b'\t', 1)
        mode, kind, oid = meta.decode().split()
        rows[os.fsdecode(name)] = (mode, kind, oid)
    index = {}
    for item in git(where, 'ls-files', '--stage', '-z').split(b'\0'):
        if not item:
            continue
        meta, name = item.split(b'\t', 1)
        mode, oid, stage = meta.decode().split()
        assert stage == '0'
        index[os.fsdecode(name)] = (mode, oid)
    assert index == {name: (mode, oid) for name, (mode, _, oid) in rows.items()}
    algorithm = git(where, 'rev-parse', '--show-object-format').decode().strip()
    blobs = 0
    for name, (mode, kind, oid) in rows.items():
        if kind == 'commit':
            continue
        path = where / name
        st = path.lstat()
        actual_mode = '120000' if stat.S_ISLNK(st.st_mode) else (
            '100755' if st.st_mode & stat.S_IXUSR else '100644')
        assert actual_mode == mode, (label, name, 'mode', actual_mode, mode)
        assert stat.S_ISREG(st.st_mode) or stat.S_ISLNK(st.st_mode)
        data = os.fsencode(os.readlink(path)) if path.is_symlink() else path.read_bytes()
        actual = hashlib.new(algorithm, b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert actual == oid, (label, name, 'blob mismatch')
        blobs += 1
    flags = [os.fsdecode(x) for x in git(where, 'ls-files', '-v', '-z').split(b'\0')
             if x and x[:1] != b'H']
    assert not flags, (label, 'index flags', flags)
    untracked = git(where, 'ls-files', '--others', '--exclude-standard', '-z')
    assert not untracked, (label, 'untracked', os.fsdecode(untracked))
    print(json.dumps({'checkout': label, 'head': expected, 'tracked_blobs_verified': blobs,
                      'gitlinks': sum(k == 'commit' for _, k, _ in rows.values()),
                      'bytes_modes_index': 'PASS', 'replace_refs': 0}))
    return rows

assert git(root, 'rev-parse', 'HEAD^{tree}').decode().strip() == TREE
rows = check(root, HEAD, 'review checkout')
for rel, pin in pins.items():
    assert rows[rel] == ('160000', 'commit', pin)
    check(root / rel, pin, rel)
print('exact head, tree, tracked bytes, modes, index and five required submodules: PASS')
