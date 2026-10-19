#!/usr/bin/env python3
import concurrent.futures,pathlib,subprocess,os,time,shutil
p=pathlib.Path(__file__).resolve().parent
src=p/'scratch/source'; env=os.environ.copy(); env['REVIEW_BUILD_JOBS']='4'; env['TMPDIR']=str(p/'scratch/tmp'); env['MAKEFLAGS']='-j16'
wrap=str(p/'bounded-sim.py')
work={
 'descriptor-controls':['python3','tb/pp_top/aecp_dispatch_mutants.py','--output',str(p/'scratch/descriptor-controls'),'--verilator',wrap,'--jobs','2','--only','rdc-base-no-overlay,rdc-unit-shift-8,rdc-short-floor-111'],
 'notify-controls':['python3','tb/pp_top/notify_mutants.py','--output',str(p/'scratch/notify-controls'),'--verilator',wrap,'--jobs','2','--only','lock_coalesced_timeout_flags_zero','occupancy_cleared_beside_push'],
}
def run(item):
 name,cmd=item; start=time.monotonic()
 with (p/'receipts'/f'{name}.log').open('w') as f:
  f.write('Command: '+' '.join(cmd)+'\n');f.flush()
  rc=subprocess.run(cmd,cwd=src,env=env,stdout=f,stderr=subprocess.STDOUT).returncode
 (p/'receipts'/f'{name}.rc').write_text(str(rc)+'\n')
 r=p/'scratch'/name/'results.json'
 if r.exists(): shutil.copyfile(r,p/'receipts'/f'{name}-results.json')
 print(name,'rc',rc,'elapsed',round(time.monotonic()-start,1),flush=True)
 return rc
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool: results=list(pool.map(run,work.items()))
raise SystemExit(any(results))
