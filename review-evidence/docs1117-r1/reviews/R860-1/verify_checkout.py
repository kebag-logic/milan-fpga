#!/usr/bin/env python3
"""Compare raw tracked bytes, executable modes, index, and gitlinks to HEAD."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')
def git(*args):
    return subprocess.check_output(['git', *args], cwd=root, env=env)
head = git('rev-parse', 'HEAD').decode().strip()
assert head == 'ee5c6f922a5863e25cef5bbc5f37289acf4e4777'
tree = git('rev-parse', 'HEAD^{tree}').decode().strip()
assert tree == '6c9fce3f9da97088789783556f38aac79a288d4c'
entries = {}
gitlinks = []
blobs = 0
for row in git('ls-tree', '-rz', '--full-tree', 'HEAD').split(b'\0'):
    if not row:
        continue
    meta, path = row.split(b'\t', 1)
    mode, kind, oid = meta.split()
    entries[path] = (mode, oid)
    file = root / os.fsdecode(path)
    if mode == b'160000':
        gitlinks.append(dict(path=os.fsdecode(path), pin=oid.decode(), initialized=(file / '.git').exists()))
        continue
    if mode == b'120000':
        assert file.is_symlink(), path
        data = os.fsencode(os.readlink(file))
    else:
        assert file.is_file() and not file.is_symlink(), path
        actual_mode = b'100755' if file.stat().st_mode & 0o111 else b'100644'
        assert mode == actual_mode, path
        data = file.read_bytes()
    digest = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    assert digest == oid.decode(), path
    blobs += 1
index = {}
for row in git('ls-files', '--stage', '-z').split(b'\0'):
    if not row:
        continue
    meta, path = row.split(b'\t', 1)
    mode, oid, stage = meta.split()
    assert stage == b'0', path
    assert path not in index, path
    index[path] = (mode, oid)
assert index == entries, 'index differs from HEAD'
assert not git('status', '--porcelain'), 'worktree is not clean'
print(json.dumps(dict(head=head, tree=tree, raw_blobs_verified=blobs, index_entries_verified=len(index), gitlinks=gitlinks, status='PASS'), indent=2))
