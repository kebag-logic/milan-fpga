#!/usr/bin/env python3
"""Verify the two-commit delta and exact tracked bytes without trusting status."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

HEAD = '26e2748f47b0d8fa533f53203264d9f31fc13c48'
TREE = 'b93fd1d39c06c069c01aa8ceeeb74fbb6083472e'
OLD = 'aa980479aafd1d72c72015707fa6618b5aa47cb1'
BASE = 'c6bd08c6f52632c6d33d834ce842ac3cf63f29cc'
MERGE = 'b075a994f6daae3b406bce415a837b7c401712d5'
PLAN = 'docs/design/MARK_II_AREA_PLAN.md'
ROOT = Path(sys.argv[1]).resolve()
ENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')

def git(*args, root=ROOT):
    return subprocess.check_output(['git', '-C', str(root), *args], env=ENV)

def tree(rev, root=ROOT):
    result = {}
    for row in git('ls-tree', '-rz', rev, root=root).split(b'\0'):
        if row:
            metadata, path = row.split(b'\t', 1)
            mode, kind, oid = metadata.decode().split()
            result[os.fsdecode(path)] = (mode, kind, oid)
    return result

def verify_checkout(root, rev):
    entries = tree(rev, root)
    index = {}
    for row in git('ls-files', '--stage', '-z', root=root).split(b'\0'):
        if row:
            metadata, path = row.split(b'\t', 1)
            mode, oid, stage = metadata.decode().split()
            assert stage == '0', (path, stage)
            index[os.fsdecode(path)] = (mode, 'commit' if mode == '160000' else 'blob', oid)
    assert entries == index, f'index differs from {rev}'
    n = 0
    for name, (mode, kind, oid) in entries.items():
        if kind == 'commit':
            continue
        path = root / name
        info = path.lstat()
        if mode == '120000':
            assert stat.S_ISLNK(info.st_mode), name
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(info.st_mode), name
            assert bool(info.st_mode & 0o111) == (mode == '100755'), name
            data = path.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert actual == oid, name
        n += 1
    return n

assert git('rev-parse', 'HEAD').decode().strip() == HEAD
assert git('rev-parse', 'HEAD^{tree}').decode().strip() == TREE
assert git('rev-list', '--first-parent', f'{OLD}..{HEAD}').decode().split() == [HEAD, MERGE]
assert git('show', '-s', '--format=%P', MERGE).decode().split() == [OLD, BASE]
auto = git('merge-tree', '--write-tree', OLD, BASE).decode().strip()
assert auto == git('rev-parse', f'{MERGE}^{{tree}}').decode().strip()
assert git('diff', '--name-only', MERGE, HEAD).decode().splitlines() == [PLAN]
assert git('diff', '--numstat', MERGE, HEAD).decode().strip() == f'3\t3\t{PLAN}'
print('PASS: exactly two lane commits, automatic merge tree', auto)
print('PASS: subsequent change is exactly three removed and three added plan lines')

old = tree(OLD)
head = tree(HEAD)
lane = git('diff', '--name-only', BASE, HEAD).decode().splitlines()
assert len(lane) == 17
assert [p for p in lane if old.get(p) != head.get(p)] == [PLAN]
print('PASS: all 16 other PR-delta paths are byte/mode/object-identical to aa980479')
for p in lane:
    print(p, *head[p], 'UNCHANGED' if old.get(p) == head[p] else 'MERGED PLAN')

print('PASS: parent tracked blob bytes, modes and index:', verify_checkout(ROOT, HEAD))
for name in ['protocol-processor', 'gptp-processor', 'third_party/verilog-axis']:
    mode, kind, pin = head[name]
    assert (mode, kind) == ('160000', 'commit')
    sub = ROOT / name
    assert (sub / '.git').is_file(), name
    assert git('rev-parse', 'HEAD', root=sub).decode().strip() == pin
    assert Path(git('rev-parse', '--show-superproject-working-tree', root=sub).decode().strip()).resolve() == ROOT
    print('PASS: required submodule', name, pin, 'tracked blobs', verify_checkout(sub, pin))

baseline = json.loads((ROOT / 'syn/ooc/pp_resource_baseline.json').read_text())
for name, endpoint in baseline['endpoints'].items():
    print('RECORD', name, json.dumps(endpoint['record']['figures'], sort_keys=True))
print('PASS: exact checkout and required gitlinks verified')
