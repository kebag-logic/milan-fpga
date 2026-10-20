import concurrent.futures, os, subprocess, sys, time
from pathlib import Path
P=Path(__file__).resolve().parents[1]
ROOT=Path(sys.argv[1]).resolve()
scratch=P/"scratch";scratch.mkdir(exist_ok=True)
wrapper=scratch/"verilator"
wrapper.write_text("#!/usr/bin/env python3\nimport os,sys\na=sys.argv[1:]\nfor i in range(len(a)-1):\n if a[i] == '-j': a[i+1]='2'\nos.execv('$VALIDATION_TOOLS/pinned-verilator-5.050/verilator',['verilator']+a)\n")
wrapper.chmod(0o755)
env=os.environ.copy();env.update(TMPDIR=str(scratch),VERILATOR=str(wrapper),MAKEFLAGS="-j16",PATH=str(scratch)+os.pathsep+env['PATH'])
subprocess.run(['$VALIDATION_TOOLS/pinned-verilator-5.050/verilator','--version'],stdout=(P/'receipts/simulator-identity.txt').open('w'),check=True)
jobs=[('acmp-focused',[sys.executable,'tb/pp_top/acmp_mutants.py','--output',str(P/'receipts/acmp-focused'),'--verilator',str(wrapper),'--jobs','2','--only','tk_failed_first_payload']),('srp-focused',[sys.executable,'tb/srp_top/mutants.py','--output',str(P/'receipts/srp-focused'),'--jobs','4','--only','listener-csid-ram-ignores-park,listener-rebind-back-keeps-park,listener-lo-not-owed,listener-park-retires-on-txla,listener-parked-applies-rx,listener-unrecorded-applicant-owes'])]
def run(job):
 name,cmd=job;t=time.monotonic()
 with (P/f'receipts/{name}.log').open('w') as out:r=subprocess.run(cmd,cwd=ROOT,env=env,stdout=out,stderr=subprocess.STDOUT)
 (P/f'receipts/{name}.rc').write_text(str(r.returncode)+'\n')
 (P/f'receipts/{name}.sec').write_text(str(round(time.monotonic()-t,2))+'\n')
 print(name,r.returncode,flush=True)
 return r.returncode
with concurrent.futures.ThreadPoolExecutor(2) as pool:rc=list(pool.map(run,jobs))
sys.exit(any(rc))
