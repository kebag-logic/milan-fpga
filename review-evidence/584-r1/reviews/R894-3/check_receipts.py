#!/usr/bin/env python3
"""Independently verify published author receipts directly from immutable Git blobs."""
import hashlib
import json
import re
import subprocess
import sys

REV = '82a41140e1a7cc7779ab05eef732e569cb8a6157'
ROOT = 'review-evidence/584-r1/'

def git(*args):
    return subprocess.check_output(['git', '--no-replace-objects', *args])

def blob(path):
    return git('show', REV + ':' + ROOT + path)

def digest(data):
    return hashlib.sha256(data).hexdigest()

paths = {p[len(ROOT):] for p in git('ls-tree', '-r', '--name-only', REV, ROOT).decode().splitlines()}
manifest = json.loads(blob('MANIFEST.json'))
authors = [r for r in manifest if r['file'].startswith(('author-r1/', 'author-r2/', 'author-r3/'))]
print('Evidence commit:', REV)
print('Source head: 599c79af9cfe242bc3d60dd1c80f3e8d57cca12e')
bad = []
for row in authors:
    actual = digest(blob(row['file']))
    if actual != row['published_sha256']:
        bad.append(row['file'])
print(f'Publication manifest author files: {len(authors)-len(bad)}/{len(authors)} match published_sha256')
assert not bad, bad
r3 = [r for r in authors if r['file'].startswith('author-r3/')]
assert all(r['original_sha256'] == r['published_sha256'] and not r['path_redacted'] for r in r3)
print(f'Round 3 publication normalization: {len(r3)}/{len(r3)} unchanged')
pattern = re.compile(r'^\| `([^`]+)` \| (\d+) \| `([0-9a-f]{64})` \|$', re.M)

def check(index, base, complete=False, historical=False):
    rows = pattern.findall(blob(index).decode())
    assert rows, index
    seen, mismatches = set(), []
    for name, count, sha in rows:
        assert name not in seen, (index, 'duplicate', name)
        seen.add(name)
        data = blob(base + name)
        actual = digest(data)
        ok = len(data) == int(count) and actual == sha
        print(f'{"OK" if ok else "SUPERSEDED-MISMATCH"} {base+name} bytes={len(data)} sha256={actual}')
        if not ok:
            mismatches.append(name)
    if complete:
        expected = {p[len(base):] for p in paths if p.startswith(base) and p != base + 'INDEX.md'}
        assert seen == expected, (expected-seen, seen-expected)
    print(f'INDEX {index}: {len(rows)-len(mismatches)}/{len(rows)} exact size/hash; complete={complete}')
    if not historical:
        assert not mismatches, mismatches
    return len(rows), mismatches

check('author-r3/receipts/INDEX.md', 'author-r3/receipts/', complete=True)
check('author-r2/receipts/f5/round1-INDEX-corrected.md', 'author-r1/receipts/', complete=True)
check('author-r3/receipts/f5/round2-INDEX-corrected.md', 'author-r2/receipts/', complete=True)
assert len(check('author-r1/receipts/INDEX.md', 'author-r1/receipts/', historical=True)[1]) == 3
assert len(check('author-r2/receipts/INDEX.md', 'author-r2/receipts/', historical=True)[1]) == 2
headers = git('cat-file', 'commit', REV).split(b'\n\n', 1)[0]
print('Evidence commit signature header present:', b'\ngpgsig ' in headers)
print('PASS: published bytes and replacement indexes verified; superseded indexes remain historical')
