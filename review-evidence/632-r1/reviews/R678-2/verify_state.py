#!/usr/bin/env python3
"""Verify tracked bytes, modes, index entries and required submodule pins."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

repo = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
head = '2ff30f0dc5e89be46f8103272883885e8553f4b8'
required = ['protocol-processor', 'gptp-processor', 'third_party/verilog-axis', 'third_party/tsn-c-stack']

def git(root, *args):
    return subprocess.check_output(['git', *args], cwd=root)

def verify(root, revision):
    assert git(root, 'rev-parse', 'HEAD').decode().strip() == revision
    entries = {}
    for item in git(root, 'ls-tree', '-rz', '--full-tree', revision).split(b'\0'):
        if not item:
            continue
        meta, path = item.split(b'\t', 1)
        mode, kind, oid = meta.split()
        entries[path] = (mode, kind, oid)
    index = {}
    for item in git(root, 'ls-files', '--stage', '-z').split(b'\0'):
        if not item:
            continue
        meta, path = item.split(b'\t', 1)
        mode, oid, stage = meta.split()
        assert stage == b'0', (path, 'unmerged index')
        index[path] = (mode, oid)
    assert index == {p: (m, o) for p, (m, k, o) in entries.items()}, 'index differs'
    blobs = 0
    links = {}
    for rawpath, (mode, kind, oid) in entries.items():
        name = os.fsdecode(rawpath)
        path = root / name
        if kind == b'commit':
            links[name] = oid.decode()
            continue
        st = path.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(st.st_mode), name
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode), name
            actual = b'100755' if st.st_mode & stat.S_IXUSR else b'100644'
            assert actual == mode, (name, 'mode')
            data = path.read_bytes()
        actual_oid = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert actual_oid == oid.decode(), (name, 'bytes')
        blobs += 1
    return {'head': revision, 'tree': git(root, 'rev-parse', revision + '^{tree}').decode().strip(),
            'tracked_blobs_verified': blobs, 'index_equal': True, 'gitlinks': links}

result = {'parent': verify(repo, head), 'required_submodules': {}}
for name in required:
    sub = repo / name
    assert (sub / '.git').is_file(), (name, 'not an initialized submodule')
    superroot = git(sub, 'rev-parse', '--show-superproject-working-tree').decode().strip()
    assert Path(superroot).resolve() == repo, (name, 'wrong superproject')
    result['required_submodules'][name] = verify(sub, result['parent']['gitlinks'][name])
result['status'] = 'PASS'
(packet / 'receipts' / 'exact-state.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
