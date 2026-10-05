#!/usr/bin/env python3
"""Foreground, bounded concurrent F0 checks; no checkout edits."""
import argparse, concurrent.futures, os, pathlib, shutil, subprocess, sys, time
ap=argparse.ArgumentParser();ap.add_argument('repo',type=pathlib.Path);ap.add_argument('--verilator',required=True);args=ap.parse_args()
r=args.repo.resolve(); p=pathlib.Path(__file__).resolve().parents[1]; scratch=p/'scratch'; logs=p/'receipts'
env=dict(os.environ,TMPDIR=str(scratch),PYTHONDONTWRITEBYTECODE='1',VERILATOR=args.verilator)
# Every executable and copy remains below scratch.
b=scratch/'cosim-tree';shutil.copytree(r/'tb/verilator/mbx',b/'tb/verilator/mbx',dirs_exist_ok=True);shutil.copytree(r/'tb/common',b/'tb/common',dirs_exist_ok=True)
vflags=subprocess.check_output(['make','-s','print-vflags'],cwd=r/'tb/verilator/mbx',env=env,text=True).splitlines()[1:]
# Replace the recipe's unlimited build count with four.
for i in range(len(vflags)-1):
 if vflags[i]=='-j': vflags[i+1]='4'
import shlex
jobs=[('contract-check',[sys.executable,'-B','sw/mailbox/gen_mailbox.py','--check','--crosscheck'],r),
('contract-selftest',[sys.executable,'-B','sw/mailbox/gen_mailbox.py','--selftest'],r),
('firmware',[sys.executable,'-B','sw/firmware/ctrl/test/test_ctrl_firmware.py','--require-rv32','--self-test','--lwsrp',str(scratch/'lwsrp'),'--build-dir',str(scratch/'firmware')],r),
('rtl-mutants',[sys.executable,'-B','tb/verilator/mbx/mutants.py','--jobs','2','--keep',str(scratch/'rtl-mutants')],r),
('cosim',['make','-j16','run-cosim','ROOT='+str(r),'VERILATOR='+args.verilator,'VFLAGS='+shlex.join(vflags)],b/'tb/verilator/mbx')]
def run(job):
 name,cmd,cwd=job
 with (logs/(name+'.log')).open('w') as f:
  f.write('COMMAND: '+shlex.join(cmd)+'\n');f.flush();start=time.monotonic()
  try: rc=subprocess.run(cmd,cwd=cwd,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=2400).returncode
  except subprocess.TimeoutExpired: rc=124
  f.write(f'\nRC: {rc} ELAPSED_SECONDS: {time.monotonic()-start:.3f}\n')
 (logs/(name+'.rc')).write_text(str(rc)+'\n');print(name,rc,flush=True);return rc
# At most 2*4 RTL compilers + 4 cosim compilers + one firmware compiler.
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool: results=list(pool.map(run,jobs))
sys.exit(any(results))
