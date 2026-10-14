#!/usr/bin/env python3
"""Verify raw tracked blob bytes, modes, stage-zero index and gitlinks."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--repo', type=Path, required=True)
args = parser.parse_args()
repo = args.repo.resolve()

def git(root, *argv):
    return subprocess.check_output(['git', '--no-replace-objects', '-C', str(root), *argv])

def verify(root, expected):
    assert git(root, 'rev-parse', 'HEAD').decode().strip() == expected
    tree = {}
    for record in git(root, 'ls-tree', '-rz', expected).split(b'\0'):
        if not record:
            continue
        meta, name = record.split(b'\t', 1)
        mode, kind, oid = meta.split()
        tree[name] = (mode, oid)
    index = {}
    for record in git(root, 'ls-files', '--stage', '-z').split(b'\0'):
        if not record:
            continue
        meta, name = record.split(b'\t', 1)
        mode, oid, stage = meta.split()
        assert stage == b'0' and name not in index
        index[name] = (mode, oid)
    assert index == tree, 'index differs from committed tree'
    checked = 0
    pins = {}
    for name, (mode, expected_oid) in tree.items():
        path = root / os.fsdecode(name)
        if mode == b'160000':
            pins[os.fsdecode(name)] = expected_oid.decode()
            continue
        info = path.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(info.st_mode)
            content = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(info.st_mode)
            assert bool(info.st_mode & stat.S_IXUSR) == (mode == b'100755')
            content = path.read_bytes()
        oid = hashlib.sha1(b'blob ' + str(len(content)).encode() + b'\0' + content).hexdigest()
        assert oid == expected_oid.decode(), str(path)
        checked += 1
    encoded = b''.join(name + b'\0' + mode + b' ' + oid + b'\n'
                       for name, (mode, oid) in sorted(tree.items()))
    label = '.' if root == repo else str(root.relative_to(repo))
    print(json.dumps({'path': label, 'head': expected,
        'tree': git(root, 'rev-parse', expected + '^{tree}').decode().strip(),
        'verified_blobs_and_modes': checked, 'index': 'exact stage zero tree',
        'inventory_sha256': hashlib.sha256(encoded).hexdigest(), 'gitlinks': pins}, sort_keys=True))
    return pins

head = '412e3f6c8c402bce63e94c291d2782b5579aaa1d'
pins = verify(repo, head)
assert pins['gptp-processor'] == 'e4869fd0c42889b2ac806587cc5c78afb1c33461'
assert pins['protocol-processor'] == '2ad2f845dd583f8310075fa2380cb60a04fd091a'
assert pins['third_party/verilog-axis'] == '48ff7a7e2ef782cf778d47910cf85835c64b1bce'
assert pins['third_party/lwSRP'] == '08ee86e812a0eb5e1dc6cd61b494d8baf3491348'
assert pins['third_party/tsn-c-stack'] == '70936b77dc41981e192438388cd0aced69954f18'
for name, pin in sorted(pins.items()):
    if name == 'external':
        print('external: gitlink verified; uninitialized and outside executed inputs')
        continue
    verify(repo / name, pin)
print('IDENTITY PASS: every initialized tracked file, mode and index matches its reviewed commit')
