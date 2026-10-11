#!/usr/bin/env python3
"""Verify committed bytes, modes, index entries and required submodule pins."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

HEAD = 'aa980479aafd1d72c72015707fa6618b5aa47cb1'
TREE = 'a7adf20bdededdf76fd4b9fdc9f6b8c820be6082'
REQUIRED = ['protocol-processor', 'gptp-processor', 'third_party/verilog-axis']
ENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')

def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], env=ENV)

def verify(root, commit):
    assert git(root, 'rev-parse', 'HEAD').decode().strip() == commit
    raw = git(root, 'ls-tree', '-rz', commit)
    expected = []
    count = 0
    pins = {}
    for entry in raw.split(b'\0'):
        if not entry:
            continue
        meta, name = entry.split(b'\t', 1)
        mode, kind, oid = meta.split()
        expected.append(mode + b' ' + oid + b' 0\t' + name)
        rel = os.fsdecode(name)
        path = root / rel
        if kind == b'commit':
            pins[rel] = oid.decode()
            continue
        st = path.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(st.st_mode), rel
            content = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode), rel
            assert bool(st.st_mode & 0o111) == (mode == b'100755'), rel
            content = path.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(content)).encode() + b'\0' + content).hexdigest()
        assert actual == oid.decode(), rel
        count += 1
    actual_index = git(root, 'ls-files', '--stage', '-z').rstrip(b'\0').split(b'\0')
    assert sorted(expected) == sorted(actual_index), 'index does not match commit'
    flags = git(root, 'ls-files', '-v', '-z').split(b'\0')
    assert all(not x or x[:1] == b'H' for x in flags), 'hidden index flags'
    return {'head': commit, 'tree': git(root, 'rev-parse', commit + '^{tree}').decode().strip(),
            'verified_blobs': count, 'gitlinks': pins, 'index': 'exact', 'bytes_and_modes': 'exact'}

def main():
    root = Path(sys.argv[1]).resolve()
    result = {'parent': verify(root, HEAD), 'required_submodules': {}}
    assert result['parent']['tree'] == TREE
    for path in REQUIRED:
        pin = result['parent']['gitlinks'][path]
        result['required_submodules'][path] = verify(root / path, pin)
        assert (root / path / '.git').is_file(), path
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
