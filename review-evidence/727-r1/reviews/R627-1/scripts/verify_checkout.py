#!/usr/bin/env python3
"""Verify raw tracked bytes, modes and index against the review commit and pins."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

p = argparse.ArgumentParser()
p.add_argument('repo', type=Path)
p.add_argument('packet', type=Path)
a = p.parse_args()
repo, packet = a.repo.resolve(), a.packet.resolve()
expected = 'a57d384dc697249c2a69f80079b676875d4f7560'
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')

def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], env=env)

def audit(root, ref):
    entries = {}
    for record in git(root, 'ls-tree', '-rz', ref).split(b'\0'):
        if record:
            header, path = record.split(b'\t', 1)
            mode, kind, oid = header.split()
            entries[path] = (mode, kind, oid)
    index = {}
    for record in git(root, 'ls-files', '--stage', '-z').split(b'\0'):
        if record:
            header, path = record.split(b'\t', 1)
            mode, oid, stage = header.split()
            assert stage == b'0' and path not in index, (root, path, stage)
            index[path] = (mode, oid)
    assert index == {path: (mode, oid) for path, (mode, kind, oid) in entries.items()}, 'index differs'
    checked, links = 0, {}
    for rawpath, (mode, kind, oid) in entries.items():
        path = root / os.fsdecode(rawpath)
        if kind == b'commit':
            links[os.fsdecode(rawpath)] = oid.decode()
            continue
        s = path.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(s.st_mode), path
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(s.st_mode), path
            assert bool(s.st_mode & 0o111) == (mode == b'100755'), path
            data = path.read_bytes()
        digest = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert digest == oid.decode(), path
        checked += 1
    return {'tracked_blobs_checked': checked, 'index_matches_tree': True, 'gitlinks': links}

assert git(repo, 'rev-parse', 'HEAD').decode().strip() == expected
assert git(repo, 'rev-parse', 'HEAD^{tree}').decode().strip() == 'a2fada192e36369be7fb6202c8f9618021c31c77'
result = {'head': expected, 'tree': 'a2fada192e36369be7fb6202c8f9618021c31c77', 'parent': audit(repo, expected), 'submodules': {}}
for name in ('third_party/verilog-axis', 'protocol-processor', 'gptp-processor'):
    pin = result['parent']['gitlinks'][name]
    root = repo / name
    assert (root / '.git').is_file() and not root.is_symlink(), name
    assert git(root, 'rev-parse', 'HEAD').decode().strip() == pin, name
    record = audit(root, pin)
    record['head'] = pin
    record['registered_gitdir'] = (root / '.git').read_text().startswith('gitdir: ')
    result['submodules'][name] = record
assert git(repo, 'status', '--porcelain', '--untracked-files=no') == b''
result['workflow_unchanged'] = git(repo, 'rev-parse', 'c6bd08c6:.github/workflows/rtl.yml') == git(repo, 'rev-parse', expected + ':.github/workflows/rtl.yml')
result['driver_unchanged'] = git(repo, 'rev-parse', 'c6bd08c6:scripts/run_all_suites.sh') == git(repo, 'rev-parse', expected + ':scripts/run_all_suites.sh')
assert result['workflow_unchanged'] and result['driver_unchanged']
(packet / 'receipts/checkout-integrity.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
