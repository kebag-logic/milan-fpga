#!/usr/bin/env python3
"""Check every tracked blob, executable bit, index entry and required gitlink.
Usage: python verify_checkout.py REPO OUTPUT_JSON
"""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

repo, output = map(Path, sys.argv[1:])
HEAD = 'f1b2489f5b1c929e81eeae79a469b2b27c47e340'
TREE = '635001816412f045f479ec4776fe641969a48815'
REQUIRED = {'gptp-processor': '5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d',
            'protocol-processor': '2ad2f845dd583f8310075fa2380cb60a04fd091a',
            'third_party/verilog-axis': '48ff7a7e2ef782cf778d47910cf85835c64b1bce'}

def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args])

def audit(root, expected):
    head = git(root, 'rev-parse', 'HEAD').decode().strip()
    assert head == expected, (root.name, head, expected)
    tree = {}
    for record in git(root, 'ls-tree', '-rz', 'HEAD').split(b'\0'):
        if not record:
            continue
        meta, name = record.split(b'\t', 1)
        mode, kind, oid = meta.decode().split()
        tree[os.fsdecode(name)] = (mode, oid)
    index = {}
    for record in git(root, 'ls-files', '--stage', '-z').split(b'\0'):
        if not record:
            continue
        meta, name = record.split(b'\t', 1)
        mode, oid, stage = meta.decode().split()
        assert stage == '0', (os.fsdecode(name), stage)
        index[os.fsdecode(name)] = (mode, oid)
    assert tree == index, 'index differs from HEAD'
    count = 0
    links = {}
    for name, (mode, oid) in tree.items():
        if mode == '160000':
            links[name] = oid
            continue
        path = root/name
        m = path.lstat().st_mode
        if mode == '120000':
            assert stat.S_ISLNK(m), name
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(m), name
            assert bool(m & 0o111) == (mode == '100755'), name
            data = path.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert actual == oid, name
        count += 1
    return dict(head=head, tree=git(root, 'rev-parse', 'HEAD^{tree}').decode().strip(),
                tracked_blobs_checked=count, bytes_equal=True, modes_equal=True,
                index_equal=True, gitlinks=links,
                status=git(root, 'status', '--porcelain=v1', '--untracked-files=all').decode())

result = {'parent': audit(repo, HEAD), 'required_submodules': {}}
assert result['parent']['tree'] == TREE
for name, oid in REQUIRED.items():
    assert result['parent']['gitlinks'][name] == oid
    result['required_submodules'][name] = audit(repo/name, oid)
assert all(not v['status'] for v in [result['parent'], *result['required_submodules'].values()])
output.write_text(json.dumps(result, indent=2) + '\n')
print('PASS: exact tracked bytes, modes, index, clean status and all three required submodule pins.')
