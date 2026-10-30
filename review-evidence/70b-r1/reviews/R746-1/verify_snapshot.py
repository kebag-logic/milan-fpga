#!/usr/bin/env python3
"""Verify raw tracked bytes, modes, index entries, and initialized gitlinks."""
import hashlib
import os
from pathlib import Path
import subprocess
import sys

def verify(root):
    def git(*args):
        return subprocess.check_output(['git', *args], cwd=root)
    entries = git('ls-tree', '-rz', 'HEAD').split(b'\0')
    expected = {}
    blobs = 0
    for entry in entries:
        if not entry:
            continue
        metadata, rawpath = entry.split(b'\t', 1)
        mode, kind, oid = metadata.split()
        expected[rawpath] = (mode, oid)
        path = root / os.fsdecode(rawpath)
        if kind == b'commit':
            if (path / '.git').exists():
                actual = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=path).strip()
                assert actual == oid, path
                print('gitlink', os.fsdecode(rawpath), oid.decode(), 'initialized')
                verify(path)
            else:
                print('gitlink', os.fsdecode(rawpath), oid.decode(), 'uninitialized; index pin verified')
            continue
        if mode == b'120000':
            assert path.is_symlink(), path
            data = os.fsencode(os.readlink(path))
        else:
            assert path.is_file() and not path.is_symlink(), path
            actual_mode = b'100755' if path.stat().st_mode & 0o111 else b'100644'
            assert actual_mode == mode, path
            data = path.read_bytes()
        digest = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest().encode()
        assert digest == oid, path
        blobs += 1
    index = {}
    for entry in git('ls-files', '-s', '-z').split(b'\0'):
        if entry:
            metadata, rawpath = entry.split(b'\t', 1)
            mode, oid, stage = metadata.split()
            assert stage == b'0', rawpath
            index[rawpath] = (mode, oid)
    assert index == expected, 'index differs from HEAD'
    print('PASS raw blobs/modes/index:', root.name, blobs, 'blobs;', git('rev-parse', 'HEAD', 'HEAD^{tree}').decode().split())

verify(Path(sys.argv[1]).resolve())
