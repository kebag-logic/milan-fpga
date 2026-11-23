#!/usr/bin/env python3
"""Verify public author receipt bytes without reading private or reviewer material.
Usage: python3 audit_packet.py CHECKOUT OUTPUT_DIR
The immutable evidence commit must already be fetched into CHECKOUT.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

checkout, output = map(Path, sys.argv[1:])
revision = 'e6835fbaa3942f3c2ad0dc5f8a1968a118e45a55'
prefix = 'review-evidence/969-r1/'

def git(*args):
    return subprocess.check_output(['git', '--no-replace-objects', '-C', str(checkout), *args])

def blob(path):
    return git('show', revision + ':' + prefix + path)

manifest = json.loads(blob('MANIFEST.json'))
lines = ['Evidence commit ' + revision,
         'Commit has embedded signature: ' + str(b'gpgsig ' in git('cat-file', 'commit', revision))]
for row in manifest:
    path = row['file']
    if not path.startswith(('author-r1/receipts/', 'author-r2/receipts/', 'author-r3/receipts/')):
        continue
    data = blob(path)
    digest = hashlib.sha256(data).hexdigest()
    assert digest == row['published_sha256'], path
    lines.append('OK ' + digest + ' ' + path)
    target = output / 'scratch' / 'public' / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
(output / 'receipt-integrity.txt').write_text('\n'.join(lines) + '\n')
print(f'{len(lines)-2} published author receipt hashes verified; no mismatch')
