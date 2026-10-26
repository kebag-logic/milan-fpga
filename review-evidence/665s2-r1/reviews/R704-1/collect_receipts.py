#!/usr/bin/env python3
"""Collect completed receipts; omit disposable trees and replace local path prefixes."""
import hashlib
import json
import os
from pathlib import Path
import shutil

root = Path(os.environ['REVIEW_ROOT'])
packet = Path(os.environ['REVIEW_PACKET'])
scratch = packet / 'scratch'
replacements = [(str(scratch), '${REVIEW_PACKET}/scratch'), (str(packet), '${REVIEW_PACKET}'),
                (str(root), '${REVIEW_ROOT}')]
replacements += [(os.environ[key], '${' + key + '}')
                 for key in ('PRODUCT_ENV', 'RV32_SDK', 'PINNED_SIMULATOR', 'DOCS_ENV', 'USER_HOME')
                 if os.environ.get(key)]

def copy(source, destination):
    destination.parent.mkdir(parents=True, exist_ok=True)
    data = source.read_bytes()
    changed = False
    for old, new in replacements:
        if old.encode() in data:
            data = data.replace(old.encode(), new.encode())
            changed = True
    destination.write_bytes(data)
    return {'path': str(destination.relative_to(packet)), 'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
            'published_sha256': hashlib.sha256(data).hexdigest(), 'path_prefixes_replaced': changed}

receipts = []
for arm in ('A1', 'A8'):
    results = scratch / arm / 'results'
    assert (results / 'results.json').exists(), (arm, 'campaign not finished')
    for source in sorted(results.iterdir()):
        if source.is_file() and source.suffix in ('.log', '.json', '.txt', '.md'):
            receipts.append(copy(source, packet / 'measurements' / arm / source.name))

for name in ('A1', 'A8', 'asbuilt', 'slow', 'own-slow'):
    receipts.append(copy(scratch / name / 'build.json', packet / 'builds' / (name + '.json')))
    for basename in ('image.log', 'runtime.log', 'litex.log', 'make.log', 'verilate.log', 'soc.json', 'csr.json'):
        source = scratch / name / basename
        if source.exists():
            receipts.append(copy(source, packet / 'builds' / name / basename))
for source in sorted(scratch.glob('*.raw.log')):
    receipts.append(copy(source, packet / 'logs' / source.name.replace('.raw', '')))
for name in ('fanout.txt', 'rom-probe.txt'):
    receipts.append(copy(scratch / name, packet / 'controls' / name))
for name in ('asbuilt', 'slow'):
    for source in sorted((scratch / name / 'results').glob('*')):
        if source.is_file():
            receipts.append(copy(source, packet / 'controls' / name / source.name))
for name in ('A1', 'own-slow'):
    for source in sorted((scratch / name / 'own-probe').glob('*.txt')):
        receipts.append(copy(source, packet / 'controls' / name / source.name))
(packet / 'receipt-index.json').write_text(json.dumps(receipts, indent=2) + '\n')
print('Collected', len(receipts), 'receipts; numeric simulation logs retain exact bytes.')
