#!/usr/bin/env python3
"""Verify tracked bytes, executable/symlink modes, index and initialized gitlinks."""
import hashlib
import json
import os
import pathlib
import stat
import subprocess
import sys

repo = pathlib.Path(sys.argv[1]).resolve()
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')
def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], env=env)
errors = []
results = []
def check(root, expected):
    head = git(root, 'rev-parse', 'HEAD').decode().strip()
    if head != expected:
        errors.append(f'{root.name}: HEAD {head} != {expected}')
    entries = {}
    for row in git(root, 'ls-tree', '-rz', '--full-tree', expected).split(b'\0'):
        if not row:
            continue
        meta, name = row.split(b'\t', 1)
        mode, kind, oid = meta.decode().split()
        entries[os.fsdecode(name)] = (mode, oid)
    index = {}
    for row in git(root, 'ls-files', '--stage', '-z').split(b'\0'):
        if not row:
            continue
        meta, name = row.split(b'\t', 1)
        mode, oid, stage = meta.decode().split()
        if stage != '0':
            errors.append(f'{root.name}: unmerged index {os.fsdecode(name)}')
        index[os.fsdecode(name)] = (mode, oid)
    if index != entries:
        errors.append(f'{root.name}: index differs from expected tree')
    links = {}
    blobs = 0
    for name, (mode, oid) in entries.items():
        p = root / name
        if mode == '160000':
            links[name] = oid
            if (p / '.git').exists():
                check(p, oid)
            continue
        try:
            st = p.lstat()
            if mode == '120000':
                assert stat.S_ISLNK(st.st_mode)
                data = os.fsencode(os.readlink(p))
            else:
                assert stat.S_ISREG(st.st_mode)
                actual_mode = '100755' if st.st_mode & stat.S_IXUSR else '100644'
                assert mode == actual_mode
                data = p.read_bytes()
            actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
            assert actual == oid
            blobs += 1
        except (OSError, AssertionError):
            errors.append(f'{root.name}: bytes or mode mismatch {name}')
    results.append({'repository': '.' if root == repo else str(root.relative_to(repo)),
                    'head': head, 'tree': git(root, 'rev-parse', expected + '^{tree}').decode().strip(),
                    'verified_blobs': blobs, 'index_matches': index == entries,
                    'gitlinks': links})
check(repo, 'ee5ece607816a1bfc834bd51734b703a8aab8e46')
print(json.dumps({'repositories': results, 'errors': errors}, indent=2))
sys.exit(bool(errors))
