#!/usr/bin/env python3
"""Read only selected public execution receipts, never lane notes or review reports."""
import concurrent.futures, hashlib, json, pathlib, subprocess, sys
out=pathlib.Path(__file__).resolve().parent
ref='988e9e8946ddd86e7ade82874a4e580c2ec61681'
files=sys.argv[1:] or ['author-r4/round4-s3-equality.json','author-r4/round4-s3-mutations.json','author-r4/round4-mutations.json','author-r4/baseline-elaborate.json','author-r4/round4-s3-receipt-f-e1-unsharded.json','author-r4/round4-s3-receipt-f-e2-leg0.json','author-r4/round4-s3-receipt-f-e3-leg1.json']
def get(name):
 assert not any(s in name for s in ['HANDOFF','PR-BODY','REPORT','reviews/'])
 path='review-evidence/737-r1/'+name
 data=subprocess.check_output(['gh','api',f'repos/kebag-logic/milan-fpga/contents/{path}?ref={ref}','-H','Accept: application/vnd.github.raw+json'])
 target=out/'scratch'/'public'/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
 return {'path':path,'ref':ref,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: results=list(pool.map(get,files))
print(json.dumps(results,indent=2))
p=out/'public-fetch-index.json'; prior=json.loads(p.read_text()) if p.exists() else []
p.write_text(json.dumps(prior+results,indent=2)+'\n')
