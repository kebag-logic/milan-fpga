# SPDX-License-Identifier: Apache-2.0
"""Verify worktree blob bytes, Git modes, index entries, head and gitlinks."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

p = argparse.ArgumentParser()
p.add_argument('--source', type=Path, required=True)
p.add_argument('--packet', type=Path, required=True)
a = p.parse_args()
source, packet = a.source.resolve(), a.packet.resolve()
def git(*args):
    return subprocess.check_output(['git', '-C', str(source), *args])
head = git('rev-parse', 'HEAD').decode().strip()
tree = git('rev-parse', 'HEAD^{tree}').decode().strip()
assert head == '82422d6ffe38d430576cd9d874a45b9e124e6c63'
assert tree == '02fda6f08254fc7dd5c259c996cfbb31e76682d7'
index = {}
for row in git('ls-files', '--stage', '-z').split(b'\0'):
    if row:
        meta, name = row.split(b'\t', 1)
        mode, oid, stage = meta.decode().split()
        assert stage == '0'
        index[name.decode()] = (mode, oid)
rows, gitlinks = [], []
for row in git('ls-tree', '-rz', 'HEAD').split(b'\0'):
    if not row:
        continue
    meta, name = row.split(b'\t', 1)
    mode, kind, oid = meta.decode().split()
    name = name.decode()
    assert index.pop(name) == (mode, oid)
    if mode == '160000':
        gitlinks.append({'path': name, 'commit': oid})
        continue
    f = source / name
    data = str(f.readlink()).encode() if mode == '120000' else f.read_bytes()
    actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    actual_mode = '120000' if f.is_symlink() else ('100755' if f.stat().st_mode & 0o111 else '100644')
    assert (actual_mode, actual) == (mode, oid), name
    assert b'SPDX-License-Identifier: Apache-2.0' in data, name
    rows.append({'path': name, 'mode': mode, 'blob': oid, 'sha256': hashlib.sha256(data).hexdigest()})
assert not index
status = git('status', '--porcelain').decode()
assert status == '', status
changed = git('diff', '--name-only', '1401654530ce7d9275de9b901e67df47e5bbc536..HEAD').decode().splitlines()
rtl = [f for f in changed if Path(f).suffix in ('.v', '.sv', '.vhd', '.vhdl', '.xdc', '.sdc')]
result = {'head': head, 'tree': tree, 'files': rows, 'gitlinks': gitlinks,
          'tracked_files': len(rows), 'changed_files': len(changed), 'changed_rtl_or_constraints': rtl,
          'index_matches_head': True, 'status': status}
(packet / 'receipts/integrity.json').write_text(json.dumps(result, indent=2) + '\n')
print(f'Head and tree match; {len(rows)} raw blobs and modes match; index matches; gitlinks={len(gitlinks)}; clean worktree; changed RTL={len(rtl)}')
