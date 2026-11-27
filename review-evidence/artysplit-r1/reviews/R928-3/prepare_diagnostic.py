"""Rebind only hashes in a disposable copy of published observation bytes.

This is a diagnostic, never validation of the original packet.
Usage: python3 prepare_diagnostic.py PUBLIC_EXTRACT NEW_SCRATCH_COPY
"""
import hashlib
import json
import os
import sys
from pathlib import Path

src, dst = map(Path, sys.argv[1:])
dst.mkdir(parents=True, exist_ok=False)
for file in src.rglob('*'):
    rel = file.relative_to(src)
    target = dst / rel
    if file.is_dir():
        target.mkdir(exist_ok=True)
    elif file.name not in ('manifest.json', 'census.json'):
        os.link(file, target)
census = json.loads((src / 'census.json').read_text())
changed = []
for row in census['cases']:
    path = src / row['manifest']
    manifest = json.loads(path.read_text())
    chunks = []
    record = manifest['extract']
    for part in record['parts']:
        data = (path.parent / part['file']).read_bytes()
        chunks.append(data)
        digest = hashlib.sha256(data).hexdigest()
        if digest != part['sha256']:
            changed.append(str(path.parent.relative_to(src) / part['file']))
        part.update(bytes=len(data), sha256=digest)
    data = b''.join(chunks)
    record.update(bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
    data = (json.dumps(manifest, separators=(',', ':')) + '\n').encode()
    (dst / row['manifest']).write_bytes(data)
    row['sha256'] = hashlib.sha256(data).hexdigest()
(dst / 'census.json').write_text(json.dumps(census))
print(f'DIAGNOSTIC ONLY: rebound {len(changed)} published observation parts; no observation bytes changed')
