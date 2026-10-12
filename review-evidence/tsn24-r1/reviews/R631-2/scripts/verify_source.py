#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Compare every tracked worktree byte, mode and index entry to a fixed commit."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess

p = argparse.ArgumentParser()
p.add_argument('--repo', type=Path, required=True)
p.add_argument('--head', required=True)
p.add_argument('--out', type=Path, required=True)
a = p.parse_args()
def git(*args):
    return subprocess.check_output(['git', '-C', str(a.repo), *args])
head = git('rev-parse', 'HEAD').decode().strip()
tree = git('rev-parse', a.head + '^{tree}').decode().strip()
rows, errors, gitlinks = [], [], []
for raw in git('ls-tree', '-rz', a.head).split(b'\0'):
    if not raw:
        continue
    info, name = raw.split(b'\t', 1)
    mode, kind, oid = info.decode().split()
    name = name.decode()
    path = a.repo / name
    if kind == 'commit':
        gitlinks.append(dict(path=name, mode=mode, oid=oid))
        continue
    data = os.readlink(path).encode() if mode == '120000' else path.read_bytes()
    actual_oid = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    actual_mode = '120000' if path.is_symlink() else ('100755' if path.stat().st_mode & 0o111 else '100644')
    row = dict(path=name, oid=oid, actual_oid=actual_oid, mode=mode, actual_mode=actual_mode,
               sha256=hashlib.sha256(data).hexdigest())
    rows.append(row)
    if actual_oid != oid or actual_mode != mode:
        errors.append(name)
index_tree = git('write-tree').decode().strip()
status = git('status', '--porcelain=v1').decode()
result = dict(head=head, expected_head=a.head, tree=tree, index_tree=index_tree,
              tracked=rows, required_gitlinks=gitlinks, status=status, errors=errors)
a.out.write_text(json.dumps(result, indent=2) + '\n')
assert head == a.head and index_tree == tree and not errors
print(json.dumps(dict(head=head, tree=tree, tracked_files=len(rows), gitlinks=gitlinks,
                     errors=errors, status=status), indent=2))
