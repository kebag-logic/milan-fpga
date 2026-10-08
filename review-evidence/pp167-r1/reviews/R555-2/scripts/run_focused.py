#!/usr/bin/env python3
"""Foreground joined independent checks; all generated trees stay in scratch."""
import concurrent.futures,json,os,pathlib,subprocess,sys,time
root=pathlib.Path(sys.argv[1]).resolve(); packet=pathlib.Path(sys.argv[2]).resolve(); scratch=packet/'scratch'; receipts=packet/'receipts'
sim=str(packet/'scripts/limited_verilator.py'); head=scratch/'head'
if not head.exists():
    subprocess.run(['git','clone','--shared','--quiet','--no-checkout',str(root),str(head)],check=True)
    subprocess.run(['git','-C',str(head),'checkout','--quiet','--detach','1411117e646023cb236de02e3acaf9bdfcef49e3'],check=True)
binpath=scratch/'bin'; binpath.mkdir(exist_ok=True)
for name in ['verilator']:
    f=binpath/name
    if not f.exists(): f.symlink_to(sim)
env=os.environ.copy(); env['PATH']=str(binpath)+os.pathsep+env['PATH']; env['TMPDIR']=str(scratch); env['PYTHONDONTWRITEBYTECODE']='1'
def run(name,cmd,cwd):
    start=time.time()
    with (receipts/(name+'.log')).open('w') as log:
        rc=subprocess.run(cmd,cwd=cwd,env=env,stdout=log,stderr=subprocess.STDOUT).returncode
    (receipts/(name+'.rc')).write_text(str(rc)+'\n')
    rec={'name':name,'argv':cmd,'cwd':str(cwd.relative_to(packet)) if cwd.is_relative_to(packet) else str(cwd),'rc':rc,'seconds':round(time.time()-start,3)}
    (receipts/(name+'.json')).write_text(json.dumps(rec,indent=2)+'\n'); print(name,rc,flush=True); return rec
jobs=[('notify-suite',['make','-j16','VERILATOR='+sim],head/'tb/aecp_notify'),('originator-suite',['make','-j16','VERILATOR='+sim],head/'tb/originator'),('ca-originator-suite',['make','-j16','VERILATOR='+sim],head/'tb/ca_originator'),('focused-campaign',['python3','tb/pp_top/notify_mutants.py','--output',str(receipts/'focused-campaign'),'--verilator',sim,'--jobs','2','--only','cancel_collision_drops_command','cancel_pending_accepts_failure','cancel_one_clock_late','cancel_one_per_command'],head)]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool: result=list(pool.map(lambda a:run(*a),jobs))
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    result+=list(pool.map(lambda a:run(*a),[('make-check',['make','-j16','check'],head),('hdl-lint',['bash','scripts/lint_hdl.sh'],head),('matrix',['python3','scripts/gen_matrix.py','--check'],head)]))
(receipts/'focused-summary.json').write_text(json.dumps(result,indent=2)+'\n')
sys.exit(any(r['rc'] for r in result))
