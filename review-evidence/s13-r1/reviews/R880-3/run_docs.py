#!/usr/bin/env python3
"""Run focused exact-head documentation checks concurrently, retaining raw output.
Usage: run_docs.py REPO OUTPUT PYTHON
"""
import concurrent.futures
import os
from pathlib import Path
import subprocess
import sys

repo, out = map(Path, sys.argv[1:3])
python = sys.argv[3]
checks = [
 ('docs-check', ['scripts/docs_check.py']),
 ('style', ['scripts/check_doc_style.py']),
 ('feature', ['scripts/check_feature_status.py']),
 ('doc-paths', ['scripts/check_doc_paths.py']),
 ('inventory', ['scripts/docs_inventory.py','--check']),
 ('em-dash', ['scripts/check_em_dash.py','--base','59b09884']),
 ('register', ['scripts/gen_register_reference.py','--check']),
 ('register-selftest', ['scripts/gen_register_reference.py','--selftest']),
 ('solution', ['scripts/check_solution_docs.py']),
 ('python-idiom', ['scripts/check_py_idiom.py']),
 ('toc', ['scripts/gen_toc.py','--check']),
 ('anchors', ['scripts/gen_toc.py','--verify-anchors']),
]
def run(item):
    name,args=item
    cmd=[python,'-B',*args]
    env={**os.environ,'TMPDIR':str(out.parent/'scratch')}
    r=subprocess.run(cmd,cwd=repo,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    (out/(name+'.txt')).write_text('COMMAND '+ ' '.join(args)+'\n'+r.stdout)
    (out/(name+'.rc')).write_text(str(r.returncode)+'\n')
    return name,r.returncode,r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ''
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    results=list(pool.map(run,checks))
for result in results: print(*result)
sys.exit(any(rc for _,rc,_ in results))
