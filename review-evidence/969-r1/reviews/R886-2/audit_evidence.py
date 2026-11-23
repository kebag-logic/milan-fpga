#!/usr/bin/env python3
"""Check immutable public receipts: CHECKOUT PACKET.
Requires evidence commit 1cd9d3f already fetched into CHECKOUT.
Only receipts and prior probe source are read; no review reports or handoff prose.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
root, packet = (Path(x).resolve() for x in sys.argv[1:3])
rev = '1cd9d3fd3e46aaeeff6650f1bc60cce139645f0e'
base = 'review-evidence/969-r1/'
def get(name):
    return subprocess.check_output(['git','-C',str(root),'show',rev+':'+base+name])
manifest = get('MANIFEST.json')
(packet/'evidence-manifest.json').write_bytes(manifest)
probes = {'reviews/R886-1/probes.cpp','reviews/R885-1/scripts/stale_count_probe.cpp','reviews/R886-1/verify_tree.py'}
lines = []
for row in json.loads(manifest):
    name = row['file']
    if not name.startswith('author-r2/receipts/') and name not in probes:
        continue
    data = get(name)
    digest = hashlib.sha256(data).hexdigest()
    if digest != row['published_sha256']:
        raise SystemExit('Hash mismatch: '+name)
    target = packet/'scratch/public-evidence'/name
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_bytes(data)
    lines.append('OK '+digest+' '+name)
(packet/'evidence-verification.txt').write_text('\n'.join(lines)+'\n')
print('Verified',len(lines),'published files')
