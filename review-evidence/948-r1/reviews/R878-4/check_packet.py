#!/usr/bin/env python3
"""Check published receipt hashes without reading any review report."""
import hashlib
import json
import subprocess
import sys

ref = 'eea845dba7b561499de5cf537a5b665d72e278b1'
prefix = 'review-evidence/948-r1/'
def blob(path):
    return subprocess.check_output(['git', 'show', f'{ref}:{prefix}{path}'])

manifest = json.loads(blob('MANIFEST.json'))
checked = 0
for row in manifest:
    if row['file'].startswith('reviews/'):
        continue
    actual = hashlib.sha256(blob(row['file'])).hexdigest()
    assert actual == row['published_sha256'], row['file']
    checked += 1
print(f'Published manifest: {checked} non-review files verified, zero hash mismatches.')
rows = blob('author-r3/receipts/MANIFEST.sha256').decode().splitlines()
for row in rows:
    digest, path = row.split(maxsplit=1)
    path = path.lstrip('*')
    assert hashlib.sha256(blob('author-r3/receipts/' + path)).hexdigest() == digest, path
print(f'Author correction receipts: {len(rows)} hashes verified.')
raw = subprocess.check_output(['git', 'cat-file', 'commit', ref])
print('Publication commit has embedded signature:', b'\ngpgsig ' in raw)
names = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', ref, prefix]).decode().splitlines()
signatures = [p for p in names if p.endswith(('.sig', '.asc', '.minisig', '.pub', '.pem'))]
print('Detached signature/key artifacts:', signatures)
print('This verifies published-byte identity; no cryptographic publisher signature is claimed.')
