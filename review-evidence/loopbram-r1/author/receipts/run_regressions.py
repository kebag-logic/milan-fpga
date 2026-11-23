import os,subprocess,time,json,concurrent.futures
from pathlib import Path
root=Path('$CHECKOUT');w=Path('$SCRATCH/regressions');w.mkdir(exist_ok=True)
# Two independent workers. Each make and each native model remains foreground.
cases=[('input8','input_loopback',['run','MDIR='+str(w/'input8')]),
('input1','input_loopback',['run','STREAMS=1','FIRST=8','CHANNELS=8','LEAD=2','MDIR='+str(w/'input1')]),
('capture','chmap_capture',['run','MDIR='+str(w/'capture')]),
('queue','render_queue',['all']),
('render','milan_dp_render',['run','ship8']),
('coherence','capture_coherence',['run','dp'])]
def run(case):
 name,directory,extra=case;cmd=['make','-s','-C',str(root/'tb/verilator'/directory),'VERILATOR_JOBS=4',*extra];t=time.time()
 with (w/(name+'.log')).open('w') as log:r=subprocess.run(cmd,cwd=root,stdout=log,stderr=subprocess.STDOUT,timeout=7200)
 result={'case':name,'command':cmd,'exit':r.returncode,'seconds':time.time()-t};(w/(name+'.json')).write_text(json.dumps(result,indent=2));print(name,r.returncode,flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(run,cases))
