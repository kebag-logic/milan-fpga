#!/usr/bin/env python3
"""Verify every tracked byte, mode, index entry and gitlink against the review head."""
import hashlib
import json
import os
from pathlib import Path
import subprocess as sp
import sys

repo = Path(sys.argv[1]).resolve()
head = '61a504eec3ec3de828ccd80076212533ef58644b'
base = '715589c1db7cf67e2f3259fd7083ebc7f0923376'
tree = '50c5014d5669bb8880b719445e6d737d22b9e285'
def git(*args):
    return sp.check_output(['git', *args], cwd=repo)
assert git('rev-parse', 'HEAD').decode().strip() == head
assert git('rev-parse', 'HEAD^{tree}').decode().strip() == tree
assert git('rev-parse', 'origin/main').decode().strip() == base
expected = {}
gitlinks = {}
for entry in git('ls-tree', '-rz', 'HEAD').split(b'\0'):
    if not entry:
        continue
    meta, path = entry.split(b'\t')
    mode, kind, oid = meta.decode().split()
    name = path.decode()
    expected[name] = (mode, oid, '0')
    p = repo / name
    if mode == '160000':
        actual = sp.check_output(['git', '-C', str(p), 'rev-parse', 'HEAD']).decode().strip()
        assert actual == oid, name
        gitlinks[name] = oid
        continue
    data = os.readlink(p).encode() if mode == '120000' else p.read_bytes()
    digest = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    assert digest == oid, ('blob mismatch', name)
    actual_mode = '120000' if p.is_symlink() else ('100755' if p.stat().st_mode & 0o111 else '100644')
    assert actual_mode == mode, ('mode mismatch', name)
index = {}
for entry in git('ls-files', '-sz').split(b'\0'):
    if entry:
        meta, path = entry.split(b'\t')
        index[path.decode()] = tuple(meta.decode().split())
assert index == expected, 'index differs'
assert not git('diff', 'origin/main', '--', 'src', 'include', 'examples', 'CMakeLists.txt', '.github'), 'production/build delta'
assert not git('status', '--porcelain'), 'worktree is not clean'
print(json.dumps({'head': head, 'tree': tree, 'origin_main': base, 'verified_tracked_files': len(expected), 'bytes_modes_index': 'PASS', 'gitlinks': gitlinks, 'production_headers_examples_build_ci_unchanged': True, 'status': 'clean'}, indent=2))
