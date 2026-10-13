#!/usr/bin/env python3
"""Normalize private absolute paths only, then list the publishable packet."""
import hashlib,json,pathlib,sys
p=pathlib.Path(__file__).resolve().parent.parent;repo=pathlib.Path(sys.argv[1]).resolve()
changes=[]
for f in sorted((p/'receipts').rglob('*')):
 if not f.is_file() or f.name=='publication-normalization.json':continue
 raw=f.read_bytes();out=raw
 for old,new in ((str(p).encode(),b'<packet>'),(str(repo).encode(),b'<review-checkout>')):out=out.replace(old,new)
 # The failed sandbox Git query exposes a private alternate-object directory.
 if f.name=='diff-check.log':
  import re
  out=re.sub(rb'/home/[^\n]+/\.git/objects',b'<alternate-object-store>',out)
 if out!=raw:
  saved=p/'scratch/raw-receipts'/f.relative_to(p/'receipts');saved.parent.mkdir(parents=True,exist_ok=True);saved.write_bytes(raw)
  f.write_bytes(out);changes.append(dict(path=f.relative_to(p).as_posix(),raw_sha256=hashlib.sha256(raw).hexdigest(),public_sha256=hashlib.sha256(out).hexdigest(),change='private absolute paths only'))
if changes:(p/'receipts/publication-normalization.json').write_text(json.dumps(changes,indent=2)+'\n')
files=[p/name for name in ('REPORT.md','independent-verdict.md','full.diff','round6.diff','history.txt','head.txt','gitlinks.txt')]
files += [f for sub in ('scripts','receipts') for f in (p/sub).rglob('*') if f.is_file() and '__pycache__' not in f.parts]
rows=[]
for f in sorted(set(files)):
 relative=f.relative_to(p).as_posix();assert not relative.startswith('scratch/')
 rows.append(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+relative)
(p/'MANIFEST.sha256').write_text('\n'.join(rows)+'\n')
print(json.dumps(dict(publishable_files=len(rows),normalized_this_run=len(changes))))
