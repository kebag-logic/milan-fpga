#!/usr/bin/env python3
"""Check tracked bytes, kinds, executable modes, index and required gitlinks.
Usage: python3 -B verify_tree.py CHECKOUT
"""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
head = 'd1aa4c44307edf4a9390c19cbb2c82fe5c5464d0'
tree = 'e8705c7ca87bb1d0f49be28e78bc54b93192ec1f'
def git(where, *args):
    return subprocess.check_output(['git', '-C', str(where), *args])
assert git(root, 'rev-parse', 'HEAD').decode().strip() == head
assert git(root, 'rev-parse', 'HEAD^{tree}').decode().strip() == tree
def check(where):
    expected = {}
    links = {}
    for entry in git(where, 'ls-tree', '-rz', 'HEAD').split(b'\0'):
        if not entry:
            continue
        fields, rawpath = entry.split(b'\t', 1)
        mode, kind, oid = fields.decode().split()
        path = os.fsdecode(rawpath)
        expected[path] = (mode, oid, '0')
        if kind == 'commit':
            links[path] = oid
            continue
        p = where / path
        info = p.lstat()
        if mode == '120000':
            assert stat.S_ISLNK(info.st_mode), path
            data = os.fsencode(os.readlink(p))
        else:
            assert stat.S_ISREG(info.st_mode), path
            assert bool(info.st_mode & 0o111) == (mode == '100755'), path
            data = p.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert actual == oid, path
    index = {}
    for entry in git(where, 'ls-files', '--stage', '-z').split(b'\0'):
        if entry:
            fields, rawpath = entry.split(b'\t', 1)
            index[os.fsdecode(rawpath)] = tuple(fields.decode().split())
    assert index == expected, 'index differs from HEAD'
    print(f'PASS {where.name}: {len(expected)} tracked entries; blob bytes, kinds, modes and index match HEAD')
    return links
links = check(root)
required = ('gptp-processor', 'protocol-processor', 'third_party/lwSRP',
            'third_party/tsn-c-stack', 'third_party/verilog-axis')
for name in required:
    child = root / name
    actual = git(child, 'rev-parse', 'HEAD').decode().strip()
    assert actual == links[name], name
    print(f'gitlink {name} {actual}')
    check(child)
print(f'external gitlink {links["external"]}; uninitialized as supplied, not required for these probes')
print(f'PASS exact head {head}, tree {tree}')
