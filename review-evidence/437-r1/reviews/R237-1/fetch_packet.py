import base64,hashlib,json,subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
OUT=Path(__file__).resolve().parent
tree=json.loads(subprocess.check_output(['rtk','proxy','gh','api','repos/kebag-logic/milan-fpga/git/trees/e6013980ef12e558b633c0d18faecc59f1939e8a?recursive=1'],text=True))
rows=[r for r in tree['tree'] if r['path'].startswith('review-evidence/437-r1/')]
(OUT/'public-packet-tree.json').write_text(json.dumps(rows,indent=2))
keep={'MANIFEST.json','author/fixtures.json','author/mutations.py','author/mutations-head.json','author/preservation.py','author/receipt.py','author/corpus-head-both-inputs.json','author/preservation-head.json','manager/manager-builder.json','manager/native-tree-integrity.json','manager/builder-final-tree-integrity.json','manager/validation-submodules.txt','manager/full-native/results.json','manager/manager-builder/results.json','manager/full-native/complete.json','manager/manager-builder/complete.json'}
def fetch(row):
 rel=row['path'].removeprefix('review-evidence/437-r1/')
 obj=json.loads(subprocess.check_output(['rtk','proxy','gh','api','repos/kebag-logic/milan-fpga/git/blobs/'+row['sha']],text=True))
 data=base64.b64decode(obj['content']);assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==row['sha']
 path=OUT/'public-packet'/rel;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
 return {'path':rel,'git_blob':row['sha'],'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)}
selected=[r for r in rows if r['type']=='blob' and (r['path'].removeprefix('review-evidence/437-r1/') in keep or '/author/mutations-head/' in r['path'] or '/manager/full-native/' in r['path'] and r['path'].endswith('.log') or '/manager/manager-builder/' in r['path'] and r['path'].endswith('.log'))]
with ThreadPoolExecutor(max_workers=4) as pool: result=list(pool.map(fetch,selected))
(OUT/'packet-downloads.json').write_text(json.dumps(result,indent=2))
print('Fetched and Git-blob-verified',len(result),'selected factual artifacts; no review reports or private material.')
