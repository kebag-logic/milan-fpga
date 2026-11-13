#!/usr/bin/env python3
"""Write and independently recheck the publication inventory, excluding scratch."""
import hashlib
from pathlib import Path

root = Path(__file__).resolve().parent
report = (root / 'REPORT.md').read_text()
assert report.splitlines()[0] == '[R712] POSITIVE - exact head 084cf7a8455e9fa8e24a0e5bcf57c9557816c819'
assert report.splitlines()[-1] == 'R712-10 FINISHED'
assert 'SKELETON' not in report
files = sorted(p for p in root.rglob('*') if p.is_file()
               and 'scratch' not in p.relative_to(root).parts
               and p.name != 'MANIFEST.sha256')
lines = [hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(root).as_posix()
         for p in files]
(root / 'MANIFEST.sha256').write_text('\n'.join(lines)+'\n')
for line in (root / 'MANIFEST.sha256').read_text().splitlines():
    expected, name = line.split('  ', 1)
    assert hashlib.sha256((root / name).read_bytes()).hexdigest() == expected
print('PASS', len(files), 'publication files hashed; scratch excluded; report boundaries valid')
