#!/usr/bin/env python3
"""Redact machine paths in logs and hash only explicitly publishable files."""
import hashlib
from pathlib import Path
import re
root=Path(__file__).resolve().parent
for p in root.glob('*.log'):
    text=p.read_text()
    text=text.replace(str(root),'<review-packet>')
    text=re.sub(r'/home/[^/\s]+/\.local/share/containers/storage/overlay/[^/\s]+/diff', '<simulator-root>',text)
    p.write_text(text)
report=(root/'REPORT.md').read_text()
assert report.startswith('[R878] POSITIVE - exact head 64117b77cb9e5c421717835b5be032b5905c447d\n')
assert report.rstrip().endswith('R878-3 FINISHED')
assert 'SKELETON' not in report
files=sorted(p for p in root.iterdir() if p.is_file() and p.name!='MANIFEST.sha256')
with (root/'MANIFEST.sha256').open('w') as f:
    for p in files:
        f.write(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n')
print(f'Manifest: {len(files)} files; scratch excluded; report finalized.')
