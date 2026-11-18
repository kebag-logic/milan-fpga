#!/usr/bin/env python3
"""Audit source bytes/index/modes/gitlinks and the public receipt manifest.
Usage: audit.py CHECKOUT PACKET. Run after all probes.
"""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

repo, packet = map(lambda s: Path(s).resolve(), sys.argv[1:3])
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')
def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], env=env)

def audit(root, ref, label, children=False):
    records = git(root, 'ls-tree', '-rz', ref).split(b'\0')
    expected = []
    count = 0
    for record in records:
        if not record:
            continue
        meta, name = record.split(b'\t', 1)
        mode, kind, oid = meta.split()
        expected.append(mode + b' ' + oid + b' 0\t' + name)
        file = root / os.fsdecode(name)
        if kind == b'commit':
            if children and os.fsdecode(name) != 'external':
                actual = git(file, 'rev-parse', 'HEAD').strip()
                assert actual == oid, (name, 'gitlink')
                assert git(file, 'rev-parse', '--show-superproject-working-tree').strip(), name
                audit(file, oid.decode(), os.fsdecode(name))
            continue
        st = file.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(st.st_mode), name
            data = os.fsencode(os.readlink(file))
        else:
            assert stat.S_ISREG(st.st_mode), name
            assert bool(st.st_mode & 0o111) == (mode == b'100755'), name
            data = file.read_bytes()
        digest = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest().encode()
        assert digest == oid, (label, name, 'blob')
        count += 1
    index = git(root, 'ls-files', '--stage', '-z').split(b'\0')
    assert sorted(filter(None, index)) == sorted(expected), (label, 'index')
    print(f'{label}: {count} tracked blobs byte/mode exact; index exact; HEAD {ref}')

head = '9f4f3de03f99dc8c7a72f5f8884f00df82c965d2'
assert git(repo, 'rev-parse', 'HEAD').decode().strip() == head
assert git(repo, 'rev-parse', 'HEAD^{tree}').decode().strip() == '9bdd0b0644d75354b43767e8453db2dc3649ea8b'
audit(repo, head, 'source', True)
print('external gitlink is unchanged; optional external checkout is uninitialized')
print('source status:', git(repo, 'status', '--porcelain').decode().strip() or 'clean')
archive = packet / 'scratch/review-evidence/946-r1'
entries = json.loads((archive / 'MANIFEST.json').read_text())
selected = [x for x in entries if x['file'].startswith('author-r2/')]
for item in selected:
    got = hashlib.sha256((archive / item['file']).read_bytes()).hexdigest()
    assert got == item['published_sha256'], item['file']
    print(got, item['file'])
print(f'Public archive c6fc4753: {len(selected)} author-r2 files match published SHA256 manifest')
print('Archive commit signature indicator:', git(repo, 'show', '-s', '--format=%G?', 'c6fc4753').decode().strip())
print('N indicates no commit signature; hash identity is not signature authentication.')
print('548324b5 -> exact head delta:')
print(git(repo, 'diff', '548324b5..HEAD', '--stat').decode())
print('Round-2 one-line subjects:')
print(git(repo, 'log', '--format=%H %s', '66c6edf3..HEAD').decode())
