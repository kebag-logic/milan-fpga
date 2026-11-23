#!/usr/bin/env python3
"""Verify published receipt hashes without opening other review reports."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

repo = Path(sys.argv[1]).resolve()
out = Path(__file__).resolve().parent
rev = 'ad3798bc641ff3f9d1f3827c5acf6a30fab0ac4b'
prefix = 'review-evidence/linuxprof-r1/'
def git(*args):
    return subprocess.check_output(['git', '-C', str(repo), *args])

manifest = json.loads(git('show', rev + ':' + prefix + 'MANIFEST.json'))
print('Published commit:', rev)
print('Commit contains signature:', b'\ngpgsig ' in git('cat-file', 'commit', rev))
print('Manifest records:', len(manifest))
count = 0
for entry in manifest:
    name = entry['file']
    if not name.startswith(('author/receipts/', 'author-r2/receipts/', 'author-r3/receipts/')):
        continue
    data = git('show', rev + ':' + prefix + name)
    digest = hashlib.sha256(data).hexdigest()
    assert digest == entry['published_sha256'], name
    print('MATCH', digest, name)
    dest = out / 'scratch' / 'published' / name
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    count += 1
print('Verified author receipts:', count)
names = git('ls-tree', '-r', '--name-only', rev, prefix).decode().splitlines()
print('Signature-named packet entries:', [n for n in names if n.endswith(('.asc', '.sig', '.pub', '.sshsig'))])
