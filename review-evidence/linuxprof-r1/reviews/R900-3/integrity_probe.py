#!/usr/bin/env python3
"""Prove raw tracked bytes, modes, index entries and required submodule pins."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
repo = Path(sys.argv[1]).resolve()
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')
head = '58f7673b8c57a80230e716bc1774ff9cc2f71ddc'
tree = '6dbb2ebaa80cf656a39b93c10c46e98fa6b92d2a'
def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], env=env)
def prove(root, rev):
    entries = {}
    blobs = links = 0
    for record in git(root, 'ls-tree', '-rz', '--full-tree', rev).split(b'\0'):
        if not record:
            continue
        meta, name = record.split(b'\t', 1)
        mode, kind, oid = meta.split()
        entries[name] = (mode, oid)
        if kind == b'commit':
            links += 1
            continue
        path = root / os.fsdecode(name)
        st = path.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(st.st_mode), name
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode), name
            assert bool(st.st_mode & 0o111) == (mode == b'100755'), name
            data = path.read_bytes()
        got = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest().encode()
        assert got == oid, name
        blobs += 1
    index = {}
    for record in git(root, 'ls-files', '--stage', '-z').split(b'\0'):
        if not record:
            continue
        meta, name = record.split(b'\t', 1)
        mode, oid, stage = meta.split()
        assert stage == b'0', name
        assert name not in index, name
        index[name] = (mode, oid)
    assert index == entries, 'index mismatch'
    flags = git(root, 'ls-files', '-v', '-z').split(b'\0')
    assert all(not r or (not r[:1].islower() and r[:1] != b'S') for r in flags)
    assert not git(root, 'status', '--porcelain=v1', '--untracked-files=all'), 'dirty status'
    return dict(revision=rev, tracked_blobs=blobs, gitlinks=links, raw_bytes='MATCH', modes='MATCH', index='MATCH', hidden_flags=0)
assert git(repo, 'rev-parse', 'HEAD').decode().strip() == head
assert git(repo, 'rev-parse', 'HEAD^{tree}').decode().strip() == tree
result = {'head': head, 'tree': tree, 'root': prove(repo, head), 'submodules': {}}
for name in ('protocol-processor', 'gptp-processor', 'third_party/verilog-axis', 'third_party/tsn-c-stack', 'third_party/lwSRP'):
    meta = git(repo, 'ls-tree', head, name).split(b'\t')[0].split()
    assert meta[:2] == [b'160000', b'commit']
    pin = meta[2].decode()
    sub = repo / name
    assert git(sub, 'rev-parse', 'HEAD').decode().strip() == pin
    assert git(sub, 'rev-parse', '--show-superproject-working-tree').decode().strip() == str(repo)
    result['submodules'][name] = prove(sub, pin)
result['unused_external'] = git(repo, 'submodule', 'status', 'external').decode().strip().split()[0]
print(json.dumps(result, indent=2))
