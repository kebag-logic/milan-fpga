#!/usr/bin/env python3
"""Check actual blob bytes, modes, index entries and required gitlinks."""
import hashlib
import os
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1])
head = '4958ca4f630da1f715bdcd78113b798bbe332b81'
tree = 'cc92bd5f2ef6d44d1510157a612578458e1e0ab6'
required = {'protocol-processor', 'gptp-processor', 'third_party/verilog-axis', 'third_party/tsn-c-stack'}

def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args])

def verify(repo, rev, label):
    entries = git(repo, 'ls-tree', '-rz', rev).split(b'\0')
    wanted = {}
    links = {}
    blobs = 0
    for entry in entries:
        if not entry:
            continue
        metadata, name = entry.split(b'\t', 1)
        mode, kind, oid = metadata.split()
        relative = os.fsdecode(name)
        wanted[name] = (mode, oid)
        path = repo / relative
        if kind == b'commit':
            links[relative] = oid.decode()
            continue
        if mode == b'120000':
            assert path.is_symlink(), relative
            data = os.fsencode(os.readlink(path))
        else:
            assert path.is_file() and not path.is_symlink(), relative
            data = path.read_bytes()
            actual_mode = b'100755' if path.stat().st_mode & 0o111 else b'100644'
            assert actual_mode == mode, (relative, mode, actual_mode)
        actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert actual == oid.decode(), relative
        blobs += 1
    index = {}
    for row in git(repo, 'ls-files', '--stage', '-z').split(b'\0'):
        if row:
            meta, name = row.split(b'\t', 1)
            mode, oid, stage = meta.split()
            assert stage == b'0', name
            index[name] = (mode, oid)
    assert index == wanted, label
    print(label + ':', blobs, 'tracked blob bytes/modes and all index entries match', rev)
    return links

assert git(root, 'rev-parse', 'HEAD').decode().strip() == head
assert git(root, 'rev-parse', 'HEAD^{tree}').decode().strip() == tree
links = verify(root, head, 'superproject')
assert required <= links.keys()
for relative, oid in links.items():
    sub = root / relative
    if not (sub / '.git').exists():
        assert relative not in required, relative
        print(relative + ': optional submodule not initialized; gitlink', oid)
        continue
    assert git(sub, 'rev-parse', 'HEAD').decode().strip() == oid, relative
    verify(sub, oid, relative)
print('Exact head/tree restored; four required submodules verified at their gitlinks.')
