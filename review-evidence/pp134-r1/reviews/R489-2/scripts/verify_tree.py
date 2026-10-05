#!/usr/bin/env python3
"""Compare tracked filesystem bytes/modes, index and submodule pins with exact HEAD."""
import argparse
import hashlib
import json
from pathlib import Path
import stat
import subprocess

p = argparse.ArgumentParser()
p.add_argument('source', type=Path)
a = p.parse_args()
root = a.source.resolve()
def git(*args):
    return subprocess.check_output(['git', '-C', str(root), *args])
head = git('rev-parse', 'HEAD').decode().strip()
tree = git('rev-parse', 'HEAD^{tree}').decode().strip()
assert head == '9050c4bbd25556929a0f24fb98258bc98e3bcfbe'
assert tree == '3bcc8532549ea69139323a863049022d10f799c1'
entries = git('ls-tree', '-rz', 'HEAD').split(b'\0')
index = git('ls-files', '--stage', '-z').split(b'\0')
expected_index = []
errors, links = [], []
count = 0
for entry in filter(None, entries):
    meta, raw_path = entry.split(b'\t')
    mode, kind, oid = meta.split()
    expected_index.append(mode + b' ' + oid + b' 0\t' + raw_path)
    path = root / raw_path.decode()
    if mode == b'160000':
        actual = subprocess.check_output(['git', '-C', str(path), 'rev-parse', 'HEAD']).strip()
        links.append(dict(path=raw_path.decode(), expected=oid.decode(), actual=actual.decode()))
        if actual != oid: errors.append('gitlink ' + str(path))
        continue
    data = path.readlink().as_posix().encode() if mode == b'120000' else path.read_bytes()
    actual_oid = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    actual_mode = '120000' if path.is_symlink() else ('100755' if path.stat().st_mode & stat.S_IXUSR else '100644')
    if actual_oid != oid.decode() or actual_mode != mode.decode(): errors.append(raw_path.decode())
    count += 1
if sorted(expected_index) != sorted(filter(None, index)): errors.append('index differs')
print(json.dumps(dict(head=head, tree=tree, tracked_blobs=count, gitlinks=links,
                     index_equal='index differs' not in errors, errors=errors), indent=2))
raise SystemExit(bool(errors))
