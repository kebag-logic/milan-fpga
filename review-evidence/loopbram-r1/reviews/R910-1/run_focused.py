#!/usr/bin/env python3
"""Run bounded independent checks; retain raw stdout and exit status."""
import argparse, concurrent.futures, json, os, pathlib, subprocess
p=argparse.ArgumentParser()
p.add_argument('source', type=pathlib.Path)
p.add_argument('--simulator', required=True)
p.add_argument('--jobs', type=int, default=12)
a=p.parse_args()
root=pathlib.Path(__file__).resolve().parent
scratch=root/'scratch'
scratch.mkdir(exist_ok=True)
env=os.environ.copy()
env['TMPDIR']=str(scratch)
env['PYTHONDONTWRITEBYTECODE']='1'
tasks={
 'wire8':['make','-j16','-s','-C','tb/verilator/input_loopback','run','VERILATOR_JOBS=4','VERILATOR='+a.simulator,'MDIR='+str(scratch/'wire8')],
 'wire1':['make','-j16','-s','-C','tb/verilator/input_loopback','run','VERILATOR_JOBS=4','VERILATOR='+a.simulator,'STREAMS=1','FIRST=8','CHANNELS=8','LEAD=2','MDIR='+str(scratch/'wire1')],
 'builder':['python3','sw/builder/test_input_loopback.py'],
}
def run(item):
 name, cmd=item
 with (scratch/(name+'.raw.log')).open('w') as log:
  r=subprocess.run(cmd,cwd=a.source,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=550)
 (scratch/(name+'.rc')).write_text(str(r.returncode)+'\n')
 return {'name':name,'exit':r.returncode}
with concurrent.futures.ThreadPoolExecutor(max_workers=max(1,min(3,a.jobs//4))) as pool:
 result=list(pool.map(run,tasks.items()))
(scratch/'focused.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
