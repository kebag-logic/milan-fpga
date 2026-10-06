#!/usr/bin/env python3
"""Verify committed bytes, executable modes, index entries and required pins."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

HEAD = '8fb296e3e02985aee27ef04cb08278836b734a14'
TREE = 'ce846f8ab472d3c9bf605598224ae2521966d928'
REQUIRED = {'protocol-processor', 'gptp-processor', 'third_party/verilog-axis'}

def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args],
                                   env={**os.environ, 'GIT_NO_REPLACE_OBJECTS': '1'})

def verify(root, revision, label):
    assert git(root, 'rev-parse', 'HEAD').decode().strip() == revision
    expected = {}
    count = 0
    pins = []
    for record in git(root, 'ls-tree', '-rz', '--full-tree', revision).split(b'\0'):
        if not record:
            continue
        meta, raw_path = record.split(b'\t', 1)
        mode, kind, oid = meta.decode().split()
        name = os.fsdecode(raw_path)
        expected[name] = (mode, oid, '0')
        path = root / name
        if kind == 'commit':
            pins.append({'path': name, 'oid': oid, 'required': name in REQUIRED})
            if name in REQUIRED:
                assert path.is_dir() and not path.is_symlink(), name
                assert (path / '.git').is_file(), name
                verify(path, oid, name)
            continue
        st = path.lstat()
        if mode == '120000':
            assert stat.S_ISLNK(st.st_mode), name
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode), name
            actual_mode = '100755' if st.st_mode & 0o111 else '100644'
            assert actual_mode == mode, (name, mode, actual_mode)
            data = path.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert actual == oid, (name, oid, actual)
        count += 1
    index = {}
    for record in git(root, 'ls-files', '--stage', '-z').split(b'\0'):
        if record:
            meta, name = record.split(b'\t', 1)
            assert os.fsdecode(name) not in index, 'duplicate/unmerged index entry'
            index[os.fsdecode(name)] = tuple(meta.decode().split())
    assert index == expected, 'index differs from committed tree'
    flags = git(root, 'ls-files', '-v', '-z').split(b'\0')
    assert all(not f or f[:1] == b'H' for f in flags), 'hidden/sparse index flag'
    assert not git(root, 'diff', '--no-ext-diff', '--exit-code'), 'worktree diff'
    print(json.dumps({'population': label, 'head': revision, 'blobs_verified': count,
                      'index_entries_verified': len(index), 'gitlinks': pins, 'result': 'PASS'}))

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('repo', type=Path)
    args = ap.parse_args()
    root = args.repo.resolve()
    assert git(root, 'rev-parse', 'HEAD^{tree}').decode().strip() == TREE
    branch = subprocess.run(['git', '-C', str(root), 'symbolic-ref', '-q', 'HEAD'], capture_output=True)
    assert branch.returncode == 1, 'candidate must remain detached'
    verify(root, HEAD, 'candidate')
    status = git(root, 'status', '--porcelain=v1', '--untracked-files=all').decode()
    assert not status, status
    print('PASS: exact head/tree, all tracked blob bytes and modes, complete indexes, required gitlinks, clean status')

if __name__ == '__main__':
    main()
