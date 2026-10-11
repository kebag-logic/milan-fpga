#!/usr/bin/env python3
"""Download selected immutable public evidence and probes; verify Git blob identities."""
import concurrent.futures,hashlib,json,subprocess
from pathlib import Path
p=Path(__file__).resolve().parents[1];ref='7ee91b258d93fa77052faa621e9b84cdf46665a8'
tree_file=p/'scratch/public-tree.json'
if not tree_file.exists():
 tree_file.parent.mkdir(parents=True,exist_ok=True)
 tree_file.write_bytes(subprocess.check_output(['gh','api','repos/kebag-logic/milan-fpga/git/trees/'+ref+'?recursive=1']))
tree=json.loads(tree_file.read_text())['tree'];prefix='review-evidence/pp73-r1/'
files=[]
for e in tree:
 n=e['path'];rel=n.removeprefix(prefix)
 if e['type']!='blob' or not n.startswith(prefix):continue
 pick=rel=='MANIFEST.json'
 pick |= rel.startswith('reviews/R608-2/scripts/')
 pick |= rel in ['reviews/R609-2/scripts/probe_export_fields.py','reviews/R609-2/scripts/probe_contract.py','reviews/R609-1/scripts/size_sweep.py','reviews/R609-1/scripts/rom_size_probe.py']
 pick |= rel.startswith('author-r3/receipts/r3/') and (rel.endswith(('.tsv','.sha')) and '/bin/' not in rel)
 pick |= rel in ['author-r3/MANIFEST.json','author-r3/LARGE-ARTIFACTS.tsv','author-r3/parent-aecp-cmds-evidence.patch']
 pick |= rel.startswith('author-r3/receipts/r3/comparisons/')
 pick |= rel.startswith('author-r3/receipts/r3/consumer/')
 pick |= rel.startswith('author-r3/receipts/r3/logs/') and any('/'+s in rel for s in ['head-final-','base-check.','head-python.','head-python-list.','head-python-self.','head-parent.','head-aecp-controls-final.','final-pr-reference.'])
 pick |= rel.endswith('/source-integrity.txt') and rel.startswith('author-r3/receipts/r3/')
 if pick:files.append(e)
def get(e):
 rel=e['path'][len(prefix):];out=p/'public'/rel;out.parent.mkdir(parents=True,exist_ok=True)
 data=subprocess.check_output(['gh','api','repos/kebag-logic/milan-fpga/contents/'+e['path']+'?ref='+ref,'-H','Accept: application/vnd.github.raw+json'])
 sha=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
 if sha!=e['sha']:raise RuntimeError('Git blob mismatch: '+rel)
 out.write_bytes(data)
 return dict(path='public/'+rel,git_blob=sha,sha256=hashlib.sha256(data).hexdigest(),bytes=len(data))
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:results=list(pool.map(get,files))
(p/'receipts/public-fetch.json').write_text(json.dumps(dict(commit=ref,files=results),indent=2)+'\n')
print('Fetched and verified',len(results),'public files; no separate review report downloaded.')
