#!/usr/bin/env python3
"""Create and verify the publishable manifest; exclude every disposable scratch file."""
import hashlib
from pathlib import Path
import sys

out = Path(sys.argv[1]).resolve()
report = (out / 'REPORT.md').read_text()
assert report.splitlines()[0] == '[R884] POSITIVE - exact head 165476c755e4728a044c12ea6bc33ce0a0a9d28f'
assert report.splitlines()[-1] == 'R884-4 FINISHED'
assert 'SKELETON' not in report
for path in out.glob('*.rc'):
    assert path.read_text().strip() == '0', path.name
files = sorted(p for p in out.rglob('*') if p.is_file()
               and 'scratch' not in p.relative_to(out).parts and p.name != 'MANIFEST.sha256')
lines = []
for path in files:
    assert not path.is_symlink()
    lines.append(hashlib.sha256(path.read_bytes()).hexdigest() + '  ' + path.relative_to(out).as_posix())
(out / 'MANIFEST.sha256').write_text('\n'.join(lines) + '\n')
for line in lines:
    digest, name = line.split('  ', 1)
    assert hashlib.sha256((out / name).read_bytes()).hexdigest() == digest
print('PASS manifest:', len(files), 'publishable files; scratch excluded; report final and all recorded exits zero')
