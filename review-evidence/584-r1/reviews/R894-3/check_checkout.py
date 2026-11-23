#!/usr/bin/env python3
"""Verify raw working bytes, executable modes, index, and initialized gitlinks."""
import os
from pathlib import Path
import subprocess

HEAD = '599c79af9cfe242bc3d60dd1c80f3e8d57cca12e'
TREE = '718c4adfc7e6cd76aa1b414c18abdcb1b64c291d'

def git(root, *args, data=None):
    return subprocess.check_output(['git', '--no-replace-objects', '-C', str(root), *args], input=data)

def verify(root, rev, top=False):
    root = Path(root)
    assert git(root, 'rev-parse', 'HEAD').decode().strip() == rev
    assert not git(root, 'diff', '--cached', '--raw', rev), 'index differs'
    entries = git(root, 'ls-tree', '-rz', rev).split(b'\0')
    n = 0
    links = []
    for entry in entries:
        if not entry:
            continue
        meta, name = entry.split(b'\t', 1)
        mode, kind, oid = meta.decode().split()
        path = root / os.fsdecode(name)
        if mode == '160000':
            links.append((path, oid))
            continue
        assert path.exists() or path.is_symlink(), name
        if mode == '120000':
            assert path.is_symlink(), name
            raw = os.fsencode(os.readlink(path))
        else:
            assert path.is_file() and not path.is_symlink(), name
            assert bool(path.stat().st_mode & 0o111) == (mode == '100755'), name
            raw = path.read_bytes()
        assert git(root, 'hash-object', '--stdin', data=raw).decode().strip() == oid, name
        n += 1
    print(f'{"superproject" if top else root.name}: {n} tracked blobs and modes match {rev}; index matches')
    for path, oid in links:
        if top and path.name == 'external':
            print(f'external: uninitialized; required gitlink {oid} retained')
            continue
        assert (path/'.git').is_file(), f'not registered submodule: {path.name}'
        verify(path, oid)

assert git('.', 'rev-parse', 'HEAD^{tree}').decode().strip() == TREE
verify('.', HEAD, top=True)
print('PASS: exact source head/tree, raw tracked bytes/modes/index and required submodule gitlinks')
