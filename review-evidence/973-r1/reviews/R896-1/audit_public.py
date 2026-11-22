#!/usr/bin/env python3
"""Audit downloaded public receipts against their published manifest.

Place the selected files and MANIFEST.json beneath packet/scratch/public,
preserving paths relative to review-evidence/973-r1 at the evidence commit.
Only the audit result is republished, not the disposable downloads.
"""
import hashlib
import json
from pathlib import Path
import re

packet = Path(__file__).resolve().parent
public = packet / 'scratch/public'
manifest = json.loads((public / 'MANIFEST.json').read_text())
base_url = 'https://github.com/kebag-logic/milan-fpga/blob/62593bf0adb29cb13e2f1ebaa95c76c496f5cdf0/review-evidence/973-r1/'
count = 0
for row in manifest:
    path = public / row['file']
    if not path.exists():
        continue
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    assert actual == row['published_sha256'], row['file']
    print('SHA256 PASS', actual, base_url + row['file'])
    count += 1
print('Verified public receipt files:', count)
receipts = public / 'author-r1/receipts'
for point, expected in [('1x1', 88), ('8x8-1if', 86)]:
    text = (receipts / f'cpu/compare/probes-{point}.md').read_text()
    rows = [line.split('|')[1:-1] for line in text.splitlines() if line.startswith('| `')]
    assert len(rows) == expected, (point, len(rows))
    assert all(float(r[1]) < float(r[4]) and float(r[2]) < float(r[4]) for r in rows)
    assert all(r[5].strip() == 'fits / fits' for r in rows)
    print('CPU', point, len(rows), 'paired rows: all base/head figures below bounds; zero verdict changes')
    print('Largest absolute rounded delta ms:', max(abs(float(r[3])) for r in rows))
for leg in (0, 1):
    data = json.loads((receipts / f'gates/builder-leg-{leg}.json').read_text())
    print('Published builder leg', leg, 'head', data['head'])
    for gate in data['driver']['gates']:
        assert gate['verdict'] == 'pass', gate
        if gate.get('not_run'):
            print('NOT RUN:', gate['gate'], gate['not_run'])
print('These are author source receipts; no manager source bank is asserted.')
