#!/usr/bin/env python3
"""Prepare portable public receipts and checksum the publication set.

Raw receipt bytes are retained in scratch/raw-receipts. Published log text
differs only by checkout and packet path substitutions, never by result.
"""
import hashlib
from pathlib import Path
import shutil

packet = Path(__file__).resolve().parent
root = Path.cwd()
raw = packet / 'scratch/raw-receipts'
raw.mkdir(parents=True, exist_ok=True)
for path in sorted((packet / 'receipts').glob('*')):
    if not path.is_file():
        continue
    original = raw / path.name
    if not original.exists():
        shutil.copyfile(path, original)
    text = original.read_text()
    text = text.replace(str(root), '<checkout>').replace(str(packet), '<packet>')
    path.write_text(text)
files = sorted([packet / 'REPORT.md', *packet.glob('*.py'), *(packet / 'receipts').glob('*')])
with (packet / 'MANIFEST.sha256').open('w') as manifest:
    for path in files:
        if path.is_file():
            manifest.write(hashlib.sha256(path.read_bytes()).hexdigest() + '  ' + str(path.relative_to(packet)) + '\n')
print('Manifest entries:', sum(path.is_file() for path in files))
report = (packet / 'REPORT.md').read_text()
assert report.splitlines()[0] == '[R896] POSITIVE - exact head 9a71daa9aa2379e2a57eb93ccafe83101bcb37f7'
assert report.splitlines()[-1] == 'R896-1 FINISHED'
assert 'SKELETON' not in report
assert report.count('| CLEAN |') == 5
print('Report format and five-lens ledger: PASS')
