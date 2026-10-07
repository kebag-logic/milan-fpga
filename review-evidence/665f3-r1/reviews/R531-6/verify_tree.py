#!/usr/bin/env python3
"""Prove tracked worktree bytes, modes, index, and required gitlinks."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

ROOT = Path(sys.argv[1]).resolve()
HEAD = 'd8060d87f892239ac4e598d0a8556cbfcd4a52ec'
TREE = '7db44a4a68c725ee0f4a74cd453eb82134c8bfcd'
REQUIRED = ('protocol-processor', 'gptp-processor', 'third_party/verilog-axis')
ENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')

def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], env=ENV)

def verify(root, revision):
    entries = git(root, 'ls-tree', '-rz', revision).split(b'\0')
    expected_index = []
    n = 0
    links = {}
    for entry in filter(None, entries):
        meta, name = entry.split(b'\t', 1)
        mode, kind, oid = meta.split()
        expected_index.append(mode + b' ' + oid + b' 0\t' + name)
        path = root / os.fsdecode(name)
        if kind == b'commit':
            links[os.fsdecode(name)] = oid.decode()
            continue
        st = path.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(st.st_mode), str(path)
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode), str(path)
            assert bool(st.st_mode & stat.S_IXUSR) == (mode == b'100755'), str(path)
            data = path.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert actual == oid.decode(), str(path)
        n += 1
    index = git(root, 'ls-files', '--stage', '-z').split(b'\0')
    assert sorted(filter(None, index)) == sorted(expected_index), 'index differs from tree'
    return n, links

assert git(ROOT, 'rev-parse', 'HEAD').decode().strip() == HEAD
assert git(ROOT, 'rev-parse', 'HEAD^{tree}').decode().strip() == TREE
n, links = verify(ROOT, HEAD)
report = {'head': HEAD, 'tree': TREE, 'tracked_blobs_verified': n, 'index': 'exact', 'submodules': {}}
for name in REQUIRED:
    path = ROOT / name
    assert not path.is_symlink()
    assert (path / '.git').is_file(), 'required registered submodule absent'
    assert Path(git(path, 'rev-parse', '--show-superproject-working-tree').decode().strip()).resolve() == ROOT
    assert git(path, 'rev-parse', 'HEAD').decode().strip() == links[name]
    count, _ = verify(path, links[name])
    report['submodules'][name] = {'gitlink': links[name], 'blobs_verified': count, 'index': 'exact'}
report['status'] = git(ROOT, 'status', '--porcelain=v1').decode()
report['result'] = 'PASS'
print(json.dumps(report, indent=2, sort_keys=True))
