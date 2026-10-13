#!/usr/bin/env python3
"""Compare all five focused linked-image pairs and emit portable digests."""
import argparse
import hashlib
import json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('build',type=Path);p.add_argument('--author',type=Path)
a=p.parse_args();rows=[]
public=json.loads(a.author.read_text()) if a.author else []
for head in sorted((a.build/'head').glob('*/ctrl_app.elf')):
    base=a.build/'base'/head.parent.name/'ctrl_app.elf'
    h=head.read_bytes();b=base.read_bytes();assert h==b,head.parent.name
    row={'shape':head.parent.name,'head_bytes':len(h),'base_bytes':len(b),
         'head_sha256':hashlib.sha256(h).hexdigest(),'base_sha256':hashlib.sha256(b).hexdigest()}
    if public:row['public_sha256']=next(x['after_sha256'] for x in public if x['shape']==head.parent.name)
    rows.append(row)
assert len(rows)==5
print(json.dumps(rows,indent=2))
