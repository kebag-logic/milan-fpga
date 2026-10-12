#!/usr/bin/env python3
"""Compare raw tracked bytes, modes, index records, and required submodule pins.

Usage: python3 verify_integrity.py /path/to/review/checkout
Read-only; reports identities without embedding checkout locations.
"""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

HEAD = '31e53e82a4a1604569ccacba8473f21e70b9cbc0'
TREE = '9dc0b704562f67cab1d805b40d56a5c983ddcebb'
REQUIRED = ('protocol-processor', 'gptp-processor', 'third_party/verilog-axis')
ENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1', GIT_OPTIONAL_LOCKS='0')


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], env=ENV)


def verify(root, revision):
    entries = {}
    for record in git(root, 'ls-tree', '-rz', '--full-tree', revision).split(b'\0'):
        if not record:
            continue
        meta, path = record.split(b'\t', 1)
        mode, kind, oid = meta.decode().split()
        entries[path] = (mode, oid)
        if kind == 'commit':
            continue
        selected = root / os.fsdecode(path)
        info = selected.lstat()
        if mode == '120000':
            assert stat.S_ISLNK(info.st_mode), path
            raw = os.fsencode(os.readlink(selected))
        else:
            assert stat.S_ISREG(info.st_mode), path
            assert mode == ('100755' if info.st_mode & 0o111 else '100644'), path
            raw = selected.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
        assert actual == oid, path
    index = {}
    for record in git(root, 'ls-files', '--stage', '-z').split(b'\0'):
        if not record:
            continue
        meta, path = record.split(b'\t', 1)
        mode, oid, stage = meta.decode().split()
        assert stage == '0' and path not in index, path
        index[path] = (mode, oid)
    assert entries == index, 'index differs from expected commit'
    return entries


def main():
    root = Path(sys.argv[1]).resolve()
    assert git(root, 'rev-parse', 'HEAD').decode().strip() == HEAD
    assert git(root, 'rev-parse', 'HEAD^{tree}').decode().strip() == TREE
    assert not git(root, 'for-each-ref', '--format=%(refname)', 'refs/replace')
    entries = verify(root, HEAD)
    result = {'head': HEAD, 'tree': TREE, 'raw_tracked_bytes_modes_index': 'PASS',
              'top_level_entries': len(entries), 'submodules': []}
    for path, (mode, oid) in entries.items():
        if mode != '160000':
            continue
        name = os.fsdecode(path)
        row = {'path': name, 'gitlink': oid}
        sub = root / name
        if name in REQUIRED:
            assert (sub / '.git').is_file(), name
            assert git(sub, 'rev-parse', 'HEAD').decode().strip() == oid, name
            superproject = git(sub, 'rev-parse', '--show-superproject-working-tree').decode().strip()
            assert Path(superproject).resolve() == root, name
            child_entries = verify(sub, oid)
            row.update(checkout='PASS', tracked_entries=len(child_entries))
        else:
            row['checkout'] = 'not used; gitlink verified against head and index'
        result['submodules'].append(row)
    result['untracked_nonignored'] = git(root, 'ls-files', '--others', '--exclude-standard').decode().splitlines()
    assert not result['untracked_nonignored']
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
