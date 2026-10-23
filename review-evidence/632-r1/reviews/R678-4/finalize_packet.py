#!/usr/bin/env python3
"""Generate a publication manifest, excluding disposable scratch data."""
import hashlib
from pathlib import Path

root = Path(__file__).resolve().parent
report = (root / 'REPORT.md').read_text()
assert report.splitlines()[0] == '[R678] NEGATIVE - exact head 417ec52864efc09f1e3ecd0f755cb0daa7604426'
assert report.splitlines()[-1] == 'R678-4 FINISHED'
assert 'SKELETON' not in report
files = sorted(p for p in root.rglob('*') if p.is_file()
               and 'scratch' not in p.relative_to(root).parts
               and p.name != 'MANIFEST.sha256')
manifest = ''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(root)}\n' for p in files)
(root / 'MANIFEST.sha256').write_text(manifest)
for line in manifest.splitlines():
    digest, name = line.split('  ', 1)
    assert hashlib.sha256((root / name).read_bytes()).hexdigest() == digest
print(f'PASS: {len(files)} files listed and verified; scratch excluded; final report format valid.')
