#!/usr/bin/env python3
"""Hash publishable top-level receipts; never include disposable scratch trees."""
import hashlib
from pathlib import Path

packet = Path(__file__).resolve().parent
excluded = {'MANIFEST.sha256', 'REPORT.md', 'independent-pass.txt'}
rows = []
for path in sorted(packet.iterdir()):
    if path.is_file() and path.name not in excluded:
        rows.append(f'{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}\n')
(packet / 'MANIFEST.sha256').write_text(''.join(rows))
print(f'{len(rows)} publishable files; REPORT.md published separately; scratch excluded')
