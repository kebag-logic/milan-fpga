#!/usr/bin/env python3
"""Seal public-safe receipts, retaining unsanitized originals in excluded scratch."""
import hashlib
import shutil
import sys
from pathlib import Path

repo, packet = (Path(x).resolve() for x in sys.argv[1:3])
raw = packet / 'scratch/raw-receipts'
raw.mkdir(parents=True, exist_ok=True)
for f in (packet / 'receipts').rglob('*'):
    if not f.is_file():
        continue
    rel = f.relative_to(packet / 'receipts')
    original = raw / rel
    original.parent.mkdir(parents=True, exist_ok=True)
    if not original.exists():
        shutil.copyfile(f, original)
    text = original.read_text()
    for old, new in ((str(packet / 'scratch'), '<scratch>'), (str(packet), '<packet>'),
                     (str(repo), '<review-checkout>'), ('$WORKSPACE_HOME', '<home>'),
                     ('$VALIDATION_TOOLS', '<tools>')):
        text = text.replace(old, new)
    f.write_text(text)
report = (packet / 'REPORT.md').read_text()
assert report.splitlines()[0] == '[R882] POSITIVE - exact head 287ca1ee96e69f71a5036061d2bf33c564965755'
assert report.splitlines()[-1] == 'R882-1 FINISHED'
assert 'SKELETON' not in report
files = [packet / 'REPORT.md', packet / 'public-scope.json']
files += sorted(packet.glob('*.py'))
files += sorted(f for f in (packet / 'receipts').rglob('*') if f.is_file())
lines = [hashlib.sha256(f.read_bytes()).hexdigest() + '  ' + f.relative_to(packet).as_posix() for f in files]
(packet / 'MANIFEST.sha256').write_text('\n'.join(lines) + '\n')
print('Sealed', len(files), 'publishable files; scratch excluded')
