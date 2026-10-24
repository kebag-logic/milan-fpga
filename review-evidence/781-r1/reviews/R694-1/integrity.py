#!/usr/bin/env python3
"""Verify committed bytes and modes directly, plus index and required gitlinks."""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
head = '8a4fa2f971427b1deb1f20a4b456a8a4d94bf008'
tree = '57cbe969ebfcd88b476edc9408446c13e299a01d'
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')
def git(where, *args):
    return subprocess.check_output(['git', '-C', str(where), *args], env=env)
def verify(where, revision, submodules=False):
    records = git(where, 'ls-tree', '-rz', revision).split(b'\0')
    expected_index = {}
    blobs = 0
    links = {}
    for row in filter(None, records):
        metadata, rel = row.split(b'\t', 1)
        mode, kind, oid = metadata.split()
        expected_index[rel] = (mode, oid, b'0')
        path = where / os.fsdecode(rel)
        if kind == b'commit':
            links[os.fsdecode(rel)] = oid.decode()
            continue
        s = path.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(s.st_mode), rel
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(s.st_mode), rel
            actual_mode = b'100755' if s.st_mode & 0o111 else b'100644'
            assert mode == actual_mode, (rel, 'mode', mode, actual_mode)
            data = path.read_bytes()
        actual = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert actual == oid.decode(), (rel, 'blob mismatch')
        blobs += 1
    index = {}
    for row in filter(None, git(where, 'ls-files', '--stage', '-z').split(b'\0')):
        metadata, rel = row.split(b'\t', 1)
        mode, oid, stage = metadata.split()
        assert rel not in index, ('unmerged', rel)
        index[rel] = (mode, oid, stage)
    assert index == expected_index, 'index differs from committed tree'
    print(f'{where.name}: {blobs} blobs, exact bytes/modes and index PASS')
    return links
assert git(root,'rev-parse','HEAD').decode().strip() == head
assert git(root,'rev-parse','HEAD^{tree}').decode().strip() == tree
assert subprocess.run(['git', '-C', str(root), 'symbolic-ref', '-q', 'HEAD'],
                      env=env, capture_output=True).returncode == 1
links = verify(root, head)
for name in ['protocol-processor', 'gptp-processor', 'third_party/verilog-axis',
             'third_party/tsn-c-stack', 'third_party/lwSRP']:
    sub = root / name
    assert not sub.is_symlink() and (sub/'.git').is_file(), name
    assert git(sub,'rev-parse','HEAD').decode().strip() == links[name], name
    assert Path(git(sub,'rev-parse','--show-superproject-working-tree').decode().strip()).resolve() == root
    verify(sub, links[name])
    print(f'gitlink {name}: {links[name]} PASS')
assert git(root,'diff','--raw','a032c6d6',head,'--','hdl','tb','protocol-processor',
           'gptp-processor','third_party') == b''
print('Product RTL, suite sources and dependency gitlinks unchanged from base PASS')
print(f'HEAD {head}; TREE {tree}; integrity PASS')
