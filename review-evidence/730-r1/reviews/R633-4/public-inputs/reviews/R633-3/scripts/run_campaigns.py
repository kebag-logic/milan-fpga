import concurrent.futures,json,subprocess,sys,time
from pathlib import Path
p=Path(sys.argv[1]).resolve();repo=sys.argv[2]
sb=['sh',str(p/'scripts/reviewer_sandbox.sh'),repo,str(p)]
checks={
 'mutants-r2-unchanged':['python3','-I',str(p/'scripts/mutants_r2.py'),str(p),str(p/'scratch/pristine'),'--jobs','10'],
 'r633-r1-unchanged':sb+['python3','-I','/packet/public-inputs/reviews/R633-1/probe_cpu_ranges.py','/work'],
 'r633-r1-compatible':sb+['python3','-I','/packet/public-inputs/reviews/R633-2/probe_cpu_ranges_compat.py','/work'],
 'r633-r2-monitor-unchanged':sb+['python3','-I','/packet/public-inputs/reviews/R633-2/probe_monitor.py','/work'],
 'r633-r2-lifecycle-unchanged':sb+['python3','-I','/packet/public-inputs/reviews/R633-2/probe_lifecycle.py','/work'],
 'r632-r2-probe-unchanged':sb+['python3','-I','/packet/scripts/probe_r2.py','/work','3000'],
 'r632-r2-shutdown-unchanged':sb+['python3','-I','/packet/scripts/probe_shutdown.py','/work'],
}
def run(item):
 name,cmd=item;start=time.monotonic()
 with (p/'receipts'/f'{name}.log').open('w') as out:
  r=subprocess.run(cmd,stdout=out,stderr=subprocess.STDOUT,timeout=540)
 (p/'receipts'/f'{name}.rc').write_text(str(r.returncode)+'\n')
 result={'name':name,'rc':r.returncode,'seconds':round(time.monotonic()-start,3),'command':cmd}
 print(json.dumps(result),flush=True);return result
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(run,checks.items()))
(p/'receipts/campaigns.json').write_text(json.dumps(results,indent=2)+'\n')
