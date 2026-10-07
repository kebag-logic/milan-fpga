#!/usr/bin/env python3
"""Verify tracked bytes, filesystem kinds/modes, full index entries and public pins."""
import argparse
import hashlib
import os
import pathlib
import stat
import subprocess

HEAD = 'c7b69cd0fb2bdf980546ab413b3b82198267cbd8'
TREE = 'f391905e7afd3485edc9d21ab317dd0802959c45'
PINS = {
    'gptp-processor': '5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d',
    'protocol-processor': 'ead8036035affd53ef4b29979190f2f4f67084c0',
    'third_party/verilog-axis': '48ff7a7e2ef782cf778d47910cf85835c64b1bce',
}
p = argparse.ArgumentParser()
p.add_argument('--repo', required=True, type=pathlib.Path)
a = p.parse_args()
root = a.repo.resolve()
env = os.environ.copy()
env['GIT_NO_REPLACE_OBJECTS'] = '1'

def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args], env=env)

def verify(repo, revision, label):
    assert git(repo, 'rev-parse', 'HEAD').decode().strip() == revision
    entries = {}
    for record in git(repo, 'ls-tree', '-rz', revision).split(b'\0'):
        if not record:
            continue
        meta, name = record.split(b'\t', 1)
        mode, kind, oid = meta.split()
        entries[name] = mode, oid
        if kind != b'blob':
            continue
        path = repo / os.fsdecode(name)
        s = path.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(s.st_mode), name
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(s.st_mode), name
            assert bool(s.st_mode & 0o111) == (mode == b'100755'), name
            data = path.read_bytes()
        digest = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest().encode()
        assert digest == oid, (name, 'blob mismatch')
    index = {}
    for record in git(repo, 'ls-files', '--stage', '-z').split(b'\0'):
        if not record:
            continue
        meta, name = record.split(b'\t', 1)
        mode, oid, stage = meta.split()
        assert stage == b'0' and name not in index
        index[name] = mode, oid
    assert index == entries, (label, 'index differs')
    flags = git(repo, 'ls-files', '-v', '-z').split(b'\0')
    assert all(not row or row[:1] == b'H' for row in flags), (label, 'hidden-index flag')
    print(f'PASS {label}: HEAD={revision}; {len(entries)} entries, tracked blob bytes/modes/index exact; no hidden-index flags')
    return entries

entries = verify(root, HEAD, 'candidate')
assert git(root, 'rev-parse', 'HEAD^{tree}').decode().strip() == TREE
print('PASS candidate tree='+TREE)
for name, pin in PINS.items():
    assert entries[name.encode()] == (b'160000', pin.encode())
    sub = root/name
    assert not sub.is_symlink() and (sub/'.git').is_file()
    assert pathlib.Path(git(sub, 'rev-parse', '--show-superproject-working-tree').decode().strip()).resolve() == root
    verify(sub, pin, name)
print('Uninitialized external gitlink excluded as prescribed; its parent tree/index entry was verified.')
print('PASS no candidate tracked edits were made during this review.')
