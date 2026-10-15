#!/usr/bin/env python3
"""Focused foreground controls; no full banks or container orchestration."""
import concurrent.futures, json, os, subprocess, sys, time
from pathlib import Path
p=Path(__file__).resolve().parent
root=Path(os.environ.get('CHECKOUT',os.getcwd())).resolve()
env={**os.environ,'TMPDIR':str(p/'scratch'),'PYTHONDONTWRITEBYTECODE':'1'}
commands={
 'differential-check':['scripts/ci_differential.py','--check'],
 'census-selftest':['scripts/ci_differential_selftest.py'],
 'baremetal-check':['scripts/check_baremetal_only.py','--check'],
 'baremetal-selftest':['scripts/check_baremetal_only.py','--selftest'],
 'lock-check':['ci/image/build.py','--work',str(p/'scratch/build'),'--check-lock'],
}
def run(item):
 name,args=item; start=time.monotonic()
 with (p/(name+'.log')).open('w') as log:
  r=subprocess.run([sys.executable,*args],cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=500)
 (p/(name+'.rc')).write_text(str(r.returncode)+'\n')
 return {'name':name,'argv':['python3',*[x.replace(str(p),'<packet>') for x in args]],'rc':r.returncode,'seconds':round(time.monotonic()-start,3)}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 results=list(pool.map(run,commands.items()))
results.append(run(('inventory-check-last',['scripts/ci_tool_inventory.py','--check'])))
(p/'controls.json').write_text(json.dumps({'python':sys.version.split()[0],'results':results},indent=2)+'\n')
print(json.dumps(results,indent=2))
