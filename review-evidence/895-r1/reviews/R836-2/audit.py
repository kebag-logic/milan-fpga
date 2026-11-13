#!/usr/bin/env python3
"""Prove archive checksums and checkout bytes/modes/index against Git objects.
Usage: python3 -B audit.py CHECKOUT PACKET
"""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

repo, packet = map(lambda s: Path(s).resolve(), sys.argv[1:])
os.environ['GIT_NO_REPLACE_OBJECTS'] = '1'
def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args])
errors = []
def prove(root, rev):
    tree = git(root, 'ls-tree', '-rz', rev).split(b'\0')
    expected_index = []
    files = 0
    for item in filter(None, tree):
        meta, name = item.split(b'\t', 1)
        mode, kind, oid = meta.split()
        expected_index.append(mode + b' ' + oid + b' 0\t' + name)
        if kind != b'blob':
            continue
        path = root / os.fsdecode(name)
        try:
            st = path.lstat()
            if mode == b'120000':
                assert stat.S_ISLNK(st.st_mode)
                data = os.fsencode(os.readlink(path))
            else:
                assert stat.S_ISREG(st.st_mode)
                assert bool(st.st_mode & 0o111) == (mode == b'100755')
                data = path.read_bytes()
            blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
            assert blob == oid.decode()
            files += 1
        except (AssertionError, OSError):
            errors.append(f'bytes/mode mismatch: {name!r}')
    actual = list(filter(None, git(root, 'ls-files', '--stage', '-z').split(b'\0')))
    if sorted(actual) != sorted(expected_index):
        errors.append(f'index mismatch: {root.name}')
    print(f'{root.name}: {rev}, {files} blobs/modes checked, index compared')

head = git(repo, 'rev-parse', 'HEAD').decode().strip()
assert head == '18300f6e5f0c63b2ebc81d6bbc243496034f638a'
print('head', head, 'tree', git(repo, 'rev-parse', 'HEAD^{tree}').decode().strip())
prove(repo, head)
for sub in ('protocol-processor', 'gptp-processor', 'third_party/verilog-axis', 'third_party/tsn-c-stack', 'third_party/lwSRP'):
    pin = git(repo, 'rev-parse', f'HEAD:{sub}').decode().strip()
    assert git(repo/sub, 'rev-parse', 'HEAD').decode().strip() == pin
    prove(repo/sub, pin)
archive = packet / 'scratch/review-evidence/895-r1'
manifest = json.loads((archive/'MANIFEST.json').read_text())
n = 0
for entry in manifest:
    if not entry['file'].startswith('author-r2/'):
        continue
    path = archive / entry['file']
    assert hashlib.sha256(path.read_bytes()).hexdigest() == entry['published_sha256'], entry['file']
    n += 1
print(f'archive 5fda69702df2e27bbbf4711c766b3b40f6703f99: {n} author-r2 published hashes verified')
print('Archive commit has no Git signature; no detached signature found in packet. Hash verification is not signer authentication.')
print('errors:', len(errors))
for error in errors:
    print(error)
sys.exit(bool(errors))
