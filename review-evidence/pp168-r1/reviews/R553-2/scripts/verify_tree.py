#!/usr/bin/env python3
"""Verify exact tracked bytes, modes, index and all recursive gitlinks."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

HEAD = '66d1b501f4879402fe76485095aef7c6e07c32af'
TREE = '36e735c0d54ceb20f2ca09f4ed07069e575a9717'
root = Path(sys.argv[1]).resolve()
def git(*args):
    return subprocess.check_output(['git', '-C', str(root), *args])
assert git('rev-parse', 'HEAD').decode().strip() == HEAD
assert git('rev-parse', 'HEAD^{tree}').decode().strip() == TREE
assert git('write-tree').decode().strip() == TREE
assert not git('diff', '--raw', 'HEAD')
records = []
gitlinks = []
for entry in git('ls-tree', '-rz', 'HEAD').split(b'\0'):
    if not entry:
        continue
    meta, name = entry.split(b'\t', 1)
    mode, typ, oid = meta.decode().split()
    path = root / os.fsdecode(name)
    if typ == 'commit':
        got = subprocess.check_output(['git', '-C', str(path), 'rev-parse', 'HEAD']).decode().strip()
        assert got == oid, str(path)
        gitlinks.append({'path': os.fsdecode(name), 'oid': oid})
        continue
    data = os.fsencode(os.readlink(path)) if mode == '120000' else path.read_bytes()
    actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    assert actual == oid, os.fsdecode(name)
    smode = path.lstat().st_mode
    expected_mode = '120000' if stat.S_ISLNK(smode) else ('100755' if smode & 0o111 else '100644')
    assert mode == expected_mode, os.fsdecode(name)
    records.append({'path': os.fsdecode(name), 'mode': mode, 'blob': actual})
print(json.dumps({'head': HEAD, 'tree': TREE, 'index_tree': TREE,
                  'tracked_blob_count': len(records), 'gitlinks': gitlinks,
                  'status_porcelain': git('status', '--porcelain=v1').decode(),
                  'verified': records}, indent=2))
