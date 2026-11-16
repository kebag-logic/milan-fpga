#!/usr/bin/env python3
"""Recount public step receipts and independently regrade all route corners."""
import hashlib
import json
from pathlib import Path
import re
import sys

root=Path(sys.argv[1]).resolve()
out={'archive':'2b4066cafdd14e0351f6d73d0f59608f93577ce1','workflows':[],'routes':[],'receipts':[]}
def receipt(p):
    out['receipts'].append({'path':str(p.relative_to(root)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
for author,expected in (('author-r2',154),('author-r3',63)):
    logs=root/author/'receipts/workflows/logs'
    files=sorted(logs.glob('*.rc'))
    bad=[p.name for p in files if p.read_text().strip()!='0']
    assert len(files)==expected and not bad,(author,len(files),bad)
    out['workflows'].append({'author':author,'executed_steps':len(files),'bad':bad})
    for p in files: receipt(p)
for author in ('author-r1','author-r2'):
    routes=root/author/'receipts/route'
    images={}
    for p in sorted(routes.glob('*/*/signoff.txt')):
        text=p.read_text()
        corners=re.findall(r'^(\w+): WNS ([+-][\d.]+) ns .*?WHS ([+-][\d.]+) ns',text,re.M)
        assert len(corners)==4,p
        setup=min(float(x[1]) for x in corners)
        hold=min(float(x[2]) for x in corners)
        met=setup>=.030 and hold>=0
        image,directive=p.parent.parent.name,p.parent.name
        images.setdefault(image,[]).append(met)
        out['routes'].append(dict(author=author,image=image,directive=directive,setup_ns=setup,hold_ns=hold,meets=met))
        receipt(p)
    assert all(len(v)==3 and any(v) for v in images.values()),images
for pattern in ('author-r2/receipts/sweep/*.txt','author-r3/receipts/budget/leaveall-spread-after.md',
                'author-r3/receipts/budget/regrade-legs-at-6ceed753.txt',
                'author-r3/receipts/budget/seeds/*.txt',
                'author-r3/receipts/budget/legs/regrade-1x1-V1.txt',
                'author-r3/receipts/budget/selftest-at-6ceed753.txt'):
    for p in sorted(root.glob(pattern)): receipt(p)
print(json.dumps(out,indent=2))
print('PASS executed-step rc census and best-of-three four-corner route floors')
