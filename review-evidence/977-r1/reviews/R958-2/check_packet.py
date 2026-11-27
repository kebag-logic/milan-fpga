#!/usr/bin/env python3
"""Verify published receipt bytes and extract author evidence, never review reports."""
import hashlib
import json
import pathlib
import subprocess
import sys

repo = pathlib.Path(sys.argv[1]).resolve()
out = pathlib.Path(__file__).resolve().parent
commit = 'da2acce94a7d069b16930642124a2fff7a2e9586'
prefix = 'review-evidence/977-r1/'
def git(*args):
    return subprocess.check_output(['git', '-C', str(repo), *args])
manifest = json.loads(git('show', f'{commit}:{prefix}MANIFEST.json'))
checked = []
for row in manifest:
    name = row['file']
    if not name.startswith(('author/', 'author-r10/', 'author-text/')):
        continue
    data = git('show', f'{commit}:{prefix}{name}')
    digest = hashlib.sha256(data).hexdigest()
    assert digest == row['published_sha256'], name
    target = out / 'scratch' / 'public-packet' / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    checked.append({'path': name, 'sha256': digest, 'bytes': len(data), 'path_redacted': row['path_redacted']})
print(json.dumps({'commit': commit, 'checked': len(checked), 'files': checked}, indent=2))
