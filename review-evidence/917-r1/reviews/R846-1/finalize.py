#!/usr/bin/env python3
"""Normalize local paths in logs, retain raw originals in scratch, hash the public packet.

Usage: python3 finalize.py CHECKOUT PACKET
Only top-level packet files are published. scratch is never in the manifest.
"""
import hashlib
from pathlib import Path
import re
import sys
repo,packet=Path(sys.argv[1]).resolve(),Path(sys.argv[2]).resolve()
raw=packet/'scratch/raw'
raw.mkdir(parents=True,exist_ok=True)
for p in sorted(packet.glob('*.log')):
    original=p.read_bytes()
    # Keep the original once; re-finalization of a normalized log is idempotent.
    if not (raw/p.name).exists():(raw/p.name).write_bytes(original)
    text=original.decode('utf-8',errors='replace')
    text=text.replace(str(repo),'<checkout>').replace(str(packet),'<packet>')
    text=re.sub(r'/home/[^\s\"\x27]+','<local-tool-path>',text)
    text=text.replace('$VALIDATION_TOOLS/','<tools>/')
    p.write_text(text)
files=[p for p in sorted(packet.iterdir()) if p.is_file() and p.name!='MANIFEST.sha256']
manifest=''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n' for p in files)
(packet/'MANIFEST.sha256').write_text(manifest)
assert 'SKELETON' not in (packet/'REPORT.md').read_text()
assert (packet/'REPORT.md').read_text().splitlines()[-1]=='R846-1 FINISHED'
print('Published files:',len(files),'(including REPORT.md); scratch excluded.')
