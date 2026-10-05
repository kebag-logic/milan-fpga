#!/usr/bin/env python3
"""Verify tracked bytes, kinds, executable modes, stage-0 index and required gitlinks."""
import argparse
import hashlib
import os
from pathlib import Path
import stat
import subprocess

ap = argparse.ArgumentParser()
ap.add_argument('--repo', type=Path, required=True)
args = ap.parse_args()
root = args.repo.resolve()
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1', GIT_OPTIONAL_LOCKS='0')
def git(repo, *argv):
    return subprocess.check_output(['git', *argv], cwd=repo, env=env)
def check(repo, rev, label):
    assert git(repo, 'rev-parse', 'HEAD').decode().strip() == rev
    expected, links = {}, {}
    count = 0
    for record in git(repo, 'ls-tree', '-rz', '--full-tree', rev).split(b'\0'):
        if not record:
            continue
        info, name = record.split(b'\t', 1)
        mode, kind, oid = info.split()
        expected[name] = (mode, oid, b'0')
        path = repo / os.fsdecode(name)
        if mode == b'160000':
            links[os.fsdecode(name)] = oid.decode()
            continue
        st = path.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(st.st_mode), name
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode), name
            assert bool(st.st_mode & 0o111) == (mode == b'100755'), name
            data = path.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest().encode()
        assert actual == oid, name
        count += 1
    index = {}
    for record in git(repo, 'ls-files', '--stage', '-z').split(b'\0'):
        if record:
            info, name = record.split(b'\t', 1)
            assert name not in index, name
            index[name] = tuple(info.split())
    assert index == expected, label + ': index differs from commit'
    print(f'PASS {label}: {count} tracked blobs, exact bytes/kinds/modes/index; HEAD {rev}')
    return links

head = 'a3ea8ffe16585270911705ffabd68ca5e17fc9e0'
assert git(root, 'rev-parse', 'HEAD^{tree}').decode().strip() == '07f62aee959ab4004ef4f2c8a3b10f0b6d52593c'
links = check(root, head, 'root')
for sub in ['protocol-processor', 'gptp-processor', 'third_party/verilog-axis']:
    repo = root / sub
    assert repo.is_dir() and not repo.is_symlink()
    assert (repo / '.git').is_file()
    assert Path(git(repo, 'rev-parse', '--show-superproject-working-tree').decode().strip()).resolve() == root
    check(repo, links[sub], sub)
    print(f'PASS required gitlink {sub}: {links[sub]}')
print('Root tree: 07f62aee959ab4004ef4f2c8a3b10f0b6d52593c')
print('Tracked sources were never edited; no restoration was necessary.')
status = git(root, 'status', '--porcelain=v1', '--untracked-files=all').decode()
print('Working-tree status: ' + (status.strip() or 'clean'))
