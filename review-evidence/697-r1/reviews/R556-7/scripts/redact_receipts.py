#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Replace host location prefixes in text receipts with placeholders; record hashes.
usage: redact_receipts.py PACKET CLONE REVIEWS_DIR DATA_DIR HOME_DIR"""
import hashlib, json, sys
from pathlib import Path
packet = Path(sys.argv[1]).resolve()
rules = list(zip([str(packet), *sys.argv[2:6]], ['<PACKET>', '<CLONE>', '<REVIEWS>', '<DATA>', '<HOME>']))
record = []
for path in sorted((packet / 'receipts').rglob('*')):
    if not path.is_file() or path.name == 'location-redactions.json':
        continue
    data = path.read_bytes()
    try:
        text = data.decode()
    except UnicodeDecodeError:
        continue
    new = text
    for old, placeholder in rules:
        new = new.replace(old, placeholder)
    if new != text:
        path.write_text(new)
        record.append({'file': str(path.relative_to(packet)), 'original_sha256': hashlib.sha256(data).hexdigest(),
                       'redacted_sha256': hashlib.sha256(new.encode()).hexdigest()})
(packet / 'receipts/location-redactions.json').write_text(json.dumps(
    {'placeholders': [p for _, p in rules], 'files': record}, indent=1) + '\n')
print('redacted files:', len(record))
