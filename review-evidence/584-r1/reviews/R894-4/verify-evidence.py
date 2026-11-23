#!/usr/bin/env python3
"""Verify public receipt bytes and exact checkout objects without trusting the index."""
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys

ROOT = Path(sys.argv[1]).resolve()
OUT = Path(__file__).resolve().parent
HEAD = '3cda030c174b325e36c26af6420487ff91346d15'
PREV = '599c79af9cfe242bc3d60dd1c80f3e8d57cca12e'
PUB = 'faacf4dfb277313f6cbe7804a995dbbd5227a12c'
PREFIX = 'review-evidence/584-r1/'
ENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')
def git(*args, root=ROOT):
    return subprocess.check_output(['git', *args], cwd=root, env=ENV)
def blob(path):
    return git('show', PUB + ':' + PREFIX + path)
def sha(data):
    return hashlib.sha256(data).hexdigest()
assert git('rev-parse', 'HEAD').decode().strip() == HEAD
assert git('rev-parse', 'HEAD^{tree}').decode().strip() == 'f6050855ee84658b4d907cf8bac69deee39bb893'
changed = git('diff', '--name-only', PREV, HEAD).decode().splitlines()
assert changed == ['CHANGELOG.md', 'docs/ENDSTATION_BUILDER.md', 'docs/reference/PP_DESCRIPTOR_OWNERSHIP.md']
print('PASS exact head/tree; delta is only the three specified documentation files')
print(git('diff', '--numstat', PREV, HEAD).decode(), end='')
manifest = json.loads(blob('MANIFEST.json'))
rows = [r for r in manifest if r['file'].startswith('author-')]
for row in rows:
    assert sha(blob(row['file'])) == row['published_sha256'], row['file']
print(f'PASS public manifest: {len(rows)} author files match published SHA256 (review reports excluded)')
index = blob('author-r3/receipts/INDEX.md').decode()
rows = re.findall(r'^\| `([^`]+)` \| (\d+) \| `([0-9a-f]{64})` \|$', index, re.M)
for path, size, digest in rows:
    data = blob('author-r3/receipts/' + path)
    assert len(data) == int(size) and sha(data) == digest, path
listed = {x[0] for x in rows}
prefix = PREFIX + 'author-r3/receipts/'
actual = {p[len(prefix):] for p in git('ls-tree', '-r', '--name-only', PUB, prefix).decode().splitlines()}
assert listed == actual - {'INDEX.md'}
print(f'PASS round-3 index: {len(rows)} exact size/hash rows, complete file coverage')
for correction, source in [
    ('author-r2/receipts/f5/round1-INDEX-corrected.md', 'author-r1/receipts/'),
    ('author-r3/receipts/f5/round2-INDEX-corrected.md', 'author-r2/receipts/'),
]:
    rows = re.findall(r'^\| `([^`]+)` \| (\d+) \| `([0-9a-f]{64})` \|$', blob(correction).decode(), re.M)
    assert rows, correction
    for path, size, digest in rows:
        data = blob(source + path)
        assert len(data) == int(size) and sha(data) == digest, path
    print(f'PASS historical correction {correction}: {len(rows)} exact size/hash rows')
for p in ['rtl/ship8-mutants.txt', 'gates/builder-union.txt', 'builder/artifact-comparison.txt', 'docs/workflow-summary.txt']:
    dest = OUT / 'public-receipts' / p
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(blob('author-r3/receipts/' + p))

def verify_tree(root, revision):
    records = git('ls-tree', '-rz', revision, root=root).split(b'\0')
    expected_index = []
    files = 0
    links = []
    for record in filter(None, records):
        metadata, rawpath = record.split(b'\t', 1)
        mode, kind, oid = metadata.split()
        path = root / os.fsdecode(rawpath)
        expected_index.append(mode + b' ' + oid + b' 0\t' + rawpath)
        if kind == b'commit':
            links.append((os.fsdecode(rawpath), oid.decode()))
            continue
        attrs = path.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(attrs.st_mode)
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(attrs.st_mode), str(path)
            assert bool(attrs.st_mode & 0o111) == (mode == b'100755'), str(path)
            data = path.read_bytes()
        actual_oid = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert actual_oid == oid.decode(), str(path)
        files += 1
    actual_index = git('ls-files', '--stage', '-z', root=root).split(b'\0')
    assert sorted(filter(None, actual_index)) == sorted(expected_index)
    return files, links
count, links = verify_tree(ROOT, HEAD)
print(f'PASS parent raw bytes/modes/index: {count} blobs; {len(links)} exact gitlink index entries')
required = {'protocol-processor', 'gptp-processor', 'third_party/verilog-axis', 'third_party/tsn-c-stack'}
for name, pin in links:
    if name not in required:
        continue
    root = ROOT / name
    assert git('rev-parse', 'HEAD', root=root).decode().strip() == pin
    assert (root / '.git').is_file()
    count, unused = verify_tree(root, pin)
    print(f'PASS required gitlink {name} {pin}: {count} raw blobs/modes and exact index')
print('PASS no tracked source edits; no source mutation or hardware execution performed')
