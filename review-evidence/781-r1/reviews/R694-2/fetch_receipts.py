import concurrent.futures, hashlib, json, subprocess
from pathlib import Path
P=Path(__file__).resolve().parent
REF='f9c239222d78ce52a9e8b067b76fb8d2e74ec3a3'
manifest=json.loads(subprocess.check_output(['gh','api','repos/kebag-logic/milan-fpga/contents/review-evidence/781-r1/MANIFEST.json?ref='+REF,'-H','Accept: application/vnd.github.raw+json']))
selected=[x for x in manifest if x['file'].startswith(('author-r2/receipts/round2/', 'author-r2/scripts/round2/'))]
# Read published executable evidence only; reviewer reports and private material excluded.
def fetch(x):
    name=x['file']; dst=P/'published'/name; dst.parent.mkdir(parents=True,exist_ok=True)
    data=subprocess.check_output(['gh','api','repos/kebag-logic/milan-fpga/contents/review-evidence/781-r1/'+name+'?ref='+REF,'-H','Accept: application/vnd.github.raw+json'])
    got=hashlib.sha256(data).hexdigest()
    assert got==x['published_sha256'],name
    dst.write_bytes(data)
    return {'file':name,'sha256':got,'verified':True,'path_redacted':x['path_redacted']}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    rows=list(pool.map(fetch,selected))
(P/'published-receipt-verification.json').write_text(json.dumps({'commit':REF,'receipts':rows},indent=2)+'\n')
print('Verified',len(rows),'published receipts against pinned manifest')
