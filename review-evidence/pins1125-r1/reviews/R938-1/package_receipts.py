#!/usr/bin/env python3
"""Retain raw receipts privately; publish copies with installation paths redacted."""
import hashlib
import json
import pathlib
import re
import shutil

packet = pathlib.Path(__file__).resolve().parent
receipts = packet / 'receipts'
raw = packet / 'scratch/raw-receipts'
assert not raw.exists(), 'package once, after all commands finish'
for source in sorted((packet / 'scratch/link-delay').glob('*/*.log')):
    dest = receipts / 'link-delay' / source.parent.name / source.name
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, dest)
shutil.copytree(receipts, raw)
records = []
for path in sorted(receipts.rglob('*')):
    if not path.is_file():
        continue
    before = path.read_bytes()
    text = before.decode()
    text = re.sub(r'/home/[^/\s]+/\.local/share/containers/storage/overlay/[^/\s]+/diff/usr/share/verilator', '<simulator-root>', text)
    text = re.sub(r'/home/[^/\s]+', '<home>', text)
    text = text.replace(str(packet), '<packet>')
    after = text.encode()
    path.write_bytes(after)
    records.append({'file': str(path.relative_to(packet)),
                    'raw_sha256': hashlib.sha256(before).hexdigest(),
                    'published_sha256': hashlib.sha256(after).hexdigest(),
                    'path_redacted': before != after})
(packet / 'RECEIPT-PROVENANCE.json').write_text(json.dumps(records, indent=2) + '\n')
print(len(records), 'receipts packaged; only installation and packet paths redacted')
