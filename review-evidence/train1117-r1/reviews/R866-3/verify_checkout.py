#!/usr/bin/env python3
"""Verify raw tracked bytes, executable/symlink modes, index entries and gitlinks."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args])

def verify(root, revision):
    tree = {}
    for entry in git(root, 'ls-tree', '-rz', revision).split(b'\0'):
        if entry:
            meta, path = entry.split(b'\t', 1)
            mode, kind, oid = meta.split()
            tree[path] = (mode, oid)
    index = {}
    for entry in git(root, 'ls-files', '--stage', '-z').split(b'\0'):
        if entry:
            meta, path = entry.split(b'\t', 1)
            mode, oid, stage = meta.split()
            assert stage == b'0'
            assert path not in index
            index[path] = (mode, oid)
    assert index == tree, 'index differs from requested tree'
    blobs = 0
    for path, (mode, oid) in tree.items():
        if mode == b'160000':
            continue
        p = root / os.fsdecode(path)
        attrs = p.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(attrs.st_mode), str(p)
            data = os.fsencode(os.readlink(p))
        else:
            assert stat.S_ISREG(attrs.st_mode), str(p)
            gotmode = b'100755' if attrs.st_mode & 0o111 else b'100644'
            assert gotmode == mode, str(p)
            data = p.read_bytes()
        digest = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest().encode()
        assert digest == oid, os.fsdecode(path)
        blobs += 1
    return {'revision': revision, 'tracked_blobs_verified': blobs, 'index_entries_verified': len(tree),
            'status': git(root, 'status', '--porcelain').decode()}, tree

root = Path.cwd()
head = '0839453f6d7135063e904bcaf4ac1852ad6b522a'
assert git(root, 'rev-parse', 'HEAD').decode().strip() == head
report, entries = verify(root, head)
report['tree'] = git(root, 'rev-parse', 'HEAD^{tree}').decode().strip()
report['submodules'] = {}
for name in ['protocol-processor', 'gptp-processor', 'third_party/verilog-axis',
             'third_party/tsn-c-stack', 'third_party/lwSRP']:
    mode, pin = entries[name.encode()]
    assert mode == b'160000'
    child = root / name
    assert not child.is_symlink()
    assert (child / '.git').is_file(), 'required real submodule gitfile'
    actual = git(child, 'rev-parse', 'HEAD').decode().strip()
    assert actual == pin.decode()
    report['submodules'][name] = verify(child, actual)[0]
report['unused_external'] = entries[b'external'][1].decode()
print(json.dumps(report, indent=2))
