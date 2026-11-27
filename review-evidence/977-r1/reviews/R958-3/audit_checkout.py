#!/usr/bin/env python3
"""Verify exact tracked bytes, executable modes, index trees and required gitlinks."""
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
head = '3181a3ec372b6473175cc1c842ada8133a96b127'

def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args])

assert git(root, 'rev-parse', 'HEAD').decode().strip() == head
assert git(root, 'rev-parse', 'HEAD^{tree}').decode().strip() == 'da2f2b0635071acfcfe49efb6c9e2cb0450e85da'
audited = []

def check(repo):
    tree = git(repo, 'ls-tree', '-rz', 'HEAD')
    expected_index = []
    count = 0
    links = []
    for row in tree.split(b'\0'):
        if not row:
            continue
        metadata, path = row.split(b'\t', 1)
        mode, kind, oid = metadata.split()
        expected_index.append(mode + b' ' + oid + b' 0\t' + path)
        p = repo / os.fsdecode(path)
        if kind == b'commit':
            initialized = (p / '.git').exists()
            links.append({'path': os.fsdecode(path), 'oid': oid.decode(), 'initialized': initialized})
            if initialized:
                assert git(p, 'rev-parse', 'HEAD').strip() == oid, p
                check(p)
            else:
                assert repo == root and path == b'external', p
            continue
        assert kind == b'blob'
        st = p.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(st.st_mode)
            data = os.fsencode(os.readlink(p))
        else:
            assert stat.S_ISREG(st.st_mode)
            assert bool(st.st_mode & 0o111) == (mode == b'100755'), p
            data = p.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest().encode()
        assert actual == oid, p
        count += 1
    index = git(repo, 'ls-files', '-s', '-z').split(b'\0')
    assert sorted(x for x in index if x) == sorted(expected_index), repo
    assert not git(repo, 'status', '--porcelain', '--untracked-files=normal').strip(), repo
    audited.append({'path': '.' if repo == root else str(repo.relative_to(root)), 'blobs': count, 'gitlinks': links})

check(root)
paths = git(root, 'diff', '--name-only', '25ff0632', head).decode().splitlines()
tokens = re.compile(r'//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|\s+|.', re.S)

def uncomment(data):
    return ''.join(t for t in tokens.findall(data) if not t.isspace() and not t.startswith(('//', '/*')))

production = []
for path in paths:
    if path.startswith('sw/firmware/ctrl/') and '/test/' not in path and path.endswith(('.c', '.h')):
        before = git(root, 'show', '25ff0632:' + path).decode()
        after = (root / path).read_text()
        assert uncomment(before) == uncomment(after), path
        production.append(path)
hot = 'sw/firmware/ctrl/plat/ctrl_split_hot.txt'
before = git(root, 'show', '25ff0632:' + hot).decode()
after = (root / hot).read_text()
assert [l for l in before.splitlines() if not l.startswith('#')] == [l for l in after.splitlines() if not l.startswith('#')]
result = {'head': head, 'tree': 'da2f2b0635071acfcfe49efb6c9e2cb0450e85da', 'audited': audited,
          'total_blobs': sum(a['blobs'] for a in audited), 'production_comment_only': production,
          'hot_entries_unchanged': True, 'gitlink_delta': git(root, 'diff', '--raw', '25ff0632', head, '--', 'third_party', 'protocol-processor', 'gptp-processor', 'external').decode()}
assert not result['gitlink_delta']
(packet / 'checkout-audit.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
