#!/usr/bin/env python3
"""Check tracked worktree bytes, executable modes, index, and gitlinks."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
root = Path(sys.argv[1]).resolve()
expected = 'e0b144904e57c96928f1dd3fca36a00df42f6ed3'
def git(*args):
    return subprocess.check_output(['git', '-C', str(root), *args])
assert git('rev-parse', 'HEAD').decode().strip() == expected
assert git('rev-parse', 'HEAD^{tree}').decode().strip() == '2b5890f3cbb82b2415f7fa50151db3acc550e282'
rows, links = [], []
for record in git('ls-tree', '-rz', 'HEAD').split(b'\0'):
    if not record:
        continue
    meta, name = record.split(b'\t', 1)
    mode, kind, oid = meta.decode().split()
    name = os.fsdecode(name)
    if mode == '160000':
        links.append([name, oid])
        assert subprocess.check_output(['git', '-C', str(root/name), 'rev-parse', 'HEAD']).decode().strip() == oid
        continue
    path = root / name
    data = os.readlink(path).encode() if mode == '120000' else path.read_bytes()
    digest = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    assert digest == oid, name
    if mode != '120000':
        assert bool(path.stat().st_mode & 0o111) == (mode == '100755'), name
    rows.append([mode, oid, name])
subprocess.run(['git', '-C', str(root), 'diff', '--quiet', 'HEAD', '--'], check=True)
assert git('write-tree').decode().strip() == '2b5890f3cbb82b2415f7fa50151db3acc550e282'
print(json.dumps({'head': expected, 'tree': '2b5890f3cbb82b2415f7fa50151db3acc550e282', 'tracked_blob_count': len(rows), 'tracked_bytes_modes_index': 'PASS', 'gitlinks': links, 'status': git('status', '--porcelain').decode()}, indent=2))
