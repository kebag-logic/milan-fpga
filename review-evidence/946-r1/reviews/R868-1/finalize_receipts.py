#!/usr/bin/env python3
"""Keep raw receipts in scratch, remove host paths from publishable copies,
and write a sha256sum manifest. Usage: python3 finalize_receipts.py PACKET
"""
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys
packet = Path(sys.argv[1]).resolve()
raw = packet/'scratch/raw-receipts'
raw.mkdir(parents=True, exist_ok=True)
records = []
for path in sorted(packet.glob('*.log')):
    original = path.read_bytes()
    target = raw/path.name
    if not target.exists():
        target.write_bytes(original)
    text = original.decode()
    text = re.sub(r'/home/[^\s]+?/usr/share/verilator', '<compiler-root>', text)
    text = text.replace(str(packet), '<packet>')
    text = text.replace('$REVIEWS/r868-1-946', '<repository>')
    path.write_text(text)
    records.append({'file':path.name,'raw_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),
                    'published_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                    'path_redacted':target.read_bytes()!=path.read_bytes()})
(packet/'receipt-provenance.json').write_text(json.dumps(records,indent=2)+'\n')
files = [p for p in sorted(packet.iterdir()) if p.is_file() and p.name != 'MANIFEST.sha256']
report = (packet/'REPORT.md').read_text()
assert report.startswith('[R868] NEGATIVE - exact head 66c6edf3f0d05915ee8ddb7346302013833cf66a\n')
assert report.rstrip().endswith('R868-1 FINISHED')
assert 'SKELETON' not in report
for p in files:
    text = p.read_text()
    assert not re.search(r'/home/[A-Za-z0-9_-]+/', text), p
(packet/'MANIFEST.sha256').write_text(''.join(
    hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n' for p in files))
print(f'Manifest lists {len(files)} publishable files. Raw logs retained under scratch/raw-receipts.')
