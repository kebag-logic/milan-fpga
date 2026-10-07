#!/usr/bin/env python3
"""Normalize two local paths, record hashes and manifest publishable files."""
import hashlib
import json
from pathlib import Path

packet = Path(__file__).resolve().parent
raw = packet / 'scratch' / 'raw_receipts'
raw.mkdir(parents=True, exist_ok=True)
records = []
for name in ('markdown_setup.log', 'composition_initial.log'):
    p = packet / name
    original = raw / name
    if not original.exists():
        original.write_bytes(p.read_bytes())
    data = original.read_bytes()
    published = data.replace(str(packet).encode(), b'<packet>').replace(str(Path.home()).encode(), b'<home>')
    p.write_bytes(published)
    records.append({'file':name, 'raw_sha256':hashlib.sha256(data).hexdigest(), 'published_sha256':hashlib.sha256(published).hexdigest(), 'normalization':'local packet/home path prefixes only'})
(packet / 'publication-normalization.json').write_text(json.dumps(records, indent=2) + '\n')
report = (packet / 'REPORT.md').read_text()
assert report.splitlines()[0] == '[R526] POSITIVE - exact head af5be4710c3516cc247c353213d6939fa8d23f57'
assert report.splitlines()[-1] == 'R526-3 FINISHED'
assert 'SKELETON' not in report
for lens in ('Conformance', 'RTL', 'Robustness', 'Tests', 'Docs'):
    assert '| ' + lens + ' | CLEAN |' in report
for receipt in packet.glob('*.rc'):
    expected = '1' if receipt.name == 'composition_initial.rc' else '0'
    assert receipt.read_text().strip() == expected, receipt.name
files = sorted(p for p in packet.rglob('*') if p.is_file() and 'scratch' not in p.relative_to(packet).parts and p.name != 'MANIFEST.sha256')
lines = []
for path in files:
    data = path.read_bytes()
    assert str(packet).encode() not in data, path.name
    assert str(Path.home()).encode() not in data, path.name
    lines.append(hashlib.sha256(data).hexdigest() + '  ' + path.relative_to(packet).as_posix())
(packet / 'MANIFEST.sha256').write_text('\n'.join(lines) + '\n')
print('Publication manifest:', len(files), 'files; no scratch content included')
print('Report first/last lines and five CLEAN ledger rows verified')
