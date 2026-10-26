#!/usr/bin/env python3
"""Complete the small scheduling and documentation gates."""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys
import time

root = Path(sys.argv[1]).resolve()
out = Path(__file__).resolve().parent
markdown_python = str(out / 'scratch/md-env/bin/python')
checks = [(name, sys.executable, ['scripts/' + name + '.py']) for name in (
    'ci_case_receipts_selftest', 'ci_make_cases_selftest', 'ci_maap_cases_selftest',
    'ci_capture_cases_selftest', 'ci_suite_pieces_selftest', 'ci_suite_collect_selftest',
    'ci_fail_fast_selftest', 'docs_check', 'check_doc_style', 'check_doc_paths', 'check_py_idiom')]
checks += [('toc_check', markdown_python, ['scripts/gen_toc.py', '--check']),
           ('em_dash', markdown_python, ['scripts/check_em_dash.py', '--base', '76de691e5625cc4ea2f9a19def9e07c1183a14ee'])]
def run(entry):
    name, python, args = entry
    scratch = out / 'scratch' / name
    scratch.mkdir(exist_ok=True)
    env = {**os.environ,'TMPDIR':str(scratch),'PYTHONDONTWRITEBYTECODE':'1'}
    start = time.monotonic()
    with (out/(name+'.log')).open('w') as log:
        log.write('COMMAND: python3 ' + ' '.join(args) + '\n')
        log.flush()
        rc = subprocess.run([python,*args],cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=570).returncode
    record = {'command':['python3',*args],'rc':rc,'elapsed_s':round(time.monotonic()-start,3)}
    (out/(name+'.rc')).write_text(str(rc)+'\n')
    print(name,json.dumps(record),flush=True)
    return name,record
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = dict(pool.map(run,checks))
(out/'more-checks.json').write_text(json.dumps(results,indent=2)+'\n')
sys.exit(int(any(r['rc'] for r in results.values())))
