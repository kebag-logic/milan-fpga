#!/usr/bin/env python3
"""Run only issue-69 controls concurrently, with bounded compiler fanout."""
import argparse, concurrent.futures, importlib.util, json, os, pathlib, subprocess, time
p=argparse.ArgumentParser(); p.add_argument('--verilator',required=True); a=p.parse_args()
packet=pathlib.Path(__file__).resolve().parents[1]; tree=packet/'scratch/focus-head'; logs=packet/'receipts/controls'; logs.mkdir(parents=True,exist_ok=True)
def module(name,path):
 s=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
adp=module('adp_controls',tree/'tb/adp_engine/mutants.py')
notify=module('notify_controls',tree/'tb/pp_top/notify_mutants.py')
wrapper=packet/'scratch/bounded-verilator.py'
env=os.environ.copy(); env.update(VERILATOR=str(wrapper),R513_VERILATOR=str(pathlib.Path(a.verilator).resolve()),TMPDIR=str(packet/'scratch/tmp'),MAKEFLAGS='-j16',R513_COMPILE_JOBS='3')
units=[('adp', ['python3',str(tree/'tb/adp_engine/mutants.py'),'--output',str(logs/'adp'),'--jobs','2','--only',','.join(m[0] for m in adp.MUTANTS if m[0].startswith('if-'))]),
 ('notify',['python3',str(tree/'tb/pp_top/notify_mutants.py'),'--output',str(logs/'notify'),'--verilator',str(wrapper),'--jobs','2','--only',*[m.name for m in notify.INTERFACE_ROWS]])]
def run(u):
 name,cmd=u; start=time.monotonic()
 with (logs/(name+'.log')).open('w') as f:
  f.write('command: '+repr(cmd)+'\n'); f.flush(); r=subprocess.run(cmd,cwd=tree,env=env,stdout=f,stderr=subprocess.STDOUT)
 (logs/(name+'.rc')).write_text(str(r.returncode)+'\n'); row=dict(name=name,rc=r.returncode,seconds=round(time.monotonic()-start,2)); print(json.dumps(row),flush=True); return row
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool: results=list(pool.map(run,units))
(logs/'results.json').write_text(json.dumps(results,indent=2)+'\n')
raise SystemExit(any(r['rc'] for r in results))
