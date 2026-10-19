#!/usr/bin/env python3
"""Retain raw local receipts privately and redact installation paths for publication."""
import hashlib
import json
from pathlib import Path
import re

p = Path(__file__).resolve().parent
raw = p / 'scratch/raw-receipts'
raw.mkdir(parents=True, exist_ok=True)
rows = []
for path in sorted((p / 'receipts').glob('*.log')):
    data = path.read_bytes()
    original = raw / path.name
    if not original.exists():
        original.write_bytes(data)
    else:
        data = original.read_bytes()
    text = data.decode('utf-8', errors='strict')
    if path.name in ('dynmap-baseline.log', 'probe-maps.log'):
        start = text.find('=== milan_datapath NxN integration')
        end = text.find('\nRESULT:', start)
        if start >= 0 and end >= 0:
            end = text.find('\n', end + 1)
            (p / 'receipts' / path.name.replace('.log', '-run.txt')).write_text(text[start:end] + '\n')
    text = re.sub(r'/home/[^\s\"\x27<>]+', '<compiler-installation-path>', text)
    text = text.replace(str(p), '<review-packet>')
    changed = text.encode()
    path.write_bytes(changed)
    rows.append({'file': str(path.relative_to(p)),
                 'raw_sha256': hashlib.sha256(data).hexdigest(),
                 'published_sha256': hashlib.sha256(changed).hexdigest(),
                 'installation_paths_redacted': data != changed})
(p / 'receipts/receipt-provenance.json').write_text(json.dumps(rows, indent=2) + '\n')
print('Prepared', len(rows), 'receipts; raw originals retained under scratch only')
