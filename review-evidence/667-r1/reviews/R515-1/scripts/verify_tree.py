#!/usr/bin/env python3
"""Verify exact tracked bytes, kinds, executable modes, index and gitlinks."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

repo = Path(sys.argv[1]).resolve()
head = '41bc9dac031526c1fd637ff1e801d3c6dc1260b4'
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')
required = ['third_party/verilog-axis', 'protocol-processor', 'gptp-processor']


def git(where, *args):
    return subprocess.check_output(['git', '-C', str(where), *args], env=env)


def verify(where, oid):
    assert git(where, 'rev-parse', 'HEAD').decode().strip() == oid
    entries = {}
    for row in git(where, 'ls-tree', '-rz', oid).split(b'\0'):
        if not row:
            continue
        info, path = row.split(b'\t', 1)
        mode, kind, blob = info.decode().split()
        entries[os.fsdecode(path)] = (mode, kind, blob)
    indexed = {}
    for row in git(where, 'ls-files', '--stage', '-z').split(b'\0'):
        if not row:
            continue
        info, path = row.split(b'\t', 1)
        mode, blob, stage = info.decode().split()
        assert stage == '0', ('unmerged index', path)
        indexed[os.fsdecode(path)] = (mode, blob)
    assert indexed == {p: (m, b) for p, (m, k, b) in entries.items()}, 'index mismatch'
    checked = 0
    for p, (mode, kind, blob) in entries.items():
        if kind == 'commit':
            continue
        path = where / p
        st = path.lstat()
        if mode == '120000':
            assert stat.S_ISLNK(st.st_mode), p
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode), p
            assert bool(st.st_mode & 0o111) == (mode == '100755'), p
            data = path.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert actual == blob, p
        checked += 1
    return entries, checked


entries, count = verify(repo, head)
result = {'head': head, 'tree': git(repo, 'rev-parse', 'HEAD^{tree}').decode().strip(),
          'tracked_blobs_verified': count, 'index': 'exact tree entries, stage zero',
          'bytes_modes_kinds': 'PASS', 'submodules': {}}
assert result['tree'] == '1a233401c2f5d585b7a0a2d1a7db16daff6d29b6'
for name in required:
    mode, kind, pin = entries[name]
    assert (mode, kind) == ('160000', 'commit')
    path = repo / name
    assert not path.is_symlink() and (path / '.git').is_file()
    assert Path(git(path, 'rev-parse', '--show-superproject-working-tree').decode().strip()) == repo
    _, checked = verify(path, pin)
    result['submodules'][name] = {'pin': pin, 'verified_blobs': checked, 'result': 'PASS'}
result['external'] = 'gitlink verified in index; uninitialized, not a required input'
result['status'] = git(repo, 'status', '--porcelain=v1', '--untracked-files=all').decode()
assert result['status'] == ''
print(json.dumps(result, indent=2))
