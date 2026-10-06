#!/usr/bin/env python3
"""Prove raw tracked bytes, executable modes, stage-zero index and required pins."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

ROOT = Path(sys.argv[1]).resolve()
EXPECTED = '4dab80ae4564ef8d6e1030564dcea4ba19235ee6'
PINS = {
    'protocol-processor': 'ead8036035affd53ef4b29979190f2f4f67084c0',
    'gptp-processor': '5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d',
    'third_party/verilog-axis': '48ff7a7e2ef782cf778d47910cf85835c64b1bce',
}
ENV = {**os.environ, 'GIT_NO_REPLACE_OBJECTS': '1', 'GIT_OPTIONAL_LOCKS': '0'}


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], env=ENV)


def inspect(root, head, label):
    assert git(root, 'rev-parse', 'HEAD').decode().strip() == head
    assert Path(git(root, 'rev-parse', '--show-toplevel').decode().strip()).resolve() == root
    entries = {}
    for record in git(root, 'ls-tree', '-rz', head).split(b'\0'):
        if not record:
            continue
        meta, path = record.split(b'\t', 1)
        mode, kind, oid = meta.split()
        entries[path] = (mode, oid)
        if kind == b'commit':
            continue
        file = root / os.fsdecode(path)
        status = file.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(status.st_mode), path
            data = os.fsencode(os.readlink(file))
        else:
            assert stat.S_ISREG(status.st_mode), path
            actual_mode = b'100755' if status.st_mode & 0o111 else b'100644'
            assert actual_mode == mode, path
            data = file.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest().encode()
        assert actual == oid, path
    index = {}
    for record in git(root, 'ls-files', '--stage', '-z').split(b'\0'):
        if not record:
            continue
        meta, path = record.split(b'\t', 1)
        mode, oid, stage = meta.split()
        assert stage == b'0' and path not in index, path
        index[path] = (mode, oid)
    assert entries == index, label
    print(json.dumps({'repository': label, 'head': head, 'tree': git(root, 'rev-parse', head + '^{tree}').decode().strip(), 'tracked_entries': len(entries), 'raw_blobs_modes_index': 'PASS'}))
    return entries


root_entries = inspect(ROOT, EXPECTED, 'candidate')
for path, pin in PINS.items():
    assert root_entries[path.encode()] == (b'160000', pin.encode())
    sub = ROOT / path
    assert sub.is_dir() and not sub.is_symlink() and (sub / '.git').is_file()
    superproject = git(sub, 'rev-parse', '--show-superproject-working-tree').decode().strip()
    assert Path(superproject).resolve() == ROOT
    inspect(sub, pin, path)
print('PASS: candidate and all three required initialized submodules match raw tracked bytes, modes, index, and gitlinks')
