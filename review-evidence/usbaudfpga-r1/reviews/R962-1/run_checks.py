#!/usr/bin/env python3
"""Run a selected bounded review campaign; all children finish before return."""
import argparse, json, os, subprocess, sys, time
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument('case', choices=['default','protocol','transport','render24','render32'])
p.add_argument('--repo',type=Path,required=True)
p.add_argument('--packet',type=Path,required=True)
p.add_argument('--engine',required=True)
a=p.parse_args()
root=a.repo.resolve(); packet=a.packet.resolve(); out=packet/'scratch'/a.case
receipts=packet/'receipts'; receipts.mkdir(exist_ok=True)
base=[sys.executable,'-B']
suite=root/'tb/verilator/usbaudio'
args=['--engine',a.engine,'--out',str(out),'--jobs','4']
if a.case=='default': cmd=base+[str(suite/'check.py')]+args
elif a.case=='protocol': cmd=base+[str(suite/'mutations.py')]+args
elif a.case=='transport':
 cmd=base+[str(suite/'transport_mutations.py')]+args+['--cleanup-ledger',str(out.parent/'transport-cleanup.log'),'--temporary-suffix','__ALL.verilator_deplist.tmp']
else:
 bits=a.case[-2:]; out.mkdir(parents=True,exist_ok=True)
 cmd=['make','-j16','-C',str(root/'tb/verilator/render_queue'),'build','VERILATOR='+a.engine,'VERILATOR_JOBS=4','SAMPLE_BITS='+bits,'MDIR='+str(out),'CPP='+str(root/'tb/verilator/render_queue/sim_main.cpp')]
env=os.environ.copy(); env['PYTHONDONTWRITEBYTECODE']='1'
start=time.time()
with (receipts/(a.case+'.log')).open('w') as log:
 log.write('COMMAND '+json.dumps(cmd)+'\n');log.flush()
 r=subprocess.run(cmd,cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT)
 if r.returncode==0 and a.case.startswith('render'):
  r=subprocess.run([str(out/'VKL_render_queue_sim')],stdout=log,stderr=subprocess.STDOUT)
(receipts/(a.case+'.rc')).write_text(str(r.returncode)+'\n')
print(json.dumps({'case':a.case,'rc':r.returncode,'seconds':round(time.time()-start,2)}),flush=True)
sys.exit(r.returncode)
