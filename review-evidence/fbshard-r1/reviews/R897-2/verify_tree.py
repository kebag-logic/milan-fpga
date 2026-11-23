#!/usr/bin/env python3
"""Verify tracked bytes, file kinds/modes, index, and initialized submodule pins."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')
head = '5392adf989349b68cfbb54d91fd0413c5b745521'
tree = '766ccefea747fa53f340cb99578f943b5279893c'
required = {'protocol-processor', 'gptp-processor', 'third_party/verilog-axis', 'third_party/tsn-c-stack', 'third_party/lwSRP'}
def git(where, *args):
    return subprocess.check_output(['git', '-C', str(where), *args], env=env)
def verify(where, revision):
    assert git(where, 'rev-parse', 'HEAD').decode().strip() == revision
    entries = {}
    for record in git(where, 'ls-tree', '-rz', revision).split(b'\0'):
        if record:
            meta, path = record.split(b'\t', 1)
            mode, kind, oid = meta.decode().split()
            entries[os.fsdecode(path)] = (mode, kind, oid)
    index = {}
    for record in git(where, 'ls-files', '--stage', '-z').split(b'\0'):
        if record:
            meta, path = record.split(b'\t', 1)
            mode, oid, stage = meta.decode().split()
            assert stage == '0'
            key = os.fsdecode(path)
            assert key not in index
            index[key] = (mode, oid)
    assert index == {p: (m, o) for p, (m, _, o) in entries.items()}, 'index differs from commit'
    count = 0
    links = {}
    for name, (mode, kind, oid) in entries.items():
        path = where / name
        if kind == 'commit':
            links[name] = oid
            continue
        info = path.lstat()
        if mode == '120000':
            assert stat.S_ISLNK(info.st_mode), name
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(info.st_mode), name
            assert bool(info.st_mode & 0o111) == (mode == '100755'), name
            data = path.read_bytes()
        digest = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert digest == oid, name
        count += 1
    return {'head': revision, 'tracked_blobs_verified': count, 'index_matches': True, 'gitlinks': links}
assert git(root, 'rev-parse', 'HEAD^{tree}').decode().strip() == tree
result = {'superproject': verify(root, head), 'submodules': {}, 'tree': tree}
for name, oid in result['superproject']['gitlinks'].items():
    if name not in required:
        result['submodules'][name] = {'pin': oid, 'initialized': (root / name / '.git').exists(), 'required': False}
        continue
    assert (root / name / '.git').is_file(), name
    assert git(root / name, 'rev-parse', '--show-superproject-working-tree').decode().strip() == str(root)
    result['submodules'][name] = verify(root / name, oid)
assert required <= result['submodules'].keys()
result['status_porcelain'] = git(root, 'status', '--porcelain=v1', '--untracked-files=all').decode()
assert not result['status_porcelain']
print(json.dumps(result, indent=2))
