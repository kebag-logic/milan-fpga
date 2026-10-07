#!/usr/bin/env python3
"""Normalize local prefixes and hash every publishable receipt and script."""
import hashlib,json,os,sys
from pathlib import Path
p=Path(__file__).resolve().parents[1];repo=Path(sys.argv[1]).resolve()
replacements=[(str(repo),'${SOURCE}'),(str(p),'${PACKET}'),*json.loads(os.environ.get('REVIEW_PATH_PREFIXES','{}')).items()]
provenance_file=p/'receipts/normalization.json'
provenance={r['file']:r for r in json.loads(provenance_file.read_text())} if provenance_file.exists() else {}
for f in sorted((p/'receipts').rglob('*')):
 if not f.is_file() or f.name=='normalization.json':continue
 original=f.read_bytes();t=original.decode()
 for old,new in replacements:t=t.replace(old,new)
 normalized=t.encode()
 if normalized!=original:
  name=str(f.relative_to(p))
  record=provenance.get(name,{'file':name,'original_sha256':hashlib.sha256(original).hexdigest(),'change':'local path prefixes only'})
  record['published_sha256']=hashlib.sha256(normalized).hexdigest();provenance[name]=record
  f.write_bytes(normalized)
(p/'receipts/normalization.json').write_text(json.dumps(list(provenance.values()),indent=2)+'\n')
files=[p/'REPORT.md']+sorted(f for folder in ('scripts','receipts') for f in (p/folder).rglob('*') if f.is_file())
(p/'MANIFEST.sha256').write_text(''.join(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+str(f.relative_to(p))+'\n' for f in files))
print('Published files:',len(files))
