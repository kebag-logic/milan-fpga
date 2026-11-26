#!/usr/bin/env python3
"""Verify the public packet's published digests without reading review reports."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path
repo, packet = map(lambda p: Path(p).resolve(), sys.argv[1:3])
records = []
for commit, directory in [('40ce56ee579d00874e4c9db98893f0742498aee3', 'adp970-r1'),
                          ('af092a85bcda1d60fab649ca42e2b013996ee21e', 'adp970-r2')]:
    base = 'review-evidence/' + directory
    def blob(path):
        return subprocess.check_output(['git', '-C', str(repo), 'show', f'{commit}:{base}/{path}'])
    manifest = json.loads(blob('MANIFEST.json'))
    for entry in manifest:
        if not entry['file'].startswith('author/'):
            continue
        data = blob(entry['file'])
        digest = hashlib.sha256(data).hexdigest()
        expected = entry['published_sha256']
        assert digest == expected, entry['file']
        dest = packet / 'scratch/public' / directory / entry['file']
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        records.append({'commit': commit, 'file': base + '/' + entry['file'], 'sha256': digest,
                        'published_digest_matches': True, 'path_redacted': entry.get('path_redacted')})
out = packet / 'receipts/evidence-integrity.json'
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(records, indent=2) + '\n')
print(f'PASS: {len(records)} public author files match their published manifest digests')
