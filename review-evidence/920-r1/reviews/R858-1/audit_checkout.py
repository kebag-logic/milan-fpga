#!/usr/bin/env python3
"""Verify tracked working bytes, modes, index and initialized submodule pins."""
import argparse
import hashlib
import json
import os
import stat
import subprocess
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('repository', type=Path)
a = p.parse_args()
root = a.repository.resolve()
HEAD = 'bd252db1d73511307c0ecb78470f0d15d0c3ea9b'
TREE = '2cc90eb47ddd00d5bd7d1d5edb6c7ec0937b509a'
failures = []
results = []

def git(where, *args):
    return subprocess.check_output(['git', '-C', str(where), *args])

def audit(where, expected, name):
    actual = git(where, 'rev-parse', 'HEAD').decode().strip()
    if actual != expected:
        failures.append(f'{name}: HEAD {actual}, expected {expected}')
    entries = {}
    for item in git(where, 'ls-tree', '-rz', 'HEAD').split(b'\0'):
        if not item:
            continue
        meta, path = item.split(b'\t', 1)
        mode, kind, oid = meta.decode().split()
        entries[os.fsdecode(path)] = (mode, kind, oid)
    index = {}
    for item in git(where, 'ls-files', '--stage', '-z').split(b'\0'):
        if not item:
            continue
        meta, path = item.split(b'\t', 1)
        mode, oid, stage = meta.decode().split()
        key = os.fsdecode(path)
        if stage != '0':
            failures.append(f'{name}/{key}: index conflict stage {stage}')
        index[key] = (mode, oid)
    expected_index = {k: (v[0], v[2]) for k, v in entries.items()}
    if index != expected_index:
        failures.append(f'{name}: index differs from HEAD')
    blobs = 0
    links = []
    for path, (mode, kind, oid) in entries.items():
        target = where / path
        if kind == 'commit':
            initialized = (target / '.git').exists()
            links.append({'path': path, 'oid': oid, 'initialized': initialized})
            if initialized:
                audit(target, oid, f'{name}/{path}')
            elif name == '.' and path != 'external':
                failures.append(f'{path}: required submodule not initialized')
            continue
        try:
            st = target.lstat()
            if mode == '120000':
                if not stat.S_ISLNK(st.st_mode):
                    failures.append(f'{name}/{path}: not a symlink')
                data = os.fsencode(os.readlink(target))
            else:
                if not stat.S_ISREG(st.st_mode):
                    failures.append(f'{name}/{path}: not a regular file')
                if bool(st.st_mode & 0o111) != (mode == '100755'):
                    failures.append(f'{name}/{path}: executable mode differs')
                data = target.read_bytes()
            digest = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
            if digest != oid:
                failures.append(f'{name}/{path}: tracked bytes differ')
            blobs += 1
        except OSError as exc:
            failures.append(f'{name}/{path}: {type(exc).__name__}')
    results.append({'repository': name, 'head': actual,
                    'tree': git(where, 'rev-parse', 'HEAD^{tree}').decode().strip(),
                    'blobs_checked': blobs, 'index_matches': index == expected_index,
                    'gitlinks': links})

audit(root, HEAD, '.')
if git(root, 'rev-parse', 'HEAD^{tree}').decode().strip() != TREE:
    failures.append('root: wrong tree')
print(json.dumps({'expected_head': HEAD, 'expected_tree': TREE,
                  'repositories': results, 'failures': failures}, indent=2))
raise SystemExit(bool(failures))
