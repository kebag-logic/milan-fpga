#!/usr/bin/env python3
"""Prove tracked bytes, modes, index and required submodule pins directly."""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
head = '394612c55148b43354359daeab2aa88d4f019ec2'
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')
def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args], env=env)
def verify(repo, ref):
    entries = {}
    for entry in git(repo, 'ls-tree', '-rz', ref).split(b'\0'):
        if not entry:
            continue
        meta, name = entry.split(b'\t', 1)
        mode, kind, oid = meta.decode().split()
        name = name.decode()
        entries[name] = (mode, oid)
        if kind == 'commit':
            continue
        p = repo / name
        s = p.lstat()
        if mode == '120000':
            assert stat.S_ISLNK(s.st_mode), name
            data = os.fsencode(os.readlink(p))
        else:
            assert stat.S_ISREG(s.st_mode), name
            assert bool(s.st_mode & 0o111) == (mode == '100755'), name
            data = p.read_bytes()
        digest = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert digest == oid, name
    index = {}
    for entry in git(repo, 'ls-files', '--stage', '-z').split(b'\0'):
        if not entry:
            continue
        meta, name = entry.split(b'\t', 1)
        mode, oid, stage = meta.decode().split()
        assert stage == '0'
        index[name.decode()] = (mode, oid)
    assert index == entries
    return entries
assert git(root, 'rev-parse', 'HEAD').decode().strip() == head
entries = verify(root, head)
print('Superproject', head, 'tree', git(root, 'rev-parse', 'HEAD^{tree}').decode().strip(), len(entries), 'entries: bytes/modes/index PASS')
for path in ('protocol-processor', 'gptp-processor', 'third_party/verilog-axis', 'third_party/tsn-c-stack', 'third_party/lwSRP'):
    mode, oid = entries[path]
    assert mode == '160000'
    sub = root / path
    assert (sub / '.git').is_file() and not sub.is_symlink()
    assert git(sub, 'rev-parse', 'HEAD').decode().strip() == oid
    checked = verify(sub, oid)
    print(path, oid, len(checked), 'entries: bytes/modes/index PASS')
print('External submodule is uninitialized and unused; its recorded gitlink is unchanged.')
print('Tracked checkout integrity: PASS')
