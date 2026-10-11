#!/usr/bin/env python3
"""Verify exact tracked bytes, kinds, executable modes, index and gitlinks."""
import argparse
import hashlib
import os
import stat
import subprocess
from pathlib import Path

HEAD = 'be607527eaac84cfc8d7456167b070a22228345b'
TREE = '0ff64b4d0d26c7d6d737802cafacf3fde3356f04'
REQUIRED = {'gptp-processor', 'protocol-processor', 'third_party/verilog-axis',
            'third_party/lwSRP', 'third_party/tsn-c-stack'}
ap = argparse.ArgumentParser()
ap.add_argument('root', type=Path)
args = ap.parse_args()
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1', GIT_GRAFT_FILE='/dev/null/no-grafts')

def git(root, *argv):
    return subprocess.check_output(['git', '-C', str(root), *argv], env=env)

def verify(root, revision, label):
    assert git(root, 'rev-parse', 'HEAD').decode().strip() == revision
    records = git(root, 'ls-tree', '-rz', revision).split(b'\0')
    expected = {}
    count = 0
    for record in filter(None, records):
        meta, rawname = record.split(b'\t', 1)
        mode, kind, oid = meta.decode().split()
        name = os.fsdecode(rawname)
        expected[rawname] = (mode, oid, '0')
        path = root / name
        if mode == '160000':
            if label == 'root' and name in REQUIRED:
                assert (path / '.git').is_file(), name + ' is not initialized as a submodule'
                verify(path, oid, name)
            else:
                print(label, name, 'gitlink', oid, '(not populated; unused)')
            continue
        status = path.lstat()
        if mode == '120000':
            assert stat.S_ISLNK(status.st_mode), name
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(status.st_mode), name
            actual_mode = '100755' if status.st_mode & stat.S_IXUSR else '100644'
            assert actual_mode == mode, name + ' mode'
            data = path.read_bytes()
        digest = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert digest == oid, name + ' bytes'
        count += 1
    index = {}
    for record in filter(None, git(root, 'ls-files', '--stage', '-z').split(b'\0')):
        meta, rawname = record.split(b'\t', 1)
        mode, oid, stage = meta.decode().split()
        assert rawname not in index and stage == '0', 'unmerged index'
        index[rawname] = (mode, oid, stage)
    assert index == expected, label + ' index differs from commit'
    print(label, revision, count, 'tracked blobs: bytes/kinds/modes/index PASS')

root = args.root.resolve()
assert git(root, 'rev-parse', 'HEAD^{tree}').decode().strip() == TREE
assert subprocess.run(['git', '-C', str(root), 'symbolic-ref', '-q', 'HEAD'],
                      stdout=subprocess.DEVNULL, env=env, check=False).returncode == 1
verify(root, HEAD, 'root')
print('HEAD', HEAD, 'TREE', TREE, 'EXACT')
