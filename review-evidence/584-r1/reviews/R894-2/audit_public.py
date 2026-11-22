#!/usr/bin/env python3
"""Check immutable public receipt hashes; do not read review reports."""
import hashlib, json, re, subprocess, sys
from pathlib import Path
repo=Path(sys.argv[1]).resolve()
out=Path(sys.argv[2]).resolve()
commit='e3127c9139ae456ef671b098eab55bed6d41d0f4'
prefix='review-evidence/584-r1/'
def blob(path):
    return subprocess.check_output(['git','show',commit+':'+prefix+path],cwd=repo)
manifest=json.loads(blob('MANIFEST.json'))
rows=[r for r in manifest if r['file'].startswith(('author-r1/receipts/','author-r2/receipts/'))]
bad=[]
for r in rows:
    actual=hashlib.sha256(blob(r['file'])).hexdigest()
    if actual!=r['published_sha256']: bad.append((r['file'],actual,r['published_sha256']))
print('Publication',commit,'manifest receipts',len(rows),'mismatches',len(bad))
for x in bad: print(x)
for path,root in [('author-r1/receipts/INDEX.md','author-r1/receipts/'),('author-r2/receipts/f5/round1-INDEX-corrected.md','author-r1/receipts/'),('author-r2/receipts/INDEX.md','author-r2/receipts/')]:
    entries=re.findall(r'\| `([^`]+)` \| (\d+) \| `([0-9a-f]{64})` \|',blob(path).decode())
    faults=[]
    for name,size,sha in entries:
        b=blob(root+name)
        if len(b)!=int(size) or hashlib.sha256(b).hexdigest()!=sha:
            faults.append((name,int(size),len(b),sha,hashlib.sha256(b).hexdigest()))
    print(path,'rows',len(entries),'mismatches',len(faults))
    for f in faults: print(f)
selected=['author-r2/receipts/rtl/ship8-64d539f1.log','author-r2/receipts/rtl/ship8-mutants-64d539f1.txt','author-r2/receipts/rtl/milan_dp_render-suite-25ad9c9a.txt','author-r2/receipts/rtl/ship8-ci-driver-e2a0858c.txt','author-r2/receipts/gates/builder-legs-union-25ad9c9a.txt','author-r2/receipts/docs/docswf-64d539f1.txt','author-r1/receipts/firmware/ledger-base-dd163e41.log','author-r1/receipts/firmware/ledgerF.log','author-r1/receipts/builder/artifacts-base-vs-head.txt','author-r2/receipts/f5/index-check.md']
for p in selected:
    dest=out/'public-receipts'/p
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_bytes(blob(p))
raw=subprocess.check_output(['git','cat-file','commit',commit],cwd=repo)
print('Commit signature header present:',b'\ngpgsig ' in raw)
print('MANIFEST is a SHA-256 publication index, not a detached cryptographic signature.')
assert not bad
