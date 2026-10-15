#!/usr/bin/env python3
"""Fetch selected public receipts, verify published hashes and Git blob identities."""
import concurrent.futures, hashlib, json, subprocess
from pathlib import Path
P=Path(__file__).resolve().parent
REV='d43f00d766c5b052515c686022da31d17c45ed0c'
PREFIX='review-evidence/737-image-r1/'
def api(path):
 return subprocess.check_output(['gh','api','-H','Accept: application/vnd.github.raw+json',f'repos/kebag-logic/milan-fpga/{path}'])
(P/'scratch').mkdir(exist_ok=True)
for target,endpoint in [('public-tree.json',f'git/trees/{REV}?recursive=1'),
                        ('public-manifest.json',f'contents/{PREFIX}MANIFEST.json?ref={REV}')]:
 if not (P/'scratch'/target).exists(): (P/'scratch'/target).write_bytes(api(endpoint))
tree=json.loads((P/'scratch/public-tree.json').read_text())['tree']
manifest=json.loads((P/'scratch/public-manifest.json').read_text())
pins={x['file']:x for x in manifest}
selected=[x for x in tree if x['type']=='blob' and x['path'].startswith(PREFIX+'author-r7/round7')]
def fetch(row):
 relative=row['path'].removeprefix(PREFIX)
 content=api(f'contents/{row["path"]}?ref={REV}')
 target=P/'scratch/public'/relative
 target.parent.mkdir(parents=True,exist_ok=True); target.write_bytes(content)
 sha=hashlib.sha256(content).hexdigest()
 blob=hashlib.sha1(b'blob '+str(len(content)).encode()+b'\0'+content).hexdigest()
 assert sha==pins[relative]['published_sha256'] and blob==row['sha'],relative
 return {'path':relative,'bytes':len(content),'sha256':sha,'git_blob':blob,'original_sha256':pins[relative]['original_sha256'],'redacted':pins[relative]['path_redacted']}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
 results=list(pool.map(fetch,selected))
commit=json.loads(api(f'commits/{REV}'))
verification=commit['commit']['verification']
report={'public_commit':REV,'commit_verification':verification,'verified_files':results,'note':'Published bytes are verified against the public manifest and Git blobs; original hashes of redacted receipts are not independently reproducible from published bytes.'}
(P/'public-evidence-verification.json').write_text(json.dumps(report,indent=2)+'\n')
print('Verified',len(results),'receipts; commit verification:',verification['verified'],verification['reason'])
