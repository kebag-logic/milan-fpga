#!/usr/bin/env python3
"""Foreground concurrent focused checks, with a log and rc for every command."""
import argparse
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import time

ap=argparse.ArgumentParser()
ap.add_argument('root',type=Path)
ap.add_argument('packet',type=Path)
ap.add_argument('--jobs',type=int,default=6)
a=ap.parse_args()
assert 1<=a.jobs<=6
root,packet=a.root.resolve(),a.packet.resolve()
scratch=packet/'scratch'; receipts=packet/'receipts'
env=os.environ.copy()
env['TMPDIR']=str(scratch)
env['PYTHONDONTWRITEBYTECODE']='1'
env['PATH']=str(scratch/'venv/bin')+os.pathsep+env['PATH']
suite_tree=scratch/'suite-tree'
if not suite_tree.exists():
 subprocess.run(['git','clone','--quiet','--shared','--no-checkout',str(root),str(suite_tree)],check=True)
 subprocess.run(['git','-C',str(suite_tree),'checkout','--quiet','--detach','5123548eb4de35f24d43eb088c12dab70b06d01d'],check=True)
wrapper=packet/'scripts/scoped_verilator.py'
wrapper.chmod(0o755)
tasks=[('make-check',['make','-j16','check'],root),('make-ids',['make','-j16','ids'],root)]
for suite in ('side_port','tx_arbiter','tx_slots','rx_validator'):
 tasks.append((suite,['make','-j16','-C',str(suite_tree/'tb'/suite),'run','VERILATOR='+str(wrapper)],root))
def run(t):
 name,cmd,cwd=t; start=time.time()
 with (receipts/(name+'.log')).open('w') as log:
  log.write('command: '+json.dumps(cmd)+'\n');log.flush()
  p=subprocess.run(cmd,cwd=cwd,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=570)
 (receipts/(name+'.rc')).write_text(str(p.returncode)+'\n')
 print(name,'rc',p.returncode,'seconds',round(time.time()-start,2),flush=True)
 return dict(name=name,command=cmd,rc=p.returncode,seconds=round(time.time()-start,2))
with concurrent.futures.ThreadPoolExecutor(max_workers=a.jobs) as pool:
 results=list(pool.map(run,tasks))
(receipts/'checks.json').write_text(json.dumps(results,indent=2)+'\n')
assert all(r['rc']==0 for r in results)
