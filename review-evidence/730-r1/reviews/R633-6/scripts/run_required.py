#!/usr/bin/env python3
"""Joined foreground campaigns: six workers each plus four focused probes."""
import concurrent.futures,json,subprocess,sys,time
from pathlib import Path
p=Path(__file__).resolve().parent.parent;repo=Path(sys.argv[1]).resolve()
sb=['sh',str(p/'scripts/reviewer_sandbox.sh'),str(repo),str(p)]
checks={
 'r633-r1-unchanged':['python3','-I','/packet/scripts/probe_cpu_ranges_r1.py','/work'],
 'r633-r1-compatible':['python3','-I','/packet/scripts/probe_cpu_ranges_compat.py','/work'],
 'r633-r2-lifecycle':['python3','-I','/packet/scripts/probe_lifecycle.py','/work'],
 'r633-r2-monitor':['python3','-I','/packet/scripts/probe_monitor.py','/work'],
 'cleanup-entry':['python3','-I','/packet/scripts/probe_cleanup_entry.py','/work'],
 'r632-r2-shutdown':['python3','-I','/packet/scripts/probe_shutdown.py','/work'],
 'r632-r3-probe':['python3','-I','/packet/scripts/probe_r3.py','/work','300'],
 'offline-dryrun':['python3','-I','/packet/scripts/offline_dryrun.py','/work'],
}
def run(name,cmd):
 start=time.monotonic()
 with (p/'receipts'/f'{name}.log').open('w') as f:
  try:rc=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,timeout=570).returncode
  except subprocess.TimeoutExpired:rc=124
 (p/'receipts'/f'{name}.rc').write_text(str(rc)+'\n')
 row=dict(name=name,command=cmd,rc=rc,seconds=round(time.monotonic()-start,3));print(json.dumps(row),flush=True);return row
def focused():
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
  return list(pool.map(lambda x:run(x[0],sb+x[1]),checks.items()))
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 fs=[pool.submit(run,f'mutants-r{n}',['python3','-I',str(p/f'scripts/mutants_r{n}.py'),str(p),str(p/'scratch/pristine'),'--jobs','6']) for n in (2,3)]
 f=pool.submit(focused);rows=[x.result() for x in fs]+f.result()
(p/'receipts/required-runs.json').write_text(json.dumps(rows,indent=2)+'\n')
sys.exit(int(any(r['rc']!=(1 if r['name']=='r633-r1-unchanged' else 0) for r in rows)))
