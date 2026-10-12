#!/usr/bin/env python3
import argparse,concurrent.futures,hashlib,json,pathlib,subprocess
p=argparse.ArgumentParser();p.add_argument('--packet',type=pathlib.Path,required=True);a=p.parse_args();root=a.packet.resolve()
tree=json.loads((root/'scratch/evidence-tree-correct.json').read_text())['tree'];prefix='review-evidence/tsn24-r1/author-r3/round3/'
entries=[e for e in tree if e['type']=='blob' and e['path'].startswith(prefix) and (e['path'].endswith(('.json','.xml','.rc','.sha256')) or e['path'].split('/')[-1] in ['coverage.log','static-analysis.log','traceability.log','test-inventory.log'])]
def fetch(e):
    rel=e['path'][len(prefix):];out=root/'scratch/public-author-r3'/rel;out.parent.mkdir(parents=True,exist_ok=True)
    data=subprocess.check_output(['gh','api','repos/kebag-logic/milan-fpga/contents/'+e['path']+'?ref=66585285f6a16ae1498416f89031698693542062','-H','Accept: application/vnd.github.raw+json'])
    blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest();assert blob==e['sha'],rel
    out.write_bytes(data);return {'path':rel,'blob':blob,'sha256':hashlib.sha256(data).hexdigest()}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:rows=list(ex.map(fetch,entries))
(root/'receipts/public-evidence-files.json').write_text(json.dumps(rows,indent=2)+'\n');print('Verified published blobs:',len(rows))
