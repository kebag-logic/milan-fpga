#!/usr/bin/env python3
"""Normalize review workspace paths in receipts, retain raw bytes privately, and hash the packet."""
import hashlib,json,sys
from pathlib import Path
p=Path(__file__).resolve().parent.parent
repo=Path(sys.argv[1]).resolve()
changes=[]
for f in (p/'receipts').rglob('*'):
 if not f.is_file() or f.name=='publication-normalization.json':continue
 raw=f.read_bytes()
 new=raw.replace(str(repo).encode(),b'<review-checkout>').replace(str(p).encode(),b'<packet>')
 if raw!=new:
  saved=p/'scratch/raw-receipts'/f.relative_to(p/'receipts');saved.parent.mkdir(parents=True,exist_ok=True);saved.write_bytes(raw)
  f.write_bytes(new)
  changes.append({'path':f.relative_to(p).as_posix(),'original_sha256':hashlib.sha256(raw).hexdigest(),'published_sha256':hashlib.sha256(new).hexdigest(),'change':'review workspace paths only; raw original retained under scratch/'})
(p/'receipts/publication-normalization.json').write_text(json.dumps(changes,indent=2)+'\n')
files=[p/'REPORT.md',p/'full.diff',p/'round5.diff']
for folder in ['scripts','receipts','public-inputs']:
 files.extend(f for f in (p/folder).rglob('*') if f.is_file())
files=sorted(files,key=lambda f:f.relative_to(p).as_posix())
(p/'MANIFEST.sha256').write_text(''.join(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+f.relative_to(p).as_posix()+'\n' for f in files))
print(f'Published files: {len(files)}; normalized receipts: {len(changes)}; scratch excluded')
