#!/usr/bin/env python3
"""Seal only the report, scripts and receipts; scratch is never publishable."""
import hashlib
import subprocess
import sys
from pathlib import Path

packet = Path(sys.argv[1]).resolve()
report = (packet / 'REPORT.md').read_text()
assert report.splitlines()[0] == '[R525] POSITIVE - exact head 6c94e9f5f496ac25f8c4e31f9e3685c725de29f3'
assert report.splitlines()[-1] == 'R525-2 FINISHED'
assert 'SKELETON' not in report
for lens in ('Conformance', 'RTL', 'Robustness', 'Tests', 'Docs'):
    assert f'| {lens} | CLEAN |' in report
files = [packet / 'REPORT.md']
for name in ('scripts', 'receipts'):
    files += [path for path in (packet / name).rglob('*') if path.is_file()]
lines = []
for path in sorted(files):
    assert not path.is_symlink()
    relative = path.relative_to(packet).as_posix()
    assert not relative.startswith('scratch/') and '__pycache__' not in relative
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    lines.append(f'{digest}  {relative}')
(packet / 'MANIFEST.sha256').write_text('\n'.join(lines) + '\n')
result = subprocess.run(['sha256sum', '--check', '--strict', 'MANIFEST.sha256'],
                        cwd=packet, capture_output=True, text=True, check=True)
assert len(result.stdout.splitlines()) == len(lines)
print(f'PASS: {len(lines)} publishable files sealed and every manifest checksum verified; scratch excluded')
