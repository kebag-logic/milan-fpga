#!/usr/bin/env python3
"""Check tracked bytes, modes, index entries and required submodule gitlinks.
Usage: verify_integrity.py REPO
"""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')
head = '1098978f4a931a667e147b68a791520eb141c917'
tree = 'cad31d5084366583e8cd18c46e71ca6277c5d825'
def git(cwd, *args):
    return subprocess.check_output(['git','-C',str(cwd),*args],env=env)
def check(cwd, rev):
    entries = {}
    blobs = 0
    links = {}
    for row in git(cwd,'ls-tree','-rz',rev).split(b'\0'):
        if not row: continue
        info, path = row.split(b'\t',1)
        mode, kind, oid = info.decode().split()
        name = path.decode()
        entries[name] = (mode,oid)
        if kind == 'commit':
            links[name] = oid
            continue
        p = cwd / name
        s = p.lstat()
        if mode == '120000':
            assert stat.S_ISLNK(s.st_mode), name
            data = os.readlink(p).encode()
        else:
            assert stat.S_ISREG(s.st_mode), name
            assert bool(s.st_mode & 0o111) == (mode == '100755'), name
            data = p.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert actual == oid, name
        blobs += 1
    index = {}
    for row in git(cwd,'ls-files','--stage','-z').split(b'\0'):
        if not row: continue
        info,path = row.split(b'\t',1)
        mode,oid,stage = info.decode().split()
        assert stage == '0', path
        index[path.decode()] = (mode,oid)
    assert index == entries, 'index differs from tree'
    print(str(cwd.relative_to(root)) or '.', rev, 'blobs/modes/index PASS', blobs)
    return links
assert git(root,'rev-parse','HEAD').decode().strip() == head
assert git(root,'rev-parse','HEAD^{tree}').decode().strip() == tree
links = check(root,head)
for name in ('protocol-processor','gptp-processor','third_party/tsn-c-stack','third_party/verilog-axis','third_party/lwSRP'):
    sub = root / name
    assert Path(git(sub,'rev-parse','--show-toplevel').decode().strip()).resolve() == sub
    assert git(sub,'rev-parse','HEAD').decode().strip() == links[name]
    check(sub,links[name])
print('Exact head/tree and five required gitlinks PASS; external unused/uninitialized.')
