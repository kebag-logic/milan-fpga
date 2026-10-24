#!/usr/bin/env python3
"""Verify published receipt hashes without loading any other review report."""
import hashlib
import json
import pathlib
import subprocess
import sys

repo = pathlib.Path(sys.argv[1]).resolve()
out = pathlib.Path(__file__).resolve().parent
commit = '4484c29cd1224098b5b0d4576cc5d8e4897b4836'
prefix = 'review-evidence/774-r1/'
def blob(path):
    return subprocess.check_output(['git', '-C', str(repo), 'show', f'{commit}:{prefix}{path}'])
manifest = json.loads(blob('MANIFEST.json'))
count = 0
for item in manifest:
    name = item['file']
    if not name.startswith('author-r2/receipts/'):
        continue
    data = blob(name)
    digest = hashlib.sha256(data).hexdigest()
    assert digest == item['published_sha256'], name
    target = out / 'scratch' / 'published' / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    print(f'{digest}  {name}')
    count += 1
print(f'PASS: {count} published author receipt hashes verified at {commit}.')
print('The archive commit has no embedded Git signature; hashes prove consistency, not signer identity.')
