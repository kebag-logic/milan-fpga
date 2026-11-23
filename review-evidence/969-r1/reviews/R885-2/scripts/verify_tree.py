#!/usr/bin/env python3
"""Prove tracked bytes, executable modes, index entries and required submodule gitlinks without trusting status.
Usage: python3 -I verify_tree.py CHECKOUT PACKET
"""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys

root, packet = (Path(p).resolve() for p in sys.argv[1:])
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')
head = 'e816c74da53a5822f2ddc1661e5ffae297f1b3aa'
tree = 'e2b9b5f88b2c9ffb5aff42996c34150c2afda190'
required = ('protocol-processor', 'gptp-processor', 'third_party/verilog-axis',
            'third_party/tsn-c-stack', 'third_party/lwSRP')
lines, failures = [], []
def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args], env=env)
def verify(repo, rev, label):
    entries = {}
    count = 0
    for row in git(repo, 'ls-tree', '-rz', rev).split(b'\0'):
        if not row:
            continue
        info, name = row.split(b'\t', 1)
        mode, kind, oid = info.split()
        entries[name] = (mode, oid)
        if kind == b'commit':
            continue
        path = repo / os.fsdecode(name)
        try:
            st = path.lstat()
            actual_mode = b'120000' if stat.S_ISLNK(st.st_mode) else (
                b'100755' if stat.S_ISREG(st.st_mode) and st.st_mode & 0o111 else b'100644')
            assert stat.S_ISLNK(st.st_mode) or stat.S_ISREG(st.st_mode)
            data = os.fsencode(os.readlink(path)) if stat.S_ISLNK(st.st_mode) else path.read_bytes()
            hashed = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest().encode()
            if (actual_mode, hashed) != (mode, oid):
                failures.append(f'{label}/{os.fsdecode(name)}: bytes or mode differ')
            count += 1
        except (OSError, AssertionError) as e:
            failures.append(f'{label}/{os.fsdecode(name)}: unreadable or wrong kind: {type(e).__name__}')
    index = {}
    for row in git(repo, 'ls-files', '--stage', '-z').split(b'\0'):
        if row:
            info, name = row.split(b'\t', 1)
            mode, oid, stage = info.split()
            if stage != b'0' or name in index:
                failures.append(f'{label}: unmerged/duplicate index')
            index[name] = (mode, oid)
    if index != entries:
        failures.append(f'{label}: index differs from commit tree')
    actual = git(repo, 'rev-parse', 'HEAD').decode().strip()
    if actual != rev:
        failures.append(f'{label}: HEAD differs')
    lines.append(f'{label}: HEAD {actual}; checked {count} blobs and modes; index exact')
    return entries

entries = verify(root, head, 'candidate')
actual_tree = git(root, 'rev-parse', 'HEAD^{tree}').decode().strip()
if actual_tree != tree:
    failures.append('candidate tree mismatch')
lines.append(f'Candidate tree {actual_tree}')
for sub in required:
    mode, oid = entries[os.fsencode(sub)]
    assert mode == b'160000'
    path = root/sub
    if path.is_symlink() or not (path/'.git').is_file():
        failures.append(f'{sub}: not an initialized registered submodule')
    verify(path, oid.decode(), sub)
lines.append('external: deliberately uninitialized, not a required test dependency')
lines += [f'FAIL {f}' for f in failures]
lines.append(f'TREE VERIFICATION {"PASS" if not failures else "FAIL"}; {len(failures)} differences')
(packet/'receipts/tree-verification.txt').write_text('\n'.join(lines)+'\n')
print('\n'.join(lines))
sys.exit(int(bool(failures)))
