#!/usr/bin/env python3
"""Prove raw working bytes, file modes and index entries against the requested trees."""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
head = 'e7e0c10f4d4e9f3180b5650507a83aa300c5d4d7'
tree = '0ae619a8c3dd3efdf2cbc9bdbf45ed7221c4e20d'
required = ('protocol-processor', 'gptp-processor', 'third_party/verilog-axis')
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')

def git(where, *args):
    return subprocess.check_output(['git', '-C', str(where), *args], env=env)

def audit(where, rev, label):
    failures = []
    entries = git(where, 'ls-tree', '-rz', '--full-tree', rev).split(b'\0')
    want_index = {}
    count = 0
    links = {}
    for entry in entries:
        if not entry:
            continue
        fields, name = entry.split(b'\t', 1)
        mode, kind, oid = fields.split()
        want_index[name] = (mode, oid, b'0')
        if kind == b'commit':
            links[name.decode()] = oid.decode()
            continue
        p = where / os.fsdecode(name)
        try:
            s = p.lstat()
            if mode == b'120000':
                assert stat.S_ISLNK(s.st_mode)
                data = os.fsencode(os.readlink(p))
            else:
                assert stat.S_ISREG(s.st_mode)
                assert bool(s.st_mode & 0o111) == (mode == b'100755')
                data = p.read_bytes()
            digest = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
            assert digest == oid.decode()
            count += 1
        except (OSError, AssertionError):
            failures.append(os.fsdecode(name))
    actual = {}
    for row in git(where, 'ls-files', '--stage', '-z').split(b'\0'):
        if row:
            fields, name = row.split(b'\t', 1)
            actual[name] = tuple(fields.split())
    assert actual == want_index, f'{label}: index differs from tree'
    assert not failures, f'{label}: raw blob/mode mismatch: {failures}'
    assert git(where, 'rev-parse', 'HEAD').decode().strip() == rev
    print(f'{label}: {rev}, {count} raw blobs/modes and complete stage-0 index PASS')
    return links

assert git(root, 'rev-parse', 'HEAD^{tree}').decode().strip() == tree
links = audit(root, head, 'candidate')
for path in required:
    sub = root / path
    assert (sub / '.git').is_file(), f'{path}: not an initialized submodule'
    audit(sub, links[path], path)
print('required gitlinks PASS; external is not a required gate input')
print('candidate tree:', tree)
print('checkout audit PASS')
