#!/usr/bin/env python3
"""Verify raw tracked bytes, file kinds, executable modes, index, and required pins."""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')
head = '63a187e1579474bca562d85304b9a91466877c33'
required = {'protocol-processor', 'gptp-processor', 'third_party/lwSRP',
            'third_party/tsn-c-stack', 'third_party/verilog-axis'}
def git(at, *args):
    return subprocess.check_output(['git', '-C', str(at), *args], env=env)
def verify(at, revision, recurse=False):
    assert git(at, 'rev-parse', 'HEAD').decode().strip() == revision
    entries = {}
    for rec in git(at, 'ls-tree', '-rz', revision).split(b'\0'):
        if not rec:
            continue
        hdr, name = rec.split(b'\t', 1)
        mode, kind, oid = hdr.split()
        entries[name] = (mode, oid)
        path = at / os.fsdecode(name)
        if kind == b'commit':
            if recurse and os.fsdecode(name) in required:
                verify(path, oid.decode())
            else:
                print('GITLINK', os.fsdecode(name), oid.decode(),
                      'required' if os.fsdecode(name) in required else 'not required')
            continue
        st = path.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(st.st_mode), path
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode), path
            actual_mode = b'100755' if st.st_mode & 0o111 else b'100644'
            assert actual_mode == mode, path
            data = path.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert actual.encode() == oid, path
    index = {}
    for rec in git(at, 'ls-files', '--stage', '-z').split(b'\0'):
        if not rec:
            continue
        hdr, name = rec.split(b'\t', 1)
        mode, oid, stage = hdr.split()
        assert stage == b'0' and name not in index, name
        index[name] = (mode, oid)
    assert index == entries, at
    print('PASS', at.name, revision, 'tree',
          git(at, 'rev-parse', revision + '^{tree}').decode().strip(),
          'tracked entries', len(entries), 'raw bytes/modes/index verified')
verify(root, head, True)
assert git(root, 'rev-parse', 'HEAD^{tree}').decode().strip() == '45c859e17681896f2fa3db26c04de75ef9f125d4'
print('PASS required five submodule checkouts and gitlinks verified')
