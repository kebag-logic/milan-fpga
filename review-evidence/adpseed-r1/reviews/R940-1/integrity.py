#!/usr/bin/env python3
"""Verify every tracked byte, file mode, index entry and gitlink at the reviewed head."""
import argparse
import json
from pathlib import Path
import stat
import subprocess

p = argparse.ArgumentParser()
p.add_argument('source', type=Path)
a = p.parse_args()
root = a.source.resolve()
def git(*args):
    return subprocess.check_output(['git', *args], cwd=root)
head = git('rev-parse', 'HEAD').decode().strip()
tree = git('rev-parse', 'HEAD^{tree}').decode().strip()
assert head == '5e6ab995b0c840bb318907642b14d45e8dd0efea'
assert tree == 'b831ac0b6f409a41c0c39ff2e2f0b01551b36bfe'
entries = git('ls-tree', '-rz', 'HEAD').split(b'\0')
expected = {}
gitlinks = {}
for entry in filter(None, entries):
    meta, path = entry.split(b'\t', 1)
    mode, kind, oid = meta.decode().split()
    name = path.decode()
    expected[name] = (mode, oid)
    f = root / name
    if mode == '160000':
        actual = subprocess.check_output(['git', '-C', str(f), 'rev-parse', 'HEAD']).decode().strip()
        assert actual == oid, name
        gitlinks[name] = oid
    else:
        actual = git('hash-object', '--no-filters', name).decode().strip()
        assert actual == oid, name
        s = f.lstat()
        actual_mode = '120000' if stat.S_ISLNK(s.st_mode) else ('100755' if s.st_mode & 0o111 else '100644')
        assert actual_mode == mode, name
index = {}
for entry in filter(None, git('ls-files', '--stage', '-z').split(b'\0')):
    meta, path = entry.split(b'\t', 1)
    mode, oid, stage = meta.decode().split()
    assert stage == '0'
    index[path.decode()] = (mode, oid)
assert index == expected
assert not git('status', '--porcelain', '--untracked-files=all').strip()
print(json.dumps({'head': head, 'tree': tree, 'tracked_entries': len(expected),
                  'tracked_blob_bytes': 'PASS', 'file_modes': 'PASS', 'index': 'PASS',
                  'gitlinks': gitlinks, 'status': 'clean'}, indent=2))
