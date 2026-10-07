#!/usr/bin/env python3
"""Foreground supervisor; all children finish before the command returns."""
import concurrent.futures,json,os,subprocess,sys,time
from pathlib import Path
repo=Path(sys.argv[1]).resolve();packet=Path(__file__).resolve().parents[1]
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(packet/'scratch'))
def run(mode):
 cmd=[sys.executable,str(packet/'scripts/focused.py'),str(repo),mode,'--jobs','2']
 start=time.monotonic()
 with (packet/'receipts'/(mode+'.log')).open('w') as log:
  r=subprocess.run(cmd,cwd=repo,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=550)
 (packet/'receipts'/(mode+'.rc')).write_text(str(r.returncode)+'\n')
 print(mode,'rc',r.returncode,'seconds',round(time.monotonic()-start,2),flush=True)
 return {'mode':mode,'rc':r.returncode,'seconds':round(time.monotonic()-start,2),'jobs':2}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 results=list(pool.map(run,['suites','probes','campaign','new-if1']))
(packet/'receipts/execution.json').write_text(json.dumps(results,indent=2)+'\n')
sys.exit(any(r['rc'] for r in results))
