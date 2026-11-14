#!/usr/bin/env python3
"""Compare tracked bytes, executable modes and index entries with exact Git trees."""
import hashlib
import os
import stat
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
expected = 'dd01b0afef87037ec485cd49b40a26b542854bdd'
required = ('protocol-processor', 'gptp-processor', 'third_party/verilog-axis',
            'third_party/tsn-c-stack', 'third_party/lwSRP')

def git(where, *args):
    return subprocess.check_output(['git', '-C', str(where), *args])

def verify(where, label):
    entries = git(where, 'ls-tree', '-rz', 'HEAD').split(b'\0')
    expected_index, links, total = {}, {}, 0
    for entry in filter(None, entries):
        meta, rawpath = entry.split(b'\t', 1)
        mode, kind, oid = meta.decode().split()
        path = os.fsdecode(rawpath)
        expected_index[path] = (mode, oid, '0')
        if kind == 'commit':
            links[path] = oid
            continue
        p = where / path
        s = p.lstat()
        if mode == '120000':
            assert stat.S_ISLNK(s.st_mode), (label, path, 'not a symlink')
            data = os.fsencode(os.readlink(p))
        else:
            assert stat.S_ISREG(s.st_mode), (label, path, 'not regular')
            assert bool(s.st_mode & 0o111) == (mode == '100755'), (label, path, 'mode')
            data = p.read_bytes()
        got = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert got == oid, (label, path, 'bytes')
        total += 1
    actual_index = {}
    for entry in filter(None, git(where, 'ls-files', '--stage', '-z').split(b'\0')):
        meta, path = entry.split(b'\t', 1)
        mode, oid, stage = meta.decode().split()
        actual_index[os.fsdecode(path)] = mode, oid, stage
    assert actual_index == expected_index, (label, 'index differs')
    dirty = git(where, 'status', '--porcelain', '--untracked-files=all').decode()
    assert not dirty, (label, dirty)
    ignored = git(where, 'ls-files', '--others', '--ignored', '--exclude-standard').decode()
    assert not ignored, (label, 'ignored files', ignored)
    print(f'{label}: {total} tracked blobs and modes match HEAD; index matches; no untracked or ignored files')
    return links

assert git(root, 'rev-parse', 'HEAD').decode().strip() == expected
tree = git(root, 'rev-parse', 'HEAD^{tree}').decode().strip()
assert tree == '4d7787fe81c9a90177d98e1afff98f216cb3b140'
print('HEAD', expected, 'TREE', tree)
links = verify(root, 'superproject')
for path in required:
    sub = root / path
    assert (sub/'.git').is_file(), (path, 'missing genuine submodule gitfile')
    assert git(sub, 'rev-parse', 'HEAD').decode().strip() == links[path]
    print('gitlink', path, links[path])
    verify(sub, path)
print('external: intentionally uninitialized; recorded gitlink', links['external'])
print('RESULT: PASS')
