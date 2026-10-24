#!/usr/bin/env python3
"""Normalize installation paths, retain original hashes, and make the manifest."""
import hashlib,json,re,shutil,sys
from pathlib import Path
repo,packet,simulator=map(lambda p:Path(p).resolve(),sys.argv[1:4])
changes=[]
for path in sorted((packet/'receipts').rglob('*')):
    if not path.is_file():continue
    target=packet/'scratch/raw'/path.relative_to(packet)
    original=target.read_bytes() if target.exists() else path.read_bytes()
    published=original.replace(str(packet).encode(),b'<packet>').replace(str(repo).encode(),b'<checkout>').replace(str(simulator.parent).encode(),b'<simulator-root>')
    published=re.sub(rb'/home/[^ /]+/\.local/share/containers/storage/overlay/[0-9a-f]+/diff/usr/share/verilator',b'<simulator-support>',published)
    if original!=published:
        target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(original)
        path.write_bytes(published)
        changes.append({'path':str(path.relative_to(packet)),'original_sha256':hashlib.sha256(original).hexdigest(),'published_sha256':hashlib.sha256(published).hexdigest()})
(packet/'receipt_redactions.json').write_text(json.dumps(changes,indent=2)+'\n')
lines=[]
for path in sorted(packet.rglob('*')):
    rel=path.relative_to(packet)
    if not path.is_file() or rel.parts[0]=='scratch' or path.name=='MANIFEST.sha256':continue
    lines.append(hashlib.sha256(path.read_bytes()).hexdigest()+'  '+str(rel))
(packet/'MANIFEST.sha256').write_text('\n'.join(lines)+'\n')
print(f'{len(lines)} publishable files; {len(changes)} receipts with installation paths normalized')
