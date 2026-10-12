#!/usr/bin/env python3
"""Run focused policy/documentation gates in disposable boundaries; await all."""
import concurrent.futures
import json
from pathlib import Path
import subprocess
import sys
import time

p = Path(__file__).resolve().parent.parent
repo = Path(sys.argv[1]).resolve()
sb = ['sh',str(p/'scripts/reviewer_sandbox.sh'),str(repo),str(p)]
docpython = '/packet/scratch/markdown/bin/python'
checks = {
    'ci-events-check':['python3','scripts/ci_events.py','--check'],
    'ci-events-selftest':['python3','scripts/ci_events.py','--selftest'],
    'py-idiom':['python3','scripts/check_py_idiom.py'],
    'py-idiom-selftest':['python3','scripts/check_py_idiom.py','--selftest'],
    'baremetal-check':['python3','scripts/check_baremetal_only.py','--check'],
    'baremetal-selftest':['python3','scripts/check_baremetal_only.py','--selftest'],
    'docs-check':['python3','scripts/docs_check.py'],
    'doc-style':['python3','scripts/check_doc_style.py'],
    'doc-paths':['python3','scripts/check_doc_paths.py'],
    'toc':[docpython,'scripts/gen_toc.py','--check'],
    'anchors':[docpython,'scripts/gen_toc.py','--verify-anchors'],
    'em-dash':[docpython,'scripts/check_em_dash.py','--base','dc4d06cb'],
    'diff-check':['git','diff','--check','dc4d06cb','HEAD'],
    'offline-dryrun':['python3','-I','/packet/public-inputs/reviews/R633-3/scripts/offline_dryrun.py','/work'],
}

def run(item):
    name, args = item
    start = time.monotonic()
    with (p/'receipts'/f'{name}.log').open('w') as log:
        result = subprocess.run(sb+args,stdout=log,stderr=subprocess.STDOUT,timeout=540)
    (p/'receipts'/f'{name}.rc').write_text(f'{result.returncode}\n')
    row = {'name':name,'command':sb+args,'rc':result.returncode,
           'seconds':round(time.monotonic()-start,3)}
    print(json.dumps(row),flush=True)
    return row

with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    rows=list(pool.map(run,checks.items()))
(p/'receipts/gates.json').write_text(json.dumps(rows,indent=2)+'\n')
sys.exit(0 if all(r['rc']==0 for r in rows) else 1)
