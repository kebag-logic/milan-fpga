#!/usr/bin/env python3
"""Publish-safe path substitution and a closed manifest; never include scratch."""
import argparse
import hashlib
import json
from pathlib import Path
import re

p = argparse.ArgumentParser()
p.add_argument('--repo', type=Path, required=True)
p.add_argument('--sim', required=True)
a = p.parse_args()
packet = Path(__file__).resolve().parents[1]
changes = []
def sha(data):
    return hashlib.sha256(data).hexdigest()
for path in sorted((packet / 'receipts').rglob('*')):
    if not path.is_file() or path.name == 'publication-redactions.json':
        continue
    raw = path.read_bytes()
    text = raw.decode()
    text = re.sub(r'/home/[^\s\"\']+/usr/share/verilator', '<SIMULATOR_ROOT>', text)
    text = text.replace(str(Path(a.sim).resolve()), '<SIMULATOR>')
    text = text.replace(a.sim, '<SIMULATOR>')
    text = text.replace(str(a.repo.resolve()), '<REPO>')
    text = text.replace(str(packet), '<PACKET>')
    assert '/home/' not in text, path
    public = text.encode()
    if raw != public:
        relative = path.relative_to(packet)
        backup = packet / 'scratch/unpublished-originals' / relative
        backup.parent.mkdir(parents=True, exist_ok=True)
        backup.write_bytes(raw)
        path.write_bytes(public)
        changes.append({'file': str(relative), 'original_sha256': sha(raw),
                        'published_sha256': sha(public),
                        'change': 'Local installation/workspace prefixes only'})
(packet / 'receipts/publication-redactions.json').write_text(json.dumps(changes, indent=2) + '\n')
report = (packet / 'REPORT.md').read_text()
assert report.splitlines()[0] == '[R475] POSITIVE - exact head 2525eae9567865a8bc741901914bdf5a1caf2c26'
assert report.splitlines()[-1] == 'R475-3 FINISHED'
assert 'SKELETON' not in report
files = [packet / 'REPORT.md']
for directory in ['receipts', 'scripts']:
    files.extend(x for x in (packet / directory).rglob('*') if x.is_file() and '__pycache__' not in x.parts)
manifest = ''.join(f'{sha(path.read_bytes())}  {path.relative_to(packet)}\n' for path in sorted(files))
(packet / 'MANIFEST.sha256').write_text(manifest)
print('Publishable files:', len(files), 'path-substituted receipts:', len(changes))
