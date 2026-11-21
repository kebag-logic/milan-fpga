#!/usr/bin/env python3
"""Run bounded independent receive-stack checks; no tracked source changes."""
import concurrent.futures, os, pathlib, subprocess, sys
root=pathlib.Path(sys.argv[1]).resolve()
packet=pathlib.Path(__file__).resolve().parent
scratch=packet/'scratch'; scratch.mkdir(exist_ok=True)
wrapper=scratch/'bounded-verilator'
wrapper.write_text("#!/usr/bin/env python3\nimport os,sys\na=sys.argv[1:]\nfor i in range(len(a)-1):\n if a[i]=='-j': a[i+1]='4'\nos.execv(os.environ['REVIEW_VERILATOR'],[os.environ['REVIEW_VERILATOR']]+a)\n")
wrapper.chmod(0o755)
env=os.environ.copy();env['REVIEW_VERILATOR']=env.get('REVIEW_VERILATOR','$VALIDATION_TOOLS/pinned-verilator-5.050/verilator');env['VERILATOR']=str(wrapper);env['TMPDIR']=str(scratch);env['PYTHONDONTWRITEBYTECODE']='1'
suite=root/'tb/verilator/avtp_rxmon'
def job(item):
 name,cmd=item
 with (packet/(name+'.log')).open('w') as log:
  log.write('Command: '+repr(cmd)+'\n');log.flush()
  r=subprocess.run(cmd,cwd=suite,env=env,stdout=log,stderr=subprocess.STDOUT)
 (packet/(name+'.rc')).write_text(str(r.returncode)+'\n')
 return name,r.returncode
jobs=[('fanout-mutants',['python3','-B','fanout_mutants.py']),('lockstep',['make','-j16','lockstep','LS_MDIR='+str(scratch/'obj_ls')])]
# The lockstep recipe prefixes ./ to LS_MDIR, so run its build and executables explicitly.
jobs[1]=('lockstep-build',['make','-j16','lockstep-build','LS_MDIR='+str(scratch/'obj_ls')])
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 for result in pool.map(job,jobs): print(result,flush=True)
for n in (1,8): print(job(('lockstep-'+str(n),[str(scratch/('obj_ls'+str(n))/'Vavtp_rxmon_lockstep')])),flush=True)
