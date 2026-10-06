#!/usr/bin/env python3
"""Run default, alternate VID, and response-budget builds concurrently in the review copy."""
import argparse,concurrent.futures,os,pathlib,shlex,subprocess,time
ap=argparse.ArgumentParser();ap.add_argument('--packet',type=pathlib.Path,required=True);ap.add_argument('--verilator',required=True);a=ap.parse_args();p=a.packet.resolve();s=p/'scratch';cwd=s/'focused-source/tb/pp_top';out=p/'receipts/top-checks';out.mkdir(exist_ok=True);v=str(s/'bin/verilator-capped')
env=os.environ.copy();env.update(PATH=str(s/'bin')+os.pathsep+env['PATH'],REVIEW_VERILATOR=str(pathlib.Path(a.verilator).resolve()),TMPDIR=str(s))
with (out/'roms.log').open('w') as f:
 rc=subprocess.run(['make','-j16','ltn_rom.hex','ucode.hex'],cwd=cwd,env=env,stdout=f,stderr=subprocess.STDOUT).returncode
assert rc==0
# Take exact compile recipes from this head's Makefile, without running the full suite bank.
raw=subprocess.check_output(['make','-n','-j16','run','VERILATOR='+v],cwd=cwd,env=env,text=True).replace('\\\n',' ')
compile_cmds=[shlex.split(l) for l in raw.splitlines() if l.startswith(v+' ')]
wanted={'default':'Vpp_top_sim','alternate-vid':'Vpp_top_vid','response-budget':'Vpp_top_tim'}
def job(item):
 name,binary=item;cmd=next(c for c in compile_cmds if c[-1]==binary);mdir=cmd[cmd.index('--Mdir')+1] if '--Mdir' in cmd else 'obj_dir';start=time.monotonic()
 with (out/(name+'.log')).open('w') as f:
  f.write('COMMAND '+repr(cmd)+'\n');f.flush();rc=subprocess.run(cmd,cwd=cwd,env=env,stdout=f,stderr=subprocess.STDOUT).returncode
  if rc==0:rc=subprocess.run(['./'+mdir+'/'+binary],cwd=cwd,env=env,stdout=f,stderr=subprocess.STDOUT).returncode
 (out/(name+'.rc')).write_text(str(rc)+'\n');print(name,'rc',rc,'seconds',round(time.monotonic()-start,1),flush=True);return rc
with concurrent.futures.ThreadPoolExecutor(3) as pool:rs=list(pool.map(job,wanted.items()))
assert not any(rs),rs
