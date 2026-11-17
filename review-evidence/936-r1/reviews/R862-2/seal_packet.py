#!/usr/bin/env python3
"""Normalize workspace paths in receipts and seal publishable files.
Usage: python3 -B seal_packet.py CHECKOUT PACKET
scratch/ is excluded. Original and normalized receipt hashes are preserved.
"""
import hashlib
import json
from pathlib import Path
import sys

checkout, packet = (Path(x).resolve() for x in sys.argv[1:3])
hash_of = lambda b: hashlib.sha256(b).hexdigest()
provenance = []
for path in sorted([*packet.glob('*.log'), *(packet / 'receipts').glob('*.log')]):
    before = path.read_bytes()
    after = before.replace(str(packet).encode(), b'<packet>').replace(str(checkout).encode(), b'<checkout>')
    path.write_bytes(after)
    provenance.append(dict(file=path.relative_to(packet).as_posix(),
                           original_sha256=hash_of(before), published_sha256=hash_of(after),
                           workspace_paths_normalized=(before != after)))
(packet / 'receipt-provenance.json').write_text(json.dumps(provenance, indent=2) + '\n')
report = (packet / 'REPORT.md').read_text()
assert report.startswith('[R862] POSITIVE - exact head d1aa4c44307edf4a9390c19cbb2c82fe5c5464d0\n')
assert report.rstrip().endswith('R862-2 FINISHED')
assert 'SKELETON' not in report and 'SELFTEST_RESULT_PENDING' not in report
files = sorted(p for p in packet.rglob('*') if p.is_file()
               and 'scratch' not in p.relative_to(packet).parts and p.name != 'MANIFEST.sha256')
lines = [f'{hash_of(p.read_bytes())}  {p.relative_to(packet).as_posix()}' for p in files]
(packet / 'MANIFEST.sha256').write_text('\n'.join(lines) + '\n')
print(f'Sealed {len(files)} publishable files, including REPORT.md; scratch excluded.')
