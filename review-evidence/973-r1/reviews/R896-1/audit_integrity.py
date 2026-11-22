#!/usr/bin/env python3
"""Verify tracked bytes, file kinds, modes, index, and required gitlinks."""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys

ROOT = Path.cwd()
HEAD = '9a71daa9aa2379e2a57eb93ccafe83101bcb37f7'
TREE = '0fe791d5c539f4100e312f17e469a2a9a50bc006'
os.environ['GIT_NO_REPLACE_OBJECTS'] = '1'


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args])


def verify(root, rev):
    entries = git(root, 'ls-tree', '-rz', rev).split(b'\0')
    expected = []
    count = 0
    for entry in filter(None, entries):
        metadata, name = entry.split(b'\t', 1)
        mode, kind, oid = metadata.split()
        expected.append(mode + b' ' + oid + b' 0\t' + name)
        if kind == b'commit':
            continue
        path = root / os.fsdecode(name)
        info = path.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(info.st_mode), name
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(info.st_mode), name
            assert bool(info.st_mode & 0o111) == (mode == b'100755'), name
            data = path.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest().encode()
        assert actual == oid, name
        count += 1
    index = git(root, 'ls-files', '--stage', '-z').split(b'\0')
    assert sorted(filter(None, index)) == sorted(expected), 'index differs from tree'
    print(root.relative_to(ROOT) or '.', rev, count, 'tracked blobs: bytes/kinds/modes/index PASS')


assert git(ROOT, 'rev-parse', 'HEAD').decode().strip() == HEAD
assert git(ROOT, 'rev-parse', 'HEAD^{tree}').decode().strip() == TREE
verify(ROOT, HEAD)
for name in ('protocol-processor', 'gptp-processor', 'third_party/verilog-axis', 'third_party/tsn-c-stack', 'third_party/lwSRP'):
    pin = git(ROOT, 'rev-parse', HEAD + ':' + name).decode().strip()
    sub = ROOT / name
    assert not sub.is_symlink()
    assert (sub / '.git').is_file(), name
    assert git(sub, 'rev-parse', 'HEAD').decode().strip() == pin, name
    verify(sub, pin)
for name in ('sw/firmware/ctrl/loop/ctrl_loop.c', 'sw/firmware/ctrl/loop/ctrl_loop.h', 'sw/firmware/gtest/coverage.ratchet'):
    assert git(ROOT, 'show', 'dd163e41:' + name) == git(ROOT, 'show', HEAD + ':' + name)
    print(name, 'byte-identical to base PASS')
print('External optional submodule not initialized; outside required population.')
print('Exact head and tree confirmed; no source changes made by review.')
