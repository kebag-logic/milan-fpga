#!/usr/bin/env python3
"""Foreground, bounded parallel review checks. Arguments: checkout packet."""
import concurrent.futures, os, pathlib, subprocess, sys
repo, out = map(pathlib.Path, sys.argv[1:])
i=out/'scratch/review-evidence/s13-r1/author-r2/receipts/identity'
py=os.environ.get('DOCS_PYTHON',sys.executable)
env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(out/'scratch'), PYTHONHASHSEED='0')
jobs={
'replay':['python3','-I',str(i/'tools/replay.py'),str(i)],
'replay-plants':['python3','-I',str(i/'tools/rmutants.py'),str(i),str(out/'scratch/replay-plants')],
'soc-selftest':['python3','-B','syn/resmap/soc_sweep.py','--selftest'],
'harness-checks':['python3','-B','-c',"import sys; sys.path.insert(0,'tb/verilator/ctrl_service_budget'); import selftest; rows=selftest.build_checks(); [print(('PASS ' if ok else 'FAIL ')+n+' '+d) for n,ok,d in rows]; sys.exit(not all(ok for _,ok,_ in rows))"],
'register-check':[py,'-B','scripts/gen_register_reference.py','--check'],
'register-selftest':[py,'-B','scripts/gen_register_reference.py','--selftest'],
'docs-check':[py,'-B','scripts/docs_check.py'],
'doc-style':[py,'-B','scripts/check_doc_style.py'],
'doc-paths':[py,'-B','scripts/check_doc_paths.py'],
'solution-docs':[py,'-B','scripts/check_solution_docs.py'],
'em-dash':[py,'-B','scripts/check_em_dash.py','--base','59b09884'],
}
def run(item):
 name,cmd=item
 with (out/(name+'.log')).open('w') as f:
  f.write('COMMAND '+repr(cmd)+'\n'); f.flush()
  r=subprocess.run(cmd,cwd=repo,env=env,stdout=f,stderr=subprocess.STDOUT)
 (out/(name+'.rc')).write_text(str(r.returncode)+'\n')
 print(name, r.returncode,flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: list(pool.map(run,jobs.items()))
