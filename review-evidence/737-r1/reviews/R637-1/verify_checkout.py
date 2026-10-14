#!/usr/bin/env python3
"""Verify committed bytes, file kinds, executable modes, index and dependency pins."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
head = 'cf9c936697a06e44c41681bcc12dc612a3242eb2'
tree = 'a5eb619c5c9ead508e7189fd77527d84d2c4fdda'
required = {'gptp-processor', 'protocol-processor', 'third_party/lwSRP',
            'third_party/tsn-c-stack', 'third_party/verilog-axis'}
rows = []

def git(directory, *args):
    return subprocess.check_output(['git', '--no-replace-objects', '-C', str(directory), *args])

def check(directory, revision, label):
    assert git(directory, 'rev-parse', 'HEAD').decode().strip() == revision
    entries = git(directory, 'ls-tree', '-rz', revision).split(b'\0')
    wanted_index = {}
    blobs = 0
    links = {}
    for entry in filter(None, entries):
        metadata, rawname = entry.split(b'\t', 1)
        mode, kind, oid = metadata.split()
        name = os.fsdecode(rawname)
        path = directory / name
        wanted_index[rawname] = (mode, oid, b'0')
        if kind == b'commit':
            links[name] = oid.decode()
            populated = (path / '.git').exists()
            if label == '.' and name in required:
                assert populated, name + ': required checkout absent'
            if populated:
                check(path, oid.decode(), name if label == '.' else label + '/' + name)
            continue
        mode_on_disk = path.lstat().st_mode
        if mode == b'120000':
            assert stat.S_ISLNK(mode_on_disk)
            raw = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(mode_on_disk)
            assert bool(mode_on_disk & 0o111) == (mode == b'100755'), name
            raw = path.read_bytes()
        digest = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
        assert digest == oid.decode(), name + ': byte mismatch'
        blobs += 1
    actual_index = {}
    for entry in filter(None, git(directory, 'ls-files', '--stage', '-z').split(b'\0')):
        metadata, name = entry.split(b'\t', 1)
        actual_index[name] = tuple(metadata.split())
    assert actual_index == wanted_index, label + ': index mismatch'
    assert not git(directory, 'ls-files', '--others', '--exclude-standard', '-z'), label + ': untracked files'
    rows.append(dict(checkout=label, head=revision, verified_blobs=blobs, gitlinks=links,
                     bytes_modes_kinds_index='PASS'))

assert git(root, 'rev-parse', 'HEAD^{tree}').decode().strip() == tree
check(root, head, '.')
print(json.dumps({'head': head, 'tree': tree, 'checkouts': rows, 'result': 'PASS'}, indent=2))
