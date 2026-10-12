#!/usr/bin/env python3
"""Fetch only public round-7 executor receipts, never review reports."""
import base64,concurrent.futures,hashlib,json,pathlib,subprocess
P=pathlib.Path(__file__).resolve().parents[1]
REV='e5ca8c172b07be7fc935a9ed85fa815380a196aa'
PREFIX='review-evidence/671-r1/author-r7/'
tree=json.loads(subprocess.check_output(['gh','api',f'repos/kebag-logic/milan-fpga/git/trees/{REV}?recursive=1']))['tree']
names=['assemble.log','capture__driver-a.log','capture__driver-b.log','selftest_final.log','controls__term_census.log','controls__term_matrix.log','controls__term_views.log','builder_final__driver.log','builder_final__part6.log','docsrep__replica.log','vsuites_final__driver.log','vsuites_final__nvm_cosim.log','final__capture.log','size__fw_size.txt','fwunit__replica.log','rtlfast__replica.log']
paths={PREFIX+'receipts/r7/'+n for n in names}
paths.update(x['path'] for x in tree if x['path'].startswith(PREFIX+'receipts/r7/capture__') and ('__measurement.json' in x['path'] or '__run-' in x['path']))
paths.update(PREFIX+'scripts/r7/'+n for n in ['assemble_receipt.py','capture_driver.sh','selftest.sh'])
(P/'receipts/public').mkdir(exist_ok=True)
def fetch(x):
 d=json.loads(subprocess.check_output(['gh','api',f"repos/kebag-logic/milan-fpga/git/blobs/{x['sha']}"]))
 raw=base64.b64decode(d['content'])
 assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==x['sha']
 out=P/'receipts/public'/pathlib.Path(x['path']).name
 out.write_bytes(raw)
 return dict(path=x['path'],git_blob=x['sha'],sha256=hashlib.sha256(raw).hexdigest(),local=str(out.relative_to(P)),url=f"https://github.com/kebag-logic/milan-fpga/blob/{REV}/{x['path']}")
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: rows=list(pool.map(fetch,[x for x in tree if x['path'] in paths]))
assert len(rows)==len(paths)
(P/'receipts/public-index.json').write_text(json.dumps(rows,indent=2)+'\n')
print('Verified public executor blobs:',len(rows))
