import concurrent.futures,json,subprocess
from pathlib import Path
p=Path('$MANAGEMENT/2026-09-23/usbnet-a855/round7/receipts')
py='$VALIDATION_STORAGE/usbnet-a855/round6/markdown-venv/bin/python3'
jobs=[['python3','scripts/docs_check.py'],[py,'scripts/gen_toc.py','--check'],[py,'scripts/gen_toc.py','--verify-anchors'],['python3','scripts/check_doc_paths.py'],['python3','scripts/docs_inventory.py','--check'],['python3','scripts/measure_naming.py','--check'],['python3','scripts/measure_test_evidence.py','--check'],['git','diff','--check'],['git','diff','--cached','--check'],[py,'scripts/check_em_dash.py','--base','91252ecf7457287079d5d2f794b8544f0d9d34c4']]
def one(item):
 i,argv=item;name=f'final-doc-{i}.log'
 with (p/name).open('w') as out:r=subprocess.run(argv,stdout=out,stderr=subprocess.STDOUT)
 return dict(command=argv,rc=r.returncode,log=name)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:rows=list(pool.map(one,enumerate(jobs)))
(p/'final-documentation-gates.json').write_text(json.dumps(rows,indent=2)+'\n')
for r in rows:print(r)
assert [i for i,r in enumerate(rows) if r['rc']]==[4]
