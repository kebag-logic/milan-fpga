#!/usr/bin/env python3
"""Verify HEAD, index entries and raw checkout bytes/modes, including required gitlinks."""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
expected = '8aeb2f0bb9bfad9c486a0abf9dbeaf134d3de2fb'
def git(directory, *args):
    return subprocess.check_output(['git', '-C', str(directory), *args], env={**os.environ, 'GIT_NO_REPLACE_OBJECTS': '1'})
assert git(root, 'rev-parse', 'HEAD').decode().strip() == expected
assert git(root, 'rev-parse', 'HEAD^{tree}').decode().strip() == 'f00413b5354577dded4c76c4098b01bd6c8002bd'
required = {'protocol-processor', 'gptp-processor', 'third_party/verilog-axis', 'third_party/tsn-c-stack', 'third_party/lwSRP'}
def verify(directory, commit, recurse=False):
    records = {}
    for entry in git(directory, 'ls-tree', '-rz', commit).split(b'\0'):
        if not entry:
            continue
        meta, name = entry.split(b'\t', 1)
        mode, kind, oid = meta.split()
        records[name] = (mode, oid)
        path = directory / os.fsdecode(name)
        if kind == b'commit':
            if recurse and os.fsdecode(name) in required:
                assert (path / '.git').is_file(), f'Unregistered submodule: {name!r}'
                assert git(path, 'rev-parse', 'HEAD').strip() == oid
                verify(path, oid.decode())
            continue
        info = path.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(info.st_mode), name
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(info.st_mode), name
            actual_mode = b'100755' if info.st_mode & 0o111 else b'100644'
            assert actual_mode == mode, name
            data = path.read_bytes()
        digest = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest().encode()
        assert digest == oid, name
    index = {}
    for entry in git(directory, 'ls-files', '--stage', '-z').split(b'\0'):
        if not entry:
            continue
        meta, name = entry.split(b'\t', 1)
        mode, oid, stage = meta.split()
        assert stage == b'0' and name not in index, name
        index[name] = (mode, oid)
    assert index == records, 'Index differs from commit'
    print(f'{directory.name}: {len(records)} tracked entries match raw bytes, modes and index at {commit}')
verify(root, expected, True)
print('Exact head/tree and all five required registered submodules verified. External submodule not used.')
