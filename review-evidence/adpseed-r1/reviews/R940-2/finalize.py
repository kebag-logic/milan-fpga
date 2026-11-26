#!/usr/bin/env python3
"""Normalize machine paths in diagnostic receipts and write publication manifest."""
from pathlib import Path
import hashlib
import shutil
import sys

source,packet,sdk=map(lambda p:Path(p).resolve(),sys.argv[1:])
raw=packet/'scratch/raw-diagnostics'
raw.mkdir(parents=True,exist_ok=True)
for p in (packet/'receipts').glob('*'):
    if p.suffix not in ('.log','.xml'): continue
    shutil.copy2(p,raw/p.name)
    text=p.read_text()
    for absolute,label in [(str(source),'SOURCE'),(str(packet),'PACKET'),(str(sdk),'DEPENDENCY')]:
        text=text.replace(absolute,label)
    p.write_text(text)
report=(packet/'REPORT.md').read_text()
assert report.startswith('[R940] POSITIVE - exact head 9590206015ead2cfd2ef955c2f4ef8d8c4e4762c\n')
assert 'SKELETON' not in report and report.rstrip().endswith('R940-2 FINISHED')
files=sorted([*packet.glob('*.py'),packet/'INDEPENDENT-PASS.md',*(p for p in (packet/'receipts').rglob('*') if p.is_file())])
manifest=''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(packet).as_posix()+'\n' for p in files)
(packet/'MANIFEST.sha256').write_text(manifest)
print(len(files),'publishable scripts, checkpoint and receipts; REPORT.md published separately')
