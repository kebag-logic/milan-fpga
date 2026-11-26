#!/usr/bin/env python3
"""Prove tracked bytes, file kinds/modes, index entries, and required gitlinks."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
repo, packet = map(lambda p: Path(p).resolve(), sys.argv[1:3])
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')
def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], env=env)
reports = []
def check(root, revision):
    assert git(root, 'rev-parse', 'HEAD').decode().strip() == revision
    expected = {}
    links = {}
    for item in git(root, 'ls-tree', '-rz', revision).split(b'\0'):
        if not item:
            continue
        info, raw_path = item.split(b'\t', 1)
        mode, kind, digest = info.decode().split()
        path = os.fsdecode(raw_path)
        expected[path] = (mode, digest, '0')
        if mode == '160000':
            links[path] = digest
            continue
        p = root / path
        st = p.lstat()
        if mode == '120000':
            assert stat.S_ISLNK(st.st_mode), path
            data = os.fsencode(os.readlink(p))
        else:
            assert stat.S_ISREG(st.st_mode), path
            assert bool(st.st_mode & 0o111) == (mode == '100755'), path
            data = p.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert actual == digest, path
    actual_index = {}
    for item in git(root, 'ls-files', '--stage', '-z').split(b'\0'):
        if item:
            info, path = item.split(b'\t', 1)
            actual_index[os.fsdecode(path)] = tuple(info.decode().split())
    assert actual_index == expected, str(root)
    reports.append({'repository': '.' if root == repo else str(root.relative_to(repo)),
                    'head': revision, 'tree': git(root, 'rev-parse', revision + '^{tree}').decode().strip(),
                    'tracked_entries': len(expected), 'bytes_modes_index': 'PASS', 'gitlinks': links})
    return links
head = 'f4833e16a07d07494277aba8dc7a5de19320c20b'
links = check(repo, head)
for path in ('protocol-processor', 'gptp-processor', 'third_party/verilog-axis',
             'third_party/lwSRP', 'third_party/tsn-c-stack'):
    check(repo / path, links[path])
assert reports[0]['tree'] == 'acc0b819bec698855f98c81f52a4a04abcde6afd'
out = packet / 'receipts/checkout-integrity.json'
out.write_text(json.dumps(reports, indent=2) + '\n')
print('PASS:', sum(r['tracked_entries'] for r in reports), 'tracked entries across', len(reports), 'repositories')
