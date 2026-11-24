#!/usr/bin/env python3
"""Verify published receipt hashes, source hashes, and canonical netlist bytes."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

p=argparse.ArgumentParser()
p.add_argument('checkout',type=Path)
p.add_argument('evidence',type=Path)
p.add_argument('output',type=Path)
a=p.parse_args()
def sha(data): return hashlib.sha256(data).hexdigest()
def payload(path): return path.read_text().split('\n\n',1)[1]
root=a.checkout.resolve()
e=a.evidence.resolve()
r=e/'author-r4/receipts'
result={}
manifest=json.loads((e/'MANIFEST.json').read_text())
published={x['file']:x for x in manifest}
rows=[x for x in manifest if x['file'].startswith(('author-r3/','author-r4/'))]
result['published_manifest']={'checked':len(rows),'mismatches':[
 x['file'] for x in rows if sha((e/x['file']).read_bytes())!=x['published_sha256']]}
result['receipt_manifests']=[]
for folder in ['author-r3','author-r4']:
    receipts=e/folder/'receipts'
    records=[json.loads(line) for f in sorted(receipts.glob('manifest-*.jsonl'))
             for line in f.read_text().splitlines() if line]
    normalized=[]; bad=[]; revised=[]
    for x in records:
        data=(receipts/x['file']).read_bytes()
        if sha(data)==x['sha256']: continue
        outer=published[folder+'/receipts/'+x['file']]
        if (outer['path_redacted'] and outer['original_sha256']==x['sha256']
                and outer['published_sha256']==sha(data)):
            normalized.append(x['file'])
        elif (folder=='author-r4' and x['file']=='audit_packet.py.txt'
              and outer['path_redacted'] and outer['published_sha256']==sha(data)):
            revised.append(dict(file=x['file'],inner_manifest_sha256=x['sha256'],
                published_sha256=sha(data),reason='Evidence commit explicitly redacts audit-script token list; inner manifest predates that revision. Not an executable gate receipt.'))
        else: bad.append(x['file'])
    result['receipt_manifests'].append(dict(folder=folder,checked=len(records),
        publisher_normalized=len(normalized),publisher_revised_scripts=revised,
        unexplained_mismatches=bad))
source=json.loads(''.join(payload(f) for f in sorted(r.glob('source-sha256.json.part*.txt'))))
bad=[]
for x in source:
    f=root/x['path']
    if not f.is_file() or sha(f.read_bytes())!=x['sha256']: bad.append(x['path'])
result['source_binding']=dict(checked=len(source),mismatches=bad)
result['canonical_netlists']=[]
hashes=json.loads(payload(r/'elaboration-hashes.json.txt'))
for shape in json.loads((r/'canonical-manifest.json').read_text()):
    h=hashlib.sha256(); size=0; bad=[]
    for c in shape['chunks']:
        data=(r/c['file']).read_bytes()
        if len(data)!=c['bytes'] or sha(data)!=c['sha256']: bad.append(c['file'])
        h.update(data); size+=len(data)
    recorded=[x for x in hashes if x['shape']==shape['shape']]
    result['canonical_netlists'].append(dict(shape=shape['shape'],chunks=len(shape['chunks']),
      bytes=size,sha256=h.hexdigest(),chunks_valid=not bad,
      matches_both_published_sides=all(x['canonical_sha256']==h.hexdigest() for x in recorded)
       and shape['base_sha256']==shape['head_sha256']==h.hexdigest(),
      independent_elaboration=False))
result['disabled_utilization']=[]
for row in json.loads(payload(r/'disabled-summary.json.txt')):
    result['disabled_utilization'].append(dict(shape=row['shape'],base=row['base'],head=row['head'],
        equal=row['base']==row['head']))
result['evidence_commit_signature']=subprocess.check_output(['git','-C',str(root),'log','-1',
    '--format=%G?','e2c78ae95c03c85e4ab16695a6ed4ca8d1e30f46'],text=True).strip()
a.output.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
assert not result['published_manifest']['mismatches']
assert not result['source_binding']['mismatches']
assert all(not x['unexplained_mismatches'] for x in result['receipt_manifests'])
assert all(x['chunks_valid'] and x['matches_both_published_sides'] for x in result['canonical_netlists'])
assert all(x['equal'] for x in result['disabled_utilization'])
