#!/usr/bin/env python3
"""Verify committed blob bytes, modes, index entries and required gitlinks."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

HEAD = '9c601b5983acfd60fb269b9a88c27b48cab7cf65'
TREE = 'd2337a496fb13813beb2f4a13aefcaca0e0a94db'
REQUIRED = ['protocol-processor', 'gptp-processor', 'third_party/verilog-axis']

def verify(root, expected):
    def git(*args):
        return subprocess.check_output(['git', '-C', str(root), *args],
                                       env=os.environ | {'GIT_NO_REPLACE_OBJECTS': '1'})
    head = git('rev-parse', 'HEAD').decode().strip()
    assert head == expected
    tree = git('rev-parse', 'HEAD^{tree}').decode().strip()
    if expected == HEAD:
        assert tree == TREE
    entries = {}
    for line in git('ls-tree', '-rz', '--full-tree', expected).split(b'\0'):
        if line:
            attrs, path = line.split(b'\t', 1)
            mode, kind, oid = attrs.decode().split()
            entries[os.fsdecode(path)] = (mode, kind, oid)
    index = {}
    for line in git('ls-files', '--stage', '-z').split(b'\0'):
        if line:
            attrs, path = line.split(b'\t', 1)
            mode, oid, stage = attrs.decode().split()
            assert stage == '0'
            index[os.fsdecode(path)] = (mode, oid)
    assert index == {p: (m, o) for p, (m, _, o) in entries.items()}
    blobs = 0
    links = {}
    for path, (mode, kind, oid) in entries.items():
        p = root / path
        if mode == '160000':
            links[path] = oid
            continue
        st = p.lstat()
        if mode == '120000':
            assert stat.S_ISLNK(st.st_mode), path
            raw = os.fsencode(os.readlink(p))
        else:
            assert stat.S_ISREG(st.st_mode), path
            actual = '100755' if st.st_mode & 0o111 else '100644'
            assert mode == actual, path
            raw = p.read_bytes()
        assert hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest() == oid, path
        blobs += 1
    return {'head': head, 'tree': tree, 'blobs_verified': blobs,
            'index_entries_verified': len(index), 'gitlinks': links, 'result': 'PASS'}

def main():
    root = Path(sys.argv[1]).resolve()
    result = {'parent': verify(root, HEAD), 'required_submodules': {}}
    for path in REQUIRED:
        assert (root / path / '.git').is_file(), path
        result['required_submodules'][path] = verify(root / path, result['parent']['gitlinks'][path])
    result['optional_external'] = 'Unused and uninitialized; recorded gitlink verified only.'
    out = Path(__file__).resolve().parent / 'checkout-integrity.json'
    out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
