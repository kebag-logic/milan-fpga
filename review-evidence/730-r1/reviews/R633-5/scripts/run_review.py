#!/usr/bin/env python3
"""Foreground review driver: two six-worker campaigns plus at most four focused jobs."""
import concurrent.futures,json,subprocess,sys,time
from pathlib import Path
p=Path(__file__).resolve().parent.parent
repo=Path(sys.argv[1]).resolve()
sb=['sh',str(p/'scripts/reviewer_sandbox.sh'),str(repo),str(p)]
checks={
'selftest':['python3','-I','scripts/act_ci.py','--selftest'],
'cleanup-entry':['python3','-I','/packet/scripts/probe_cleanup_entry.py','/work'],
'r633-r1-unchanged':['python3','-I','/packet/public-inputs/reviews/R633-2/probe_cpu_ranges_r1.py','/work'],
'r633-r1-compatible':['python3','-I','/packet/public-inputs/reviews/R633-2/probe_cpu_ranges_compat.py','/work'],
'r633-r2-lifecycle':['python3','-I','/packet/public-inputs/reviews/R633-2/probe_lifecycle.py','/work'],
'r633-r2-monitor':['python3','-I','/packet/public-inputs/reviews/R633-2/probe_monitor.py','/work'],
'r632-r3-probe':['python3','-I','/packet/scripts/probe_r3.py','/work','300'],
'r632-r2-shutdown':['python3','-I','/packet/scripts/probe_shutdown.py','/work'],
'offline-dryrun':['python3','-I','/packet/scripts/offline_dryrun.py','/work'],
'slot-proof':['bash','scripts/act_slot_proof.sh','--selftest'],
'ci-events-check':['python3','scripts/ci_events.py','--check'],
'ci-events-selftest':['python3','scripts/ci_events.py','--selftest'],
'py-idiom':['python3','scripts/check_py_idiom.py'],
'py-idiom-selftest':['python3','scripts/check_py_idiom.py','--selftest'],
}
def run(name,cmd):
 start=time.monotonic()
 with (p/'receipts'/f'{name}.log').open('w') as f:
  try: rc=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,timeout=570).returncode
  except subprocess.TimeoutExpired: rc=124
 (p/'receipts'/f'{name}.rc').write_text(str(rc)+'\n')
 row={'name':name,'command':cmd,'rc':rc,'seconds':round(time.monotonic()-start,3)}
 print(json.dumps(row),flush=True)
 return row
def focused():
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as e:
  return list(e.map(lambda item:run(item[0],sb+item[1]),checks.items()))
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as e:
 futures=[e.submit(run,f'mutants-r{n}', ['python3','-I',str(p/f'scripts/mutants_r{n}.py'),str(p),str(p/'scratch/pristine'),'--jobs','6']) for n in (2,3)]
 f=e.submit(focused)
 rows=[x.result() for x in futures]+f.result()
(p/'receipts/review-runs.json').write_text(json.dumps(rows,indent=2)+'\n')
sys.exit(0 if all(x['rc']==(1 if x['name']=='r633-r1-unchanged' else 0) for x in rows) else 1)
