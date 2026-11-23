#!/usr/bin/env python3
"""Prepare only the completed review receipts and a relative SHA-256 manifest."""
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

root, packet = (Path(x).resolve() for x in sys.argv[1:])
excluded = {'public-0.json', 'public-1.json', 'independent-verdict.md',
            'harness-selftest.log', 'harness-selftest.rc', 'MANIFEST.sha256'}
selected = sorted(p for p in packet.iterdir() if p.is_file() and p.name not in excluded)
assert all(p.suffix in {'.md', '.py', '.json', '.log', '.rc', '.txt', '.gz'} for p in selected)
originals = packet / 'scratch/publication-originals'
originals.mkdir(parents=True, exist_ok=True)
redactions = []
for path in selected:
    if path.suffix != '.log':
        continue
    original = originals / path.name
    if not original.exists():
        shutil.copyfile(path, original)
    before = original.read_bytes()
    text = before.decode()
    text = text.replace(str(packet / 'scratch'), '<scratch>')
    text = text.replace(str(root), '<checkout>').replace(str(packet), '<packet>')
    text = re.sub(r'/home/[^/\s]+/', '<home>/', text)
    after = text.encode()
    path.write_bytes(after)
    redactions.append(dict(file=path.name, original_sha256=hashlib.sha256(before).hexdigest(),
                           published_sha256=hashlib.sha256(after).hexdigest(),
                           path_prefixes_redacted=before != after))
provenance = packet / 'publication-paths.json'
provenance.write_text(json.dumps(dict(policy='Only host-diagnostic local path prefixes replaced; '
    'native gzip logs are unchanged raw bytes.', files=redactions), indent=2) + '\n')
selected = sorted(set(selected) | {provenance})
for path in selected:
    if path.suffix == '.rc':
        assert path.read_text().strip() == '0', path.name
report = (packet / 'REPORT.md').read_text()
assert report.startswith('[R899] NEGATIVE - exact head 4cca956932073b3f704f12f81c53f2934cfa215c\n')
assert report.rstrip().endswith('R899-1 FINISHED') and 'SKELETON' not in report
manifest = ''.join(f'{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}\n' for path in selected)
(packet / 'MANIFEST.sha256').write_text(manifest)
print(f'Packaged {len(selected)} files; excluded scratch and unfinished/nonpublication receipts.')
