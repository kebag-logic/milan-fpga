#!/usr/bin/env python3
"""Compare raw tracked bytes, modes and the complete index against each pinned tree."""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
head = '85569e241625d8e4176aae7d77c524783dff30cd'
tree = '89dc2ac457b7506fe6e76e877f8635bf757101a5'
def git(where, *args):
    return subprocess.check_output(['git', *args], cwd=where)
def inspect(where, expected, label):
    assert git(where, 'rev-parse', 'HEAD').decode().strip() == expected, label + ' head'
    entries = {}
    for record in git(where, 'ls-tree', '-rz', expected).split(b'\0'):
        if not record: continue
        meta, path = record.split(b'\t', 1)
        mode, kind, oid = meta.split()
        entries[path] = (mode, kind, oid)
    index = {}
    for record in git(where, 'ls-files', '--stage', '-z').split(b'\0'):
        if not record: continue
        meta, path = record.split(b'\t', 1)
        mode, oid, stage = meta.split()
        assert stage == b'0', label + ' unresolved index'
        index[path] = (mode, oid)
    assert index == {p: (mode, oid) for p, (mode, _, oid) in entries.items()}, label + ' index'
    count = 0
    for path, (mode, kind, oid) in entries.items():
        if kind != b'blob': continue
        full = where / os.fsdecode(path)
        sm = full.lstat().st_mode
        if mode == b'120000':
            assert stat.S_ISLNK(sm), label + ' symlink mode'
            data = os.fsencode(os.readlink(full))
        else:
            assert stat.S_ISREG(sm), label + ' regular file mode'
            assert bool(sm & 0o111) == (mode == b'100755'), label + ' executable mode'
            data = full.read_bytes()
        got = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest().encode()
        assert got == oid, label + ' blob ' + repr(path)
        count += 1
    print('PASS', label, expected, 'blobs', count, 'raw bytes/modes/index')
    return entries

assert git(root, 'rev-parse', 'HEAD^{tree}').decode().strip() == tree
entries = inspect(root, head, 'superproject')
for path in ('protocol-processor', 'gptp-processor', 'third_party/verilog-axis', 'third_party/tsn-c-stack',
             'third_party/lwSRP'):
    mode, kind, pin = entries[path.encode()]
    assert mode == b'160000' and kind == b'commit'
    sub = root / path
    assert (sub / '.git').is_file(), 'registered submodule ' + path
    assert git(sub, 'rev-parse', '--show-superproject-working-tree').decode().strip() == str(root)
    inspect(sub, pin.decode(), path)
print('STATUS', git(root, 'status', '--porcelain=v1', '--untracked-files=no').decode().strip() or 'clean')
print('External optional gitlink preserved; its uninitialized checkout was not required or executed.')
print('RESULT PASS')
