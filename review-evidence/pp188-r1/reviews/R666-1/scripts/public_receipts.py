#!/usr/bin/env python3
"""Keep raw logs in scratch and publish path-redacted copies with a hash mapping."""
import hashlib
import json
from pathlib import Path
import re
import sys

p=Path(sys.argv[1]).resolve(); rows=[]
for path in sorted((p/'receipts').rglob('*.log')):
    rel=path.relative_to(p); raw=p/'scratch/raw-receipts'/rel
    raw.parent.mkdir(parents=True,exist_ok=True)
    if not raw.exists():raw.write_bytes(path.read_bytes())
    original=raw.read_bytes(); text=original.decode()
    text=re.sub(r'/home/[^/\s]+/\.local/share/containers/storage/overlay/[^/\s]+/diff',
                '<scoped-sdk>',text)
    text=text.replace(str(p/'scratch'),'<review-scratch>')
    text=text.replace(str(p),'<review-packet>')
    data=text.encode();path.write_bytes(data)
    rows.append({'file':str(rel),'original_sha256':hashlib.sha256(original).hexdigest(),
                 'published_sha256':hashlib.sha256(data).hexdigest(),
                 'path_redacted':original!=data})
(p/'receipts/publication-map.json').write_text(json.dumps(rows,indent=2)+'\n')
print(f'Preserved {len(rows)} raw logs in scratch; published path-only redactions.')
