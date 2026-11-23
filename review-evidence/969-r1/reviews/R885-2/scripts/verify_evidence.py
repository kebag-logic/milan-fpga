#!/usr/bin/env python3
"""Verify public author receipts against the published packet manifest, then extract into scratch.
Usage: python3 -I verify_evidence.py CHECKOUT PACKET
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

root, packet = (Path(p).resolve() for p in sys.argv[1:])
commit = '1cd9d3fd3e46aaeeff6650f1bc60cce139645f0e'
prefix = 'review-evidence/969-r1/'
def blob(path):
    return subprocess.check_output(['git', '-C', str(root), 'show', f'{commit}:{prefix}{path}'])
manifest = blob('MANIFEST.json')
entries = json.loads(manifest)
out = packet / 'scratch' / 'published'
out.mkdir(parents=True, exist_ok=True)
(out / 'MANIFEST.json').write_bytes(manifest)
lines = [f'Public evidence commit {commit}', f'MANIFEST.json sha256 {hashlib.sha256(manifest).hexdigest()}']
failed = 0
for e in entries:
    path = e['file']
    if not path.startswith(('author-r1/receipts/', 'author-r2/receipts/')):
        continue
    assert '..' not in Path(path).parts and not Path(path).is_absolute()
    data = blob(path)
    actual = hashlib.sha256(data).hexdigest()
    ok = actual == e['published_sha256']
    failed += not ok
    lines.append(f'{"PASS" if ok else "FAIL"} {actual} {path}')
    dest = out / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
lines.append(f'Verified {len(lines)-2} author receipt blobs; mismatches={failed}')
commit_data = subprocess.check_output(['git', '-C', str(root), 'cat-file', 'commit', commit])
lines.append('Commit signature header: ' + ('present' if b'\ngpgsig ' in commit_data else 'absent; no signer authentication claimed'))
(packet / 'receipts' / 'evidence-verification.txt').write_text('\n'.join(lines) + '\n')
print('\n'.join(lines[:2] + lines[-2:]))
sys.exit(int(bool(failed)))
