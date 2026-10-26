#!/usr/bin/env python3
"""Verify public receipts against the published manifest without reading handoffs."""
import hashlib,json,pathlib,subprocess,sys
root=pathlib.Path(sys.argv[1]).resolve()
packet=pathlib.Path(__file__).resolve().parent
rev='50eb576c296d80307eac7c3064129440642d823d'
prefix='review-evidence/665s1-r1/'
def blob(path): return subprocess.check_output(['git','show',rev+':'+prefix+path],cwd=root)
manifest=json.loads(blob('MANIFEST.json'))
rows=[]
for row in manifest:
    name=row['file']
    if not (name.startswith('author/receipts/') or name.startswith('author/probes/')): continue
    data=blob(name)
    digest=hashlib.sha256(data).hexdigest()
    assert digest==row['published_sha256'],name
    dest=packet/'scratch/public-evidence'/name
    dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
    rows.append({'file':name,'sha256':digest,'bytes':len(data),'path_redacted':row['path_redacted']})
signed=b'gpgsig ' in subprocess.check_output(['git','cat-file','commit',rev],cwd=root)
(packet/'evidence-hashes.json').write_text(json.dumps({'commit':rev,'commit_signature_present':signed,'checked':rows},indent=2)+'\n')
print('Verified',len(rows),'public receipts/probes against published SHA-256 manifest.')
print('Signature header present:', signed)
