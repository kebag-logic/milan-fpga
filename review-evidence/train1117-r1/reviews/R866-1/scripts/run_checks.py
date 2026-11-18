#!/usr/bin/env python3
import concurrent.futures, os, pathlib, subprocess, sys, time
P=pathlib.Path(__file__).resolve().parents[1]
R=P/'receipts/checks'; R.mkdir(parents=True,exist_ok=True)
env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(P/'scratch'))
py=os.environ.get('DOCS_PYTHON', '$VALIDATION_TOOLS/md-venv/bin/python' if pathlib.Path('$VALIDATION_TOOLS/md-venv/bin/python').exists() else sys.executable)
jobs={
 'history':[sys.executable,str(P/'scripts/check_history.py')],
 'docs':[py,'scripts/docs_check.py'],
 'idiom':[sys.executable,'scripts/check_py_idiom.py'],
 'hygiene':[sys.executable,'scripts/check_hygiene.py','--check'],
 'flip1':[sys.executable,'-B','tb/verilator/ctrl_service_budget/flip_grade.py','--check','--point','1x1/1if'],
 'flip8':[sys.executable,'-B','tb/verilator/ctrl_service_budget/flip_grade.py','--check','--point','8x8/1if'],
 'flip-controls':[sys.executable,'-B','tb/verilator/ctrl_service_budget/flip_grade.py','--selftest'],
 'load':[sys.executable,'-B','tb/verilator/ctrl_service_budget/load_grade.py','--check'],
 'load-controls':[sys.executable,'-B','tb/verilator/ctrl_service_budget/load_grade.py','--selftest'],
 'run-controls':[sys.executable,'-B','tb/verilator/ctrl_service_budget/run.py','--self-test'],
 'baseline':[sys.executable,'syn/ooc/pp_resource_gate.py','check-baseline'],
 'baseline-controls':[sys.executable,'syn/ooc/pp_resource_gate.py','--selftest'],
}
def run(item):
 name,cmd=item
 with (R/(name+'.log')).open('w') as f:
  f.write('COMMAND '+repr(cmd)+'\n'); f.flush()
  try: rc=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,env=env,timeout=500).returncode
  except subprocess.TimeoutExpired: rc=124
 (R/(name+'.rc')).write_text(str(rc)+'\n')
 print(name,rc,flush=True)
 return rc
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 results=list(pool.map(run,jobs.items()))
sys.exit(any(results))
