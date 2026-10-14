#!/usr/bin/env python3
"""Validate a completed report and hash its explicit publication set."""
import hashlib
import json
from pathlib import Path

packet = Path(__file__).resolve().parents[1]
report = (packet / 'REPORT.md').read_text()
head = '4c5d70b50230fbd5da347852d39daf7f23b3df0b'
assert report.splitlines()[0] in {f'[R593] POSITIVE - exact head {head}', f'[R593] NEGATIVE - exact head {head}'}
assert report.splitlines()[-1] == 'R593-5 FINISHED'
assert 'SKELETON' not in report and 'HOSTED_SECTION_PENDING' not in report
for label in ['suite-shards', 'ci-check', 'ci-selftest', 'serial-preflight', 'delta-checks', 'focused-baseline', 'generated-limits', 'identity']:
    assert (packet / 'receipts' / f'{label}.rc').read_text().strip() == '0', label
publication = sorted([packet / 'REPORT.md', *[p for root in ['scripts', 'receipts'] for p in (packet / root).rglob('*') if p.is_file() and '__pycache__' not in p.parts]])
for path in publication:
    text = path.read_text(errors='replace')
    assert ('/' + 'home/' + 'alex/') not in text, path
    assert 'scratch/' not in str(path.relative_to(packet)), path
manifest = ''.join(hashlib.sha256(p.read_bytes()).hexdigest() + '  ' + str(p.relative_to(packet)) + '\n' for p in publication)
(packet / 'MANIFEST.sha256').write_text(manifest)
for line in manifest.splitlines():
    digest, relative = line.split('  ', 1)
    assert hashlib.sha256((packet / relative).read_bytes()).hexdigest() == digest
print(f'PASS: {len(publication)} publication files, all SHA-256 digests verified; scratch excluded')
