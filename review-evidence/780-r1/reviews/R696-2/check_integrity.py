#!/usr/bin/env python3
"""Compare actual tracked bytes/modes and the complete index to immutable trees."""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys

env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')
root = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
HEAD = '25f05752f7e50e3cf7e27008e434ffde930b4b6f'
def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args], env=env)
def check(repo, rev, label):
    assert git(repo, 'rev-parse', 'HEAD').decode().strip() == rev
    entries = {}
    links = []
    for record in git(repo, 'ls-tree', '-rz', rev).split(b'\0'):
        if not record:
            continue
        meta, name = record.split(b'\t', 1)
        mode, kind, oid = meta.decode().split()
        name = name.decode()
        entries[name] = (mode, oid, '0')
        path = repo / name
        if mode == '160000':
            links.append((name, oid))
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
    index = {}
    for record in git(repo, 'ls-files', '--stage', '-z').split(b'\0'):
        if record:
            meta, name = record.split(b'\t', 1)
            assert name.decode() not in index
            index[name.decode()] = tuple(meta.decode().split())
    assert index == entries, label + ' index differs'
    print(f'PASS {label}: {len(entries)} tree entries; tracked bytes, modes, index match {rev}')
    for name, oid in links:
        if name == 'external' and not (repo / name / '.git').exists():
            print(f'PASS historical unused gitlink {name}: {oid}; checkout uninitialized')
            continue
        assert (repo / name / '.git').is_file(), name
        assert Path(git(repo / name, 'rev-parse', '--show-toplevel').decode().strip()) == repo / name
        check(repo / name, oid, name)
check(root, HEAD, 'parent')
tree = git(root, 'rev-parse', HEAD + '^{tree}').decode().strip()
assert tree == '5db8e8298734d18c8a50ba24cd8c46140292302b'
print('PASS unchanged tree:', tree)
