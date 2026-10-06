#!/usr/bin/env python3
"""Prove raw working bytes, modes, index records and required submodule pins."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

HEAD = '6c94e9f5f496ac25f8c4e31f9e3685c725de29f3'
TREE = '25b32c793bd4bb6d959640094a44fb2b5c9d7a45'
REQUIRED = ('protocol-processor', 'gptp-processor', 'third_party/verilog-axis')
ap = argparse.ArgumentParser()
ap.add_argument('checkout', type=Path)
args = ap.parse_args()
root = args.checkout.resolve()
env = {**os.environ, 'GIT_NO_REPLACE_OBJECTS': '1'}

def git(where, *argv):
    return subprocess.check_output(['rtk', 'proxy', 'git', '-C', str(where), *argv], env=env)

def audit(where, rev):
    assert git(where, 'rev-parse', 'HEAD').decode().strip() == rev
    raw_tree = git(where, 'ls-tree', '-rz', rev)
    entries = {}
    count = 0
    links = {}
    for record in raw_tree.split(b'\0'):
        if not record:
            continue
        meta, path = record.split(b'\t', 1)
        mode, kind, oid = meta.split()
        entries[path] = (mode, oid)
        file = where / os.fsdecode(path)
        if mode == b'160000':
            assert kind == b'commit'
            links[os.fsdecode(path)] = oid.decode()
            continue
        assert kind == b'blob'
        st = file.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(st.st_mode)
            data = os.fsencode(os.readlink(file))
        else:
            assert mode in (b'100644', b'100755') and stat.S_ISREG(st.st_mode)
            assert bool(st.st_mode & 0o111) == (mode == b'100755')
            data = file.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest().encode()
        assert actual == oid, os.fsdecode(path)
        count += 1
    index = {}
    raw_index = git(where, 'ls-files', '--stage', '-z')
    for record in raw_index.split(b'\0'):
        if not record:
            continue
        meta, path = record.split(b'\t', 1)
        mode, oid, stage = meta.split()
        assert stage == b'0' and path not in index
        index[path] = (mode, oid)
    assert entries == index
    flags = git(where, 'ls-files', '-v', '-z')
    assert all(r.startswith(b'H ') for r in flags.split(b'\0') if r)
    return {'head': rev, 'blobs_verified': count, 'index_records': len(index),
            'tree_sha256': hashlib.sha256(raw_tree).hexdigest(),
            'index_records_sha256': hashlib.sha256(raw_index).hexdigest(),
            'index_flags_sha256': hashlib.sha256(flags).hexdigest(), 'gitlinks': links,
            'raw_blob_bytes_modes_kinds_index_and_flags': 'PASS'}

result = {'superproject': audit(root, HEAD), 'required_submodules': {}}
assert git(root, 'rev-parse', 'HEAD^{tree}').decode().strip() == TREE
for name in REQUIRED:
    sub = root / name
    assert not sub.is_symlink() and (sub / '.git').is_file()
    assert Path(git(sub, 'rev-parse', '--show-superproject-working-tree').decode().strip()).resolve() == root
    result['required_submodules'][name] = audit(sub, result['superproject']['gitlinks'][name])
assert not git(root, 'status', '--porcelain=v1', '--untracked-files=all').strip()
result.update(result='PASS', tree=TREE, clean_status=True, source_edits=False)
print(json.dumps(result, indent=2))
