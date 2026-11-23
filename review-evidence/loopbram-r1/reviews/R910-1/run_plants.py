#!/usr/bin/env python3
"""Run the published fault plants concurrently in disposable directories."""
import argparse, concurrent.futures, importlib.util, json, os, pathlib, subprocess, sys
sys.dont_write_bytecode=True
p=argparse.ArgumentParser(); p.add_argument('source',type=pathlib.Path); p.add_argument('--simulator',required=True); p.add_argument('--jobs',type=int,default=12); a=p.parse_args()
root=pathlib.Path(__file__).resolve().parent; out=root/'scratch'/'plants'; out.mkdir(exist_ok=True)
spec=importlib.util.spec_from_file_location('plants',a.source/'tb/verilator/input_loopback/mutants.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
source=m.QUEUE.read_text()
def run(plant):
 name,old,new,label=plant
 assert source.count(old)==1
 work=out/name; work.mkdir(exist_ok=True); rtl=work/'KL_render_queue.sv'; rtl.write_text(source.replace(old,new,1))
 cmd=['make','-j16','-s','-C',str(a.source/'tb/verilator/input_loopback'),'run','VERILATOR_JOBS=4','VERILATOR='+a.simulator,'MDIR='+str(work/'obj'),'QUEUE_SRC='+str(rtl)]
 with (work/'raw.log').open('w') as log: r=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,timeout=550)
 text=(work/'raw.log').read_text(); passed=r.returncode!=0 and 'FAIL '+label in text and 'FAIL input-loopback' in text
 (work/'rc').write_text(str(r.returncode)+'\n')
 return dict(plant=name,exit=r.returncode,detected=passed)
with concurrent.futures.ThreadPoolExecutor(max_workers=max(1,min(3,a.jobs//4))) as pool: results=list(pool.map(run,m.PLANTS))
(out/'results.json').write_text(json.dumps(results,indent=2)+'\n'); print(json.dumps(results))
raise SystemExit(0 if all(r['detected'] for r in results) else 1)
