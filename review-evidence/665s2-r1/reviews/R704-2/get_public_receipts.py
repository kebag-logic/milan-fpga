#!/usr/bin/env python3
"""Read immutable public evidence and verify hashes without reading peer reports."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
packet=Path(os.environ['REVIEW_PACKET'])
revision='33750832853802892619b60c16d7fa37d3911ccc'
prefix='review-evidence/665s2-r1/'
def read(name):
    return subprocess.check_output(['git','show',revision+':'+prefix+name])
rows=[]
for row in json.loads(read('MANIFEST.json')):
    name=row['file']
    if not(name.startswith('author-r2/') or name.startswith('reviews/R704-1/')):continue
    data=read(name);sha=hashlib.sha256(data).hexdigest()
    rows.append(dict(file=name,ok=sha==row['published_sha256'],sha256=sha))
    if name.startswith('author-r2/receipts/') or (name.startswith('reviews/R704-1/') and
        (name.endswith('.py') or name.endswith('REPRODUCE.txt') or '/notification-' in name
         or name.endswith('/controls/fanout.txt'))):
        path=packet/'scratch/public'/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
result=dict(revision=revision,checked=len(rows),failures=[r for r in rows if not r['ok']],files=rows)
(packet/'publication-check.json').write_text(json.dumps(result,indent=2)+'\n')
print(result['checked'],'checked;',len(result['failures']),'mismatches')
raise SystemExit(bool(result['failures']))
