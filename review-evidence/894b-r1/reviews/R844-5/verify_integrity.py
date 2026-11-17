#!/usr/bin/env python3
"""Verify public packet hashes and exact tracked bytes, modes and index entries.
Usage: python3 -B verify_integrity.py REPOSITORY EXTRACTED_PACKET_ROOT
"""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

repo, packet = map(Path, sys.argv[1:])
env = {**os.environ, 'GIT_NO_REPLACE_OBJECTS': '1'}

def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], env=env)

def check_tree(root, rev, label):
    entries = git(root, 'ls-tree', '-rz', rev).split(b'\0')
    expected, count, links = {}, 0, {}
    for entry in filter(None, entries):
        meta, name = entry.split(b'\t', 1)
        mode, kind, oid = meta.split()
        expected[name] = (mode, oid, b'0')
        path = root / os.fsdecode(name)
        if kind == b'commit':
            links[os.fsdecode(name)] = oid.decode()
            continue
        s = path.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(s.st_mode), name
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(s.st_mode), name
            assert bool(s.st_mode & 0o111) == (mode == b'100755'), name
            data = path.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert actual == oid.decode(), (label, name)
        count += 1
    index = {}
    for line in filter(None, git(root, 'ls-files', '--stage', '-z').split(b'\0')):
        meta, name = line.split(b'\t', 1)
        assert name not in index, ('multiple index stages', name)
        index[name] = tuple(meta.split())
    assert index == expected, ('index differs', label)
    assert git(root, 'rev-parse', 'HEAD').decode().strip() == rev
    print(f'{label}: {count} tracked blobs verified by raw bytes/mode; index matches tree; gitlinks {len(links)}')
    return links

head = 'd0a2a1605d7acc691936a61f9afaa0e67f4b46f2'
tree = git(repo, 'rev-parse', head + '^{tree}').decode().strip()
assert tree == '200d73043aefc480fc11c6d00e2689c4757077ff'
print('HEAD', head, 'TREE', tree)
links = check_tree(repo, head, 'candidate')
for sub in ('protocol-processor', 'gptp-processor', 'third_party/verilog-axis', 'third_party/tsn-c-stack', 'third_party/lwSRP'):
    print('GITLINK', sub, links[sub])
    check_tree(repo / sub, links[sub], sub)
print('external gitlink is uninitialized; no scoped test requires it')
manifest = json.loads((packet / 'MANIFEST.json').read_text())
selected = [r for r in manifest if r['file'].startswith('author-r13/')]
assert selected
seen = set()
for row in selected:
    path = packet / row['file']
    assert row['file'] not in seen
    seen.add(row['file'])
    assert hashlib.sha256(path.read_bytes()).hexdigest() == row['published_sha256'], row['file']
actual = {str(p.relative_to(packet)) for p in (packet / 'author-r13').rglob('*') if p.is_file()}
print('Published author-r13 hashes:', len(selected), 'verified; unlisted files:', sorted(actual - seen))
assert not (actual - seen)
print('Archive', git(repo, 'rev-parse', '48b6c3a2').decode().strip())
print('Archive signature status:', git(repo, 'log', '-1', '--format=%G?', '48b6c3a2').decode().strip(), '(N means unsigned; no signature authentication claimed)')
print('RESULT: PASS')
