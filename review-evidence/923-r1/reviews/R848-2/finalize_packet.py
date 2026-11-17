#!/usr/bin/env python3
"""Validate the review packet and write its publication manifest, excluding disposable data."""
import hashlib
import json
from pathlib import Path

packet = Path(__file__).resolve().parent
report = (packet / 'REPORT.md').read_text()
assert report.splitlines()[0] == '[R848] POSITIVE - exact head d06ded5ad3d6eb26bfd79787260adcdcc7d3f80b'
assert report.splitlines()[-1] == 'R848-2 FINISHED'
assert 'SKELETON' not in report
for lens in ('Conformance', 'RTL', 'Robustness', 'Tests', 'Docs'):
    assert f'| {lens} | CLEAN |' in report
results = json.loads((packet / 'probe-summary.json').read_text())
assert len(results) == 5 and all(r['rc'] == 0 for r in results)
for result in results:
    name = result['probe']
    assert (packet / (name + '.rc')).read_text().strip() == '0'
    assert f'PROBE {name} PASS' in (packet / (name + '.log')).read_text()
paths = sorted(p for p in packet.rglob('*') if p.is_file()
               and 'scratch' not in p.relative_to(packet).parts
               and '__pycache__' not in p.relative_to(packet).parts
               and p.name != 'MANIFEST.sha256')
lines = [hashlib.sha256(p.read_bytes()).hexdigest() + '  ' + p.relative_to(packet).as_posix() for p in paths]
(packet / 'MANIFEST.sha256').write_text('\n'.join(lines) + '\n')
print('Publication manifest:', len(paths), 'files; all scratch files excluded.')
print('Verdict, five-lens ledger, receipts and terminal marker validated.')
