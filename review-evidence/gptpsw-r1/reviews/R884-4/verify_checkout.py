#!/usr/bin/env python3
"""Verify tracked disk bytes, types, modes, index, and initialized required gitlinks."""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
os.environ['GIT_NO_REPLACE_OBJECTS'] = '1'
def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args])
def verify(repo, revision, label):
    assert git(repo, 'rev-parse', 'HEAD').decode().strip() == revision
    tree = {}
    links = {}
    for record in git(repo, 'ls-tree', '-rz', revision).split(b'\0'):
        if not record:
            continue
        meta, path = record.split(b'\t', 1)
        mode, kind, oid = meta.split()
        tree[path] = (mode, oid)
        p = repo / os.fsdecode(path)
        if kind == b'commit':
            links[os.fsdecode(path)] = oid.decode()
            continue
        info = p.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(info.st_mode), path
            data = os.fsencode(os.readlink(p))
        else:
            assert stat.S_ISREG(info.st_mode), path
            executable = bool(info.st_mode & 0o111)
            assert executable == (mode == b'100755'), path
            data = p.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert actual == oid.decode(), path
    index = {}
    for record in git(repo, 'ls-files', '--stage', '-z').split(b'\0'):
        if not record:
            continue
        meta, path = record.split(b'\t', 1)
        mode, oid, stage = meta.split()
        assert stage == b'0' and path not in index
        index[path] = mode, oid
    assert index == tree, label
    print('PASS', label, revision, 'tracked blobs/modes/index:', len(tree), 'gitlinks:', len(links))
    return links
links = verify(root, '165476c755e4728a044c12ea6bc33ce0a0a9d28f', 'superproject')
for path in ['protocol-processor', 'gptp-processor', 'third_party/verilog-axis', 'third_party/tsn-c-stack', 'third_party/lwSRP']:
    sub = root / path
    assert not sub.is_symlink() and (sub / '.git').is_file(), path
    assert Path(git(sub, 'rev-parse', '--show-superproject-working-tree').decode().strip()).resolve() == root
    verify(sub, links[path], path)
print('External non-required gitlink remains uninitialized; no hardware or external checkout used.')
print('PASS exact-head tracked bytes, modes, index and required submodule gitlinks')
