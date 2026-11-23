#!/usr/bin/env python3
"""List and verify every publishable receipt; never include disposable trees."""
import hashlib
from pathlib import Path
import sys

packet=Path(sys.argv[1]).resolve()
report=(packet/'REPORT.md').read_text()
assert report.splitlines()[0]=='[R896] POSITIVE - exact head 87b2fc0f2867ef132b9388e22ec262fc626cbb57'
assert report.splitlines()[-1]=='R896-3 FINISHED'
assert 'SKELETON' not in report
for lens in ['Conformance','RTL','Robustness','Tests','Docs']:
    assert '| '+lens+' | CLEAN |' in report
files=sorted(p for p in packet.rglob('*') if p.is_file() and 'scratch' not in p.relative_to(packet).parts
             and p.name not in ['REPORT.md','MANIFEST.sha256'])
lines=[]
for p in files:
    assert not p.is_symlink()
    lines.append(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(packet).as_posix())
(packet/'MANIFEST.sha256').write_text('\n'.join(lines)+'\n')
for line in lines:
    digest,name=line.split('  ',1)
    assert hashlib.sha256((packet/name).read_bytes()).hexdigest()==digest
print(f'PASS: {len(files)} manifest-listed receipts/scripts plus REPORT.md; scratch excluded')
