#!/usr/bin/env python3
"""Check raw tracked bytes, executable modes, index entries and pinned dependencies."""
import hashlib
import json
import os
import stat
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
expected = '0ad0e5180558a376f6064d0b33884ed40af6e196'
expected_tree = 'd89ab4e42af51456f1bd2855a4025668bfa0ca57'

def git(where, *args):
    return subprocess.check_output(['git', '-C', str(where), *args])

def audit(where, revision, required):
    assert git(where, 'rev-parse', 'HEAD').decode().strip() == revision
    assert git(where, 'diff', '--cached', '--raw', revision) == b''
    records = git(where, 'ls-tree', '-rz', revision).split(b'\0')
    checked = 0
    children = []
    for record in filter(None, records):
        info, raw_path = record.split(b'\t', 1)
        mode, kind, oid = info.split()
        path = where / os.fsdecode(raw_path)
        if kind == b'commit':
            rel = os.fsdecode(raw_path)
            if rel in required:
                result = audit(path, oid.decode(), set())
                children.append({'path': rel, 'oid': oid.decode(), 'result': result})
            else:
                children.append({'path': rel, 'oid': oid.decode(), 'worktree': 'not required; uninitialized'})
            continue
        st = path.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(st.st_mode)
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode), raw_path
            assert bool(st.st_mode & 0o111) == (mode == b'100755'), raw_path
            data = path.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert actual == oid.decode(), raw_path
        checked += 1
    assert git(where, 'status', '--porcelain', '--untracked-files=no') == b''
    return {'head': revision, 'tracked_blobs_checked': checked,
            'bytes_modes_index': 'PASS', 'gitlinks': children}

assert git(root, 'rev-parse', 'HEAD^{tree}').decode().strip() == expected_tree
required = {'protocol-processor', 'gptp-processor', 'third_party/lwSRP',
            'third_party/tsn-c-stack', 'third_party/verilog-axis'}
result = audit(root, expected, required)
result['tree'] = expected_tree
result['tracked_status'] = 'clean'
print(json.dumps(result, indent=2))
