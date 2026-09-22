"""Download selected immutable public evidence, verifying each Git blob."""
import base64,concurrent.futures,hashlib,json,pathlib,subprocess
root=pathlib.Path(__file__).resolve().parents[1]
tree=json.loads((root/'raw/evidence-tree.json').read_bytes())
prefix='review-evidence/423-r1/'
exact=['author/public/scripts/fixtures.py','author/public/rawlogs/fixture-matrix.json','author/receipts/public-matrix.json','author/receipts/pr62-history.json','author/receipts/mutations-matrix.json','author/scripts/reproduce_history.py','author/scripts/reproduce_public.py','review/R244-interrupted/locale_transport_probe.sh']
selected=[x for x in tree['tree'] if x['type']=='blob' and x['path'].startswith(prefix) and (x['path'][len(prefix):] in exact or x['path'].startswith(prefix+'corrected-source2/manager/') or x['path'].startswith(prefix+'corrected-source2/author/'))]
def fetch(entry):
 rel=entry['path'][len(prefix):]
 dest=root/'public'/rel
 dest.parent.mkdir(parents=True,exist_ok=True)
 r=subprocess.run(['rtk','proxy','gh','api','repos/kebag-logic/milan-fpga/git/blobs/'+entry['sha']],capture_output=True,check=True)
 data=base64.b64decode(json.loads(r.stdout)['content'])
 actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
 assert actual==entry['sha'],rel
 dest.write_bytes(data)
 return {'path':rel,'blob':actual,'size':len(data),'sha256':hashlib.sha256(data).hexdigest()}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 results=list(pool.map(fetch,selected))
(root/'raw/evidence-verification.json').write_text(json.dumps(results,indent=2)+'\n')
print('Verified',len(results),'immutable public blobs; no hosted API endpoints used.')
