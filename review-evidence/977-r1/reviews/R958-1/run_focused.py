#!/usr/bin/env python3
"""Run independent focused checks concurrently; all children joined before exit."""
import argparse
import concurrent.futures
import os
import subprocess
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument('--root',type=Path,required=True)
p.add_argument('--packet',type=Path,required=True)
a=p.parse_args(); root=a.root.resolve(); packet=a.packet.resolve()
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(packet/'scratch'))
base='tb/verilator/ctrl_service_budget/'
tasks={
 'charge-1x1':['python3',str(packet/'probe_charge.py'),'--root',str(root),'--packet',str(packet),'--point','1x1','--jobs','4'],
 'charge-8x8':['python3',str(packet/'probe_charge.py'),'--root',str(root),'--packet',str(packet),'--point','8x8','--jobs','4'],
 'load':['python3','-I',base+'load_grade.py','--check'],
 'flip-1x1':['python3','-I',base+'flip_grade.py','--check','--point','1x1/1if'],
 'flip-8x8':['python3','-I',base+'flip_grade.py','--check','--point','8x8/1if'],
 'kept-selftest':['python3','-I',base+'kept_grade.py','--selftest'],
 'egress-selftest':['python3','-I',base+'egress_ledger.py','--selftest'],
 'shape':['python3','-I',base+'shape_costs.py','--check'],
 'memory':['python3','sw/litex/test_ctrl_memory.py'],
 'hot':['python3','sw/firmware/ctrl/test/ctrl_hot.py','--check'],
}
def run(item):
 name,cmd=item
 with (packet/(name+'.log')).open('w') as log:
  log.write('COMMAND: '+' '.join(cmd)+'\n'); log.flush()
  r=subprocess.run(cmd,cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=550)
 (packet/(name+'.rc')).write_text(str(r.returncode)+'\n')
 return name,r.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 for name,rc in pool.map(run,tasks.items()): print(name,rc,flush=True)
