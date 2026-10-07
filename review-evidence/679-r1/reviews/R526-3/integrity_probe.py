#!/usr/bin/env python3
"""Prove tracked bytes, modes, stage-zero index entries and required gitlinks."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

ROOT = Path.cwd()
ENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')
HEAD = 'af5be4710c3516cc247c353213d6939fa8d23f57'
REQUIRED = ['protocol-processor', 'gptp-processor', 'third_party/verilog-axis']

def git(root, *args):
    return subprocess.check_output(['git', '-c', 'core.commitGraph=false', '-C', str(root), *args], env=ENV)

def verify(root, revision):
    assert git(root, 'rev-parse', 'HEAD').decode().strip() == revision
    entries = {}
    for row in git(root, 'ls-tree', '-rz', revision).split(b'\0'):
        if row:
            header, name = row.split(b'\t', 1)
            mode, kind, oid = header.decode().split()
            entries[os.fsdecode(name)] = (mode, kind, oid)
    indexed = {}
    for row in git(root, 'ls-files', '--stage', '-z').split(b'\0'):
        if row:
            header, name = row.split(b'\t', 1)
            mode, oid, stage = header.decode().split()
            assert stage == '0'
            name = os.fsdecode(name)
            assert name not in indexed
            indexed[name] = (mode, oid)
    assert indexed == {p:(m,h) for p,(m,k,h) in entries.items()}
    records = []
    for name, (mode, kind, oid) in sorted(entries.items()):
        if kind == 'commit':
            continue
        path = root / name
        metadata = path.lstat()
        if mode == '120000':
            assert stat.S_ISLNK(metadata.st_mode), name
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(metadata.st_mode), name
            assert mode == ('100755' if metadata.st_mode & 0o111 else '100644'), name
            data = path.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert actual == oid, name
        records.append([name, mode, oid, hashlib.sha256(data).hexdigest()])
    digest = hashlib.sha256(json.dumps(records, separators=(',',':')).encode()).hexdigest()
    return entries, {'head': revision, 'tracked_blobs': len(records), 'tracked_entries': len(entries), 'bytes_modes_sha256': digest, 'index_equals_tree': True}

entries, summary = verify(ROOT, HEAD)
print('superproject:', json.dumps(summary, sort_keys=True))
for sub in REQUIRED:
    mode, kind, pin = entries[sub]
    assert (mode, kind) == ('160000', 'commit')
    checkout = ROOT / sub
    assert checkout.is_dir() and not checkout.is_symlink()
    assert (checkout / '.git').is_file()
    assert git(checkout, 'rev-parse', '--show-superproject-working-tree').decode().strip() == str(ROOT)
    _, receipt = verify(checkout, pin)
    print(sub + ':', json.dumps(receipt, sort_keys=True))
print('external gitlink retained but not initialized; outside required validation population:', entries['external'][2])
assert not git(ROOT, 'status', '--porcelain').strip()
print('Final tracked blob bytes, modes, index and required submodule gitlinks: PASS')
