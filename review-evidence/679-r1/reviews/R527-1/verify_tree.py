#!/usr/bin/env python3
"""Prove tracked bytes, modes, index and required submodule pins."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

HEAD = '0a004a8cc2ad879e74d8e4168bd4a39a12d5dbbe'
TREE = 'dfc55c6343d0c4c943e0c127dee9912ea94357fa'
root = Path(sys.argv[1]).resolve()
env = {**os.environ, 'GIT_NO_REPLACE_OBJECTS': '1'}

def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args], env=env)

def check(repo, rev):
    entries = git(repo, 'ls-tree', '-rz', rev).split(b'\0')
    expected_index = []
    files = 0
    links = {}
    for entry in filter(None, entries):
        spec, raw_name = entry.split(b'\t', 1)
        mode, kind, oid = spec.split()
        expected_index.append(mode + b' ' + oid + b' 0\t' + raw_name + b'\0')
        name = os.fsdecode(raw_name)
        path = repo / name
        if kind == b'commit':
            links[name] = oid.decode()
            continue
        st = path.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(st.st_mode), name
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode), name
            assert bool(st.st_mode & 0o111) == (mode == b'100755'), name
            data = path.read_bytes()
        digest = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert digest == oid.decode(), name
        files += 1
    assert b''.join(expected_index) == git(repo, 'ls-files', '--stage', '-z'), 'index mismatch'
    return {'tracked_blobs_verified': files, 'gitlinks': links,
            'index_sha256': hashlib.sha256(git(repo, 'ls-files', '--stage', '-z')).hexdigest()}

assert git(root, 'rev-parse', 'HEAD').decode().strip() == HEAD
assert git(root, 'rev-parse', 'HEAD^{tree}').decode().strip() == TREE
result = {'head': HEAD, 'tree': TREE, 'root': check(root, HEAD), 'required_submodules': {}}
for name in ('protocol-processor', 'gptp-processor', 'third_party/verilog-axis'):
    pin = result['root']['gitlinks'][name]
    repo = root / name
    assert (repo / '.git').is_file(), name
    assert git(repo, 'rev-parse', 'HEAD').decode().strip() == pin, name
    assert Path(git(repo, 'rev-parse', '--show-superproject-working-tree').decode().strip()).resolve() == root
    result['required_submodules'][name] = {'pin': pin, **check(repo, pin)}
print(json.dumps(result, indent=2, sort_keys=True))
