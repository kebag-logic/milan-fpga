#!/usr/bin/env python3
"""Prepare public receipts and manifest: CHECKOUT PACKET.

Only path prefixes are redacted. Originals stay under unpublished scratch.
Discovery snapshots and scratch builds are never selected for publication.
"""
import hashlib
from pathlib import Path
import re
import sys

checkout, packet = (Path(s).resolve() for s in sys.argv[1:3])
selected_json = {
    'focused-results.json', 'probe-results.json', 'plants-results.json',
    'small-gate-results.json', 'tree-integrity.json', 'hosted-snapshot.json',
    'evidence-manifest.json',
}
selected_txt = {'published-gate-extracts.txt', 'evidence-download-verification.txt'}
files = []
for f in packet.iterdir():
    if f.is_file() and (f.suffix in ('.py', '.cpp', '.log', '.rc') or
                       f.name in selected_json | selected_txt | {'REPORT.md', 'RECEIPTS.md'}):
        files.append(f)
files.extend(f for f in (packet / 'plant-logs').rglob('*') if f.is_file())
originals = packet / 'scratch/original-receipts'
for f in files:
    if f.suffix in ('.py', '.cpp'):
        continue
    text = f.read_text()
    safe = text.replace(str(checkout), '<checkout>').replace(str(packet), '<packet>')
    safe = re.sub(r'/home/[^/\s"\x27]+', '<home>', safe)
    safe = safe.replace('$VALIDATION_TOOLS', '<tools>')
    if f.name == 'REPORT.md':
        safe = safe.replace('\u2014', '-').replace('\u2013', '-')
    if safe != text:
        original = originals / f.relative_to(packet)
        original.parent.mkdir(parents=True, exist_ok=True)
        if not original.exists():
            original.write_bytes(f.read_bytes())
        f.write_text(safe)
rows = [f'{hashlib.sha256(f.read_bytes()).hexdigest()}  {f.relative_to(packet).as_posix()}\n'
        for f in sorted(files)]
(packet / 'MANIFEST.sha256').write_text(''.join(rows))
print(f'Publishable artifacts: {len(rows)}; scratch and discovery snapshots excluded.')
