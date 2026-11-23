import os,subprocess,json,time,concurrent.futures
from pathlib import Path
root=Path('$CHECKOUT');w=Path('$SCRATCH/builder-union');w.mkdir(exist_ok=True)
env=dict(os.environ,LITEX_PYTHON='<home-path>/litex-milan/venv/bin/python3',PATH='<home-path>/litex-milan/venv/bin:/usr/local/bin:/usr/bin:/bin',PYTHONHASHSEED='0',VERILATOR_JOBS='4')
def run(leg):
 cmd=['python3','scripts/ci_builder_legs.py','run',str(leg),'--receipt',str(w/('leg'+str(leg)+'.json')),'--','python3','sw/builder/test_builder.py','--require-elaboration','--require-rv32']
 with (w/('leg'+str(leg)+'.log')).open('w') as log:r=subprocess.run(cmd,cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=10800)
 print('BUILDER LEG',leg,r.returncode,flush=True);return r.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(run,[0,1]))
if any(results):raise SystemExit(1)
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
tree=subprocess.check_output(['git','rev-parse','HEAD^{tree}'],cwd=root,text=True).strip()
cmd=['python3','scripts/ci_builder_legs.py','union','--workflow','elaborate','--head',head,'--tree',tree,'--output',str(w/'union.json'),str(w/'leg0.json'),str(w/'leg1.json')]
with (w/'union.log').open('w') as log:r=subprocess.run(cmd,cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=600)
print('BUILDER UNION',r.returncode,flush=True);raise SystemExit(r.returncode)
