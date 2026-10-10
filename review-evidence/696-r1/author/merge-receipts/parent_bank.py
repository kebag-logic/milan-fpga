import json,os,shutil,signal,subprocess,sys,time
from pathlib import Path
signal.signal(signal.SIGHUP, signal.SIG_DFL)
repo=Path(sys.argv[1]).resolve(); work=Path(__file__).resolve().parent
head=subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip()
subprocess.run(['git','-C',str(repo),'diff','--quiet'],check=True)
env=dict(os.environ,TMPDIR=str(work/'tmp'),PYTHONDONTWRITEBYTECODE='1',VERILATOR=str(work/'bin/verilator'),VERILATOR_JOBS='2',MAKEFLAGS='-j8',JOBS='4',POOL='2',LAW_BOUNDARY_JOBS='4',START_JOBS='4',SIM_JOBS='2',MILAN_RV32_CC='<sdk>/bin/riscv32-linux-gcc')
env['PATH']=str(work/'bin')+os.pathsep+'<litex-env>/bin'+os.pathsep+env['PATH']
(work/'tmp').mkdir(exist_ok=True)
assert shutil.disk_usage(work).free > 30*1024**3
name=sys.argv[2] if len(sys.argv)>2 else 'parent-suites'
args=['bash','scripts/run_all_suites.sh',str(work/(name+'-logs'))]
print('START',name,head,flush=True);start=time.time()
with (work/(name+'.log')).open('w') as log:
 rc=subprocess.run(args,cwd=repo,env=env,stdout=log,stderr=subprocess.STDOUT).returncode
(work/(name+'.rc')).write_text(str(rc)+'\n')
row=dict(name=name,argv=args,rc=rc,head=head,seconds=round(time.time()-start,1));print(row,flush=True)
(work/(name+'-results.json')).write_text(json.dumps([row],indent=2)+'\n')
raise SystemExit(rc)
