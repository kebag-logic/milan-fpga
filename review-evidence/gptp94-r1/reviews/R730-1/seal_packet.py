#!/usr/bin/env python3
"""Write and verify the publishable packet manifest; never include scratch."""
import hashlib
from pathlib import Path

packet = Path(__file__).resolve().parent
report = (packet / 'REPORT.md').read_text()
assert report.splitlines()[0] == '[R730] NEGATIVE - exact head 9d509029de967c50de7527edf2b8869aa9db9074'
assert report.splitlines()[-1] == 'R730-1 FINISHED'
assert 'SKELETON' not in report
files = sorted(p for p in packet.rglob('*') if p.is_file()
               and 'scratch' not in p.relative_to(packet).parts
               and p.name != 'MANIFEST.sha256')
manifest = ''.join(hashlib.sha256(p.read_bytes()).hexdigest() + '  '
                   + p.relative_to(packet).as_posix() + '\n' for p in files)
(packet / 'MANIFEST.sha256').write_text(manifest)
for line in manifest.splitlines():
    digest, name = line.split('  ', 1)
    assert hashlib.sha256((packet / name).read_bytes()).hexdigest() == digest
print('Manifest verified:', len(files), 'publishable files;',
      sum(p.stat().st_size for p in files), 'bytes; scratch excluded')
