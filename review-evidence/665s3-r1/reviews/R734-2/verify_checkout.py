#!/usr/bin/env python3
"""Prove tracked bytes, modes, index entries and initialized dependency pins."""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
expected = 'ac105b158bb740a65e0154305377fd4a7d0f6f87'
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')
def git(where, *args):
    return subprocess.check_output(['git', '-C', str(where), *args], env=env)
def verify(where, revision):
    assert git(where, 'rev-parse', 'HEAD').decode().strip() == revision
    tree = git(where, 'ls-tree', '-r', '-z', revision)
    entries = []
    blobs = 0
    for row in tree.split(b'\0'):
        if not row:
            continue
        metadata, name = row.split(b'\t', 1)
        mode, kind, oid = metadata.split()
        entries.append(mode + b' ' + oid + b' 0\t' + name)
        if kind == b'commit':
            continue
        path = where / os.fsdecode(name)
        info = path.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(info.st_mode), name
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(info.st_mode), name
            assert bool(info.st_mode & 0o111) == (mode == b'100755'), name
            data = path.read_bytes()
        digest = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest().encode()
        assert digest == oid, name
        blobs += 1
    index = git(where, 'ls-files', '--stage', '-z').split(b'\0')
    assert sorted(entries) == sorted(x for x in index if x), 'index differs from pinned tree'
    print(f'{where.name}: {revision}; {blobs} tracked blobs/modes and index verified')
    return tree

tree = verify(root, expected)
assert git(root, 'rev-parse', 'HEAD^{tree}').decode().strip() == '10a286051e8aa59003bfac98cf4f7d5973d241f9'
required = {'protocol-processor', 'gptp-processor', 'third_party/lwSRP',
            'third_party/tsn-c-stack', 'third_party/verilog-axis'}
for row in tree.split(b'\0'):
    if not row:
        continue
    metadata, name = row.split(b'\t', 1)
    mode, kind, oid = metadata.split()
    if os.fsdecode(name) in required:
        assert kind == b'commit' and mode == b'160000'
        verify(root/os.fsdecode(name), oid.decode())
        assert (root/os.fsdecode(name)/'.git').is_file(), 'dependency must be an initialized submodule'
print('PASS: exact head, tree, bytes, modes, index and five required gitlinks')
