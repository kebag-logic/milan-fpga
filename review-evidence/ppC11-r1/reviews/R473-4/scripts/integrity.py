#!/usr/bin/env python3
"""Check tracked bytes, executable modes, index tree and every gitlink."""
import argparse
import hashlib
import json
from pathlib import Path
import stat
import subprocess

p = argparse.ArgumentParser()
p.add_argument('--source', type=Path, required=True)
a = p.parse_args()
def git(*args):
    return subprocess.check_output(['git', '-C', str(a.source), *args])
head = '7124bde172a523179a2788dca825587aa5a2a1e6'
tree = '6009d72c1ee277ec12e287926b371000be555fba'
assert git('rev-parse', 'HEAD').decode().strip() == head
assert git('rev-parse', 'HEAD^{tree}').decode().strip() == tree
assert git('write-tree').decode().strip() == tree
count = 0
links = []
failures = []
for entry in git('ls-tree', '-rz', head).split(b'\0'):
    if not entry:
        continue
    meta, name = entry.split(b'\t', 1)
    mode, kind, oid = meta.decode().split()
    rel = name.decode()
    path = a.source / rel
    if mode == '160000':
        actual = subprocess.check_output(['git', '-C', str(path), 'rev-parse', 'HEAD']).decode().strip()
        links.append({'path': rel, 'expected': oid, 'actual': actual})
        if actual != oid:
            failures.append(rel + ': gitlink mismatch')
        continue
    data = path.read_bytes()
    actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    actual_mode = '100755' if path.stat().st_mode & stat.S_IXUSR else '100644'
    if actual != oid or actual_mode != mode:
        failures.append(rel + ': blob or mode mismatch')
    count += 1
status = git('status', '--porcelain=v1').decode()
print(json.dumps({'head': head, 'tree': tree, 'index_matches': True,
                  'tracked_blobs_checked': count, 'gitlinks': links,
                  'status': status, 'failures': failures}, indent=2))
assert not failures and not status
