#!/usr/bin/env python3
"""Verify published receipt hashes against the immutable public archive."""
import hashlib
import json
import subprocess

revision = '06c6f5d97328e8c4c684314df156d02637224341'
prefix = 'review-evidence/665s3-r1/'
def read(path):
    return subprocess.check_output(['git','show',f'{revision}:{prefix}{path}'])
entries = json.loads(read('MANIFEST.json'))
for entry in entries:
    digest = hashlib.sha256(read(entry['file'])).hexdigest()
    assert digest == entry['published_sha256'], entry['file']
commit = subprocess.check_output(['git','cat-file','commit',revision])
print(f'Publication {revision}: {len(entries)} published SHA256 entries verified')
print('Commit has signature field:', b'\ngpgsig ' in commit)
print('Hash integrity does not establish a cryptographic signature or execution authenticity.')
