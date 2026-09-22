#!/usr/bin/env python3
"""Read-only exact-byte/kind/mode/index audit; no git-status shortcuts."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

def git(root, *args):
    return subprocess.check_output(['rtk', 'proxy', 'git', '-C', str(root), *args],
                                   env=dict(os.environ, GIT_NO_REPLACE_OBJECTS='1', GIT_OPTIONAL_LOCKS='0'))

def audit(root, revision):
    rows = git(root, 'ls-tree', '-rz', revision).split(b'\0')
    expected = []
    errors = []
    count = 0
    for row in filter(None, rows):
        header, rawpath = row.split(b'\t', 1)
        mode, kind, oid = header.decode().split()
        name = os.fsdecode(rawpath)
        expected.append((mode, oid, '0', name))
        if kind == 'commit':
            continue
        p = root / name
        try:
            s = p.lstat()
            if mode == '120000':
                assert stat.S_ISLNK(s.st_mode), 'not a symlink'
                data = os.fsencode(os.readlink(p))
            else:
                assert stat.S_ISREG(s.st_mode), 'not a regular file'
                assert bool(s.st_mode & 0o111) == (mode == '100755'), 'executable mode differs'
                data = p.read_bytes()
            actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
            assert actual == oid, 'blob differs'
            count += 1
        except (OSError, AssertionError) as e:
            errors.append({'path': name, 'error': str(e)})
    actual_index = []
    for row in filter(None, git(root, 'ls-files', '--stage', '-z').split(b'\0')):
        hdr, p = row.split(b'\t', 1)
        mode, oid, stage = hdr.decode().split()
        actual_index.append((mode, oid, stage, os.fsdecode(p)))
    if sorted(actual_index) != sorted(expected):
        errors.append({'index': 'stage/mode/blob/population mismatch'})
    return {'head': git(root, 'rev-parse', 'HEAD').decode().strip(),
            'expected': revision, 'tree': git(root, 'rev-parse', revision + '^{tree}').decode().strip(),
            'blobs_verified': count, 'index_records': len(actual_index), 'errors': errors}

def main():
    p = argparse.ArgumentParser()
    p.add_argument('root', type=Path)
    p.add_argument('output', type=Path)
    args = p.parse_args()
    root = args.root.resolve()
    head = '28e350b99ac240a750326b762c6d029f0653362c'
    result = {'root': str(root), 'source': audit(root, head), 'submodules': {}}
    for name in ('third_party/verilog-axis', 'protocol-processor', 'gptp-processor'):
        pin = git(root, 'ls-tree', head, '--', name).decode().split()[2]
        assert not (root / name).is_symlink()
        result['submodules'][name] = audit(root / name, pin)
    result['status'] = git(root, 'status', '--porcelain=v1', '--untracked-files=all').decode()
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
    assert result['source']['head'] == head
    for part in [result['source'], *result['submodules'].values()]:
        assert part['head'] == part['expected'] and not part['errors']
    assert not result['status']

if __name__ == '__main__':
    main()
