#!/usr/bin/env python3
"""Redact private installation paths, retain raw copies, and hash publication files.
Usage: python3 package_receipts.py PACKET
Run only after the report and all receipts are final.
"""
import hashlib
import json
from pathlib import Path
import re
import sys

packet = Path(sys.argv[1]).resolve()
records = []
for path in sorted((packet/'probes').glob('*.log')):
    original = path.read_bytes()
    public = re.sub(rb'/home/[^/\s]+/\.local/share/containers/storage/overlay/[^/\s]+/diff/usr/share/verilator', b'<simulator-root>', original)
    public = re.sub(rb'/home/[^/\s]+', b'<home>', public)
    if original != public:
        raw = packet/'scratch/raw_receipts'/path.name
        raw.parent.mkdir(parents=True,exist_ok=True)
        raw.write_bytes(original)
        path.write_bytes(public)
        records.append({'file':path.relative_to(packet).as_posix(), 'original_sha256':hashlib.sha256(original).hexdigest(), 'published_sha256':hashlib.sha256(public).hexdigest(), 'change':'private installation path only'})
if records:
    (packet/'receipt_redactions.json').write_text(json.dumps(records,indent=2)+'\n')
files=sorted(f for f in packet.rglob('*') if f.is_file() and 'scratch' not in f.relative_to(packet).parts and f.name!='MANIFEST.sha256')
for f in files:
    assert not f.is_symlink()
    if f.suffix != '.py':
        assert not re.search(rb'/home/[^/\s]+/',f.read_bytes()),f.name
(packet/'MANIFEST.sha256').write_text(''.join(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+f.relative_to(packet).as_posix()+'\n' for f in files))
print(f'Publication manifest: {len(files)} files, {sum(f.stat().st_size for f in files)} bytes; scratch excluded.')
