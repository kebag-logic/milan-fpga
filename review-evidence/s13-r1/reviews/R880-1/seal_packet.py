#!/usr/bin/env python3
"""Preserve raw logs privately, normalize local paths in public receipts, and seal the packet."""
import hashlib
import json
from pathlib import Path
import re
import sys
repo, packet = map(Path,sys.argv[1:3])
raw=packet/'scratch/raw-receipts'
raw.mkdir(parents=True,exist_ok=True)
records=[]
for path in sorted(packet.glob('*.log')):
 original=(raw/path.name).read_bytes() if (raw/path.name).exists() else path.read_bytes()
 if not (raw/path.name).exists():
  (raw/path.name).write_bytes(original)
 data=original.replace(str(packet).encode(),b'<packet>').replace(str(repo).encode(),b'<review-root>')
 data=re.sub(rb'/home/[^/\s]+/\.local/share/containers/storage/overlay/[^/]+/diff/usr/share/verilator',
             b'<simulator-root>',data)
 data=re.sub(rb'/home/[^/\s]+',b'<home>',data)
 path.write_bytes(data)
 records.append({'file':path.name,'raw_sha256':hashlib.sha256(original).hexdigest(),
                 'published_sha256':hashlib.sha256(data).hexdigest(),'path_normalized':data!=original})
(packet/'receipt-normalization.json').write_text(json.dumps(records,indent=2)+'\n')
paths=sorted(p for p in packet.iterdir() if p.is_file() and p.name!='MANIFEST.sha256')
lines=[hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name for p in paths]
(packet/'MANIFEST.sha256').write_text('\n'.join(lines)+'\n')
assert 'SKELETON' not in (packet/'REPORT.md').read_text()
assert (packet/'REPORT.md').read_text().splitlines()[0]=='[R880] NEGATIVE - exact head 62477be4cb90336ca9b59ae7ab8377546e72557a'
assert (packet/'REPORT.md').read_text().splitlines()[-1]=='R880-1 FINISHED'
for p in paths:
 assert not re.search(rb'/home/[a-z][a-z0-9._-]*/',p.read_bytes()),p.name
print('Sealed',len(paths),'publishable files;',sum(p.stat().st_size for p in paths),'bytes; scratch excluded')
