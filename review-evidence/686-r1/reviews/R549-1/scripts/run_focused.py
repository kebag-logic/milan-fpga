#!/usr/bin/env python3
"""Run one scoped campaign in foreground, with capped compilation and raw receipts."""
import argparse, os, pathlib, subprocess, sys
p=argparse.ArgumentParser(); p.add_argument('kind', choices=['mutants','differential']); p.add_argument('--repo', type=pathlib.Path, required=True); p.add_argument('--verilator', required=True)
a=p.parse_args(); packet=pathlib.Path(__file__).resolve().parents[1]; repo=a.repo.resolve()
scratch=packet/'scratch'; out=packet/'receipts'; scratch.mkdir(exist_ok=True); out.mkdir(exist_ok=True)
env=os.environ.copy(); env.update(TMPDIR=str(scratch), VERILATOR_JOBS='4', MAKEFLAGS='-j16', PYTHONDONTWRITEBYTECODE='1')
# The differential hardcodes -j 8; an executable adapter enforces this review's cap.
adapter=scratch/'verilator_capped.py'
adapter.write_text("#!/usr/bin/env python3\nimport os, sys\na=sys.argv[1:]\nfor i in range(len(a)-1):\n    if a[i] in ('-j','--jobs','--build-jobs'): a[i+1]='4'\nos.execv(os.environ['REVIEW_VERILATOR'], [os.environ['REVIEW_VERILATOR'], *a])\n")
adapter.chmod(0o755); env['REVIEW_VERILATOR']=a.verilator; env['VERILATOR']=str(adapter)
if a.kind=='mutants': argv=[sys.executable,str(repo/'tb/verilator/maap/mutants.py')]
else: argv=[sys.executable,str(repo/'sw/firmware/ctrl/test/maap_differential.py'),'--self-test','--keep',str(scratch/'differential')]
with (out/(a.kind+'.log')).open('w') as log:
    result=subprocess.run(argv,cwd=repo,env=env,stdout=log,stderr=subprocess.STDOUT)
(out/(a.kind+'.rc')).write_text(str(result.returncode)+'\n')
print(a.kind+': rc='+str(result.returncode)); print((out/(a.kind+'.log')).read_text()[-5500:]); sys.exit(result.returncode)
