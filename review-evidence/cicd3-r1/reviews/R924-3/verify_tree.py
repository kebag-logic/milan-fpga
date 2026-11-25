#!/usr/bin/env python3
"""Usage: python3 verify_tree.py CHECKOUT. Verify raw bytes, modes, index and gitlinks."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')
def git(at, *args):
    return subprocess.check_output(['git', '-C', str(at), *args], env=env)
def verify(at, revision):
    tree = {}
    for record in git(at, 'ls-tree', '-rz', revision).split(b'\0'):
        if record:
            meta, name = record.split(b'\t', 1)
            mode, kind, oid = meta.split()
            tree[name] = (mode, oid)
    index = {}
    for record in git(at, 'ls-files', '--stage', '-z').split(b'\0'):
        if record:
            meta, name = record.split(b'\t', 1)
            mode, oid, stage = meta.split()
            assert stage == b'0' and name not in index
            index[name] = (mode, oid)
    assert tree == index, f'index mismatch: {at.name}'
    links = {}
    for name, (mode, oid) in tree.items():
        path = at / os.fsdecode(name)
        if mode == b'160000':
            links[os.fsdecode(name)] = oid.decode()
            continue
        st = path.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(st.st_mode)
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode), os.fsdecode(name)
            assert bool(st.st_mode & 0o111) == (mode == b'100755'), os.fsdecode(name)
            data = path.read_bytes()
        digest = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert digest == oid.decode(), os.fsdecode(name)
    return len(tree), links
head = git(root, 'rev-parse', 'HEAD').decode().strip()
assert head == 'b0f2bc1a784d9f006204491c883ac2b1783e970a'
tree = git(root, 'rev-parse', 'HEAD^{tree}').decode().strip()
assert tree == 'bb0c6d59a6e22c499de562a642978b73c998c653'
count, links = verify(root, head)
submodules = {}
for name, pin in links.items():
    if name == 'external':
        continue
    at = root / name
    assert not at.is_symlink() and (at / '.git').is_file() and not (at / '.git').is_symlink()
    assert git(at, 'rev-parse', 'HEAD').decode().strip() == pin
    assert Path(git(at, 'rev-parse', '--show-superproject-working-tree').decode().strip()).resolve() == root
    n, nested = verify(at, pin)
    submodules[name] = {'pin': pin, 'entries': n, 'nested_gitlinks': nested}
print(json.dumps({'head':head, 'tree':tree, 'superproject_entries':count,
                  'submodules':submodules, 'external':'uninitialized; not required',
                  'all_tracked_blobs_modes_and_indexes_match':True}, indent=2))
