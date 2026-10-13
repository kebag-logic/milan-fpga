#!/usr/bin/env python3
"""Foreground driver for independent offline review; every child is joined."""
import concurrent.futures,json,subprocess,sys,time
from pathlib import Path
p=Path(__file__).resolve().parent.parent
repo=Path(sys.argv[1]).resolve()
sb=['sh',str(p/'scripts/reviewer_sandbox.sh'),str(repo),str(p)]
checks={
 'independent-selftest':['python3','-I','scripts/act_ci.py','--selftest'],
 'independent-boundary':['python3','-I','/packet/scripts/probe_boundary_precedence.py','/work'],
 'ci-events-check':['python3','scripts/ci_events.py','--check'],
 'ci-events-selftest':['python3','scripts/ci_events.py','--selftest'],
 'py-idiom':['python3','scripts/check_py_idiom.py'],
 'py-idiom-selftest':['python3','scripts/check_py_idiom.py','--selftest'],
 'slot-proof':['bash','scripts/act_slot_proof.sh','--selftest'],
 'doc-style':['python3','scripts/check_doc_style.py'],
 'doc-paths':['python3','scripts/check_doc_paths.py'],
 'docs-check':['python3','scripts/docs_check.py'],
 'diff-check':['git','diff','--check','dc4d06cb','HEAD'],
}
def run(item):
 name,cmd=item;start=time.monotonic()
 with (p/'receipts'/f'{name}.log').open('w') as f:
  try:rc=subprocess.run(sb+cmd,stdout=f,stderr=subprocess.STDOUT,timeout=570).returncode
  except subprocess.TimeoutExpired:rc=124
 (p/'receipts'/f'{name}.rc').write_text(str(rc)+'\n')
 row=dict(name=name,command=cmd,rc=rc,seconds=round(time.monotonic()-start,3))
 print(json.dumps(row),flush=True);return row
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 rows=list(pool.map(run,checks.items()))
(p/'receipts/independent-runs.json').write_text(json.dumps(rows,indent=2)+'\n')
sys.exit(int(any(row['rc'] for row in rows)))
