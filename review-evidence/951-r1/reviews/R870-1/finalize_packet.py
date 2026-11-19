#!/usr/bin/env python3
"""Normalize receipt root paths, retain original logs in scratch, and hash publishable files."""
from pathlib import Path
import hashlib
import sys

checkout, packet = map(lambda p: Path(p).resolve(), sys.argv[1:3])
raw = packet / 'scratch/raw-receipts'
raw.mkdir(parents=True, exist_ok=True)
for path in packet.glob('*.log'):
    data = path.read_bytes()
    if not (raw / path.name).exists():
        (raw / path.name).write_bytes(data)
    data = data.replace(str(checkout).encode(), b'<checkout>').replace(str(packet).encode(), b'<packet>')
    path.write_bytes(data)
report = (packet / 'REPORT.md').read_text()
assert report.startswith('[R870] NEGATIVE - exact head 0d1eb8e4c5821e9431097950882659f2083d96ba\n')
assert report.rstrip().endswith('R870-1 FINISHED')
assert 'SKELETON' not in report and 'Reconciliation pending' not in report
for path in packet.glob('*.rc'):
    assert path.read_text().strip() == '0', path.name
files = sorted(p for p in packet.iterdir() if p.is_file() and p.name != 'MANIFEST.sha256')
(packet / 'MANIFEST.sha256').write_text(''.join(
    f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n' for p in files))
print('Manifest covers',len(files),'publishable files; scratch excluded.')
