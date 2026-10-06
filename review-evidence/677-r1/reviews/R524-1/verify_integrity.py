#!/usr/bin/env python3
"""Prove tracked bytes, kinds, modes, index entries, flags and required gitlinks."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

HEAD = '6c94e9f5f496ac25f8c4e31f9e3685c725de29f3'
TREE = '25b32c793bd4bb6d959640094a44fb2b5c9d7a45'
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], env=env)


def inspect(root, rev):
    expected = {}
    for row in git(root, 'ls-tree', '-rz', rev).split(b'\0'):
        if row:
            meta, name = row.split(b'\t', 1)
            mode, kind, oid = meta.decode().split()
            expected[name] = (mode, kind, oid)
    index = {}
    for row in git(root, 'ls-files', '--stage', '-z').split(b'\0'):
        if row:
            meta, name = row.split(b'\t', 1)
            mode, oid, stage = meta.decode().split()
            assert stage == '0', (name, 'unmerged')
            assert name not in index
            index[name] = (mode, oid)
    assert index == {k: (v[0], v[2]) for k, v in expected.items()}, 'index mismatch'
    flags = git(root, 'ls-files', '-v', '-z').split(b'\0')
    assert all(not x or x[:1] == b'H' for x in flags), 'hidden index flags'
    count = 0
    for name, (mode, kind, oid) in expected.items():
        if mode == '160000':
            continue
        path = root / os.fsdecode(name)
        s = path.lstat()
        if mode == '120000':
            assert stat.S_ISLNK(s.st_mode), name
            raw = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(s.st_mode), name
            assert bool(s.st_mode & 0o111) == (mode == '100755'), name
            raw = path.read_bytes()
        got = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
        assert got == oid, ('blob mismatch', name)
        count += 1
    return expected, count


root = Path.cwd().resolve()
assert git(root, 'rev-parse', 'HEAD').decode().strip() == HEAD
assert git(root, 'rev-parse', 'HEAD^{tree}').decode().strip() == TREE
expected, count = inspect(root, HEAD)
report = {'head': HEAD, 'tree': TREE, 'tracked_blobs_verified': count,
          'index_matches_tree': True, 'bytes_modes_kinds_verified': True,
          'no_hidden_index_flags': True, 'required_submodules': []}
for name in ('protocol-processor', 'gptp-processor', 'third_party/verilog-axis'):
    mode, kind, pin = expected[name.encode()]
    assert mode == '160000' and kind == 'commit'
    sub = root / name
    assert (sub / '.git').is_file(), 'not a registered submodule'
    assert git(sub, 'rev-parse', 'HEAD').decode().strip() == pin
    assert git(sub, 'rev-parse', '--show-superproject-working-tree').decode().strip() == str(root)
    _, subcount = inspect(sub, pin)
    report['required_submodules'].append({'path': name, 'pin': pin, 'blobs_verified': subcount})
report['other_gitlinks'] = [{'path': os.fsdecode(k), 'pin': v[2]} for k, v in expected.items()
                          if v[0] == '160000' and os.fsdecode(k) not in
                          ('protocol-processor', 'gptp-processor', 'third_party/verilog-axis')]
out = Path(__file__).resolve().parent / sys.argv[1]
out.write_text(json.dumps(report, indent=2) + '\n')
print(out.name, json.dumps(report))
