#!/usr/bin/env python3
"""Verify raw tracked bytes, types, executable modes, index and submodule pins."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

root = Path(os.environ['REVIEW_ROOT'])
expected = 'cd3525c3ddcbdb5d78bf8fccdab354c468926997'
required = {'gptp-processor', 'protocol-processor', 'third_party/lwSRP',
            'third_party/tsn-c-stack', 'third_party/verilog-axis'}
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')

def git(where, *args):
    return subprocess.check_output(['git', '-C', str(where), *args], env=env)

def check(where, rev, submodules=False):
    head = git(where, 'rev-parse', 'HEAD').decode().strip()
    assert head == rev, (where.name, head, rev)
    tree = git(where, 'rev-parse', rev + '^{tree}').decode().strip()
    entries = git(where, 'ls-tree', '-rz', rev).split(b'\0')
    expected_index = []
    count = 0
    subs = {}
    for entry in filter(None, entries):
        info, name = entry.split(b'\t', 1)
        mode, kind, oid = info.split()
        expected_index.append(mode + b' ' + oid + b' 0\t' + name)
        path = where / os.fsdecode(name)
        if kind == b'commit':
            if submodules and os.fsdecode(name) in required:
                assert (path / '.git').is_file(), name
                subs[os.fsdecode(name)] = check(path, oid.decode())
            continue
        st = path.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(st.st_mode), name
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode), name
            actual_mode = b'100755' if st.st_mode & 0o111 else b'100644'
            assert actual_mode == mode, (name, mode, actual_mode)
            data = path.read_bytes()
        actual_oid = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest().encode()
        assert actual_oid == oid, name
        count += 1
    actual_index = git(where, 'ls-files', '--stage', '-z').split(b'\0')
    assert sorted(filter(None, actual_index)) == sorted(expected_index), where.name
    return {'head': head, 'tree': tree, 'verified_blobs': count, 'raw_bytes_modes_index': 'PASS',
            'submodules': subs}

print(json.dumps(check(root, expected, True), indent=2))
