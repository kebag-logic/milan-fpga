#!/usr/bin/env python3
"""Focused read-only checks; usage: run_checks.py CHECKOUT PACKET."""
import concurrent.futures,os,pathlib,subprocess,sys
root=pathlib.Path(sys.argv[1]).resolve(); packet=pathlib.Path(sys.argv[2]).resolve()
checks={
'capture':['python3','scripts/check_nvm_capture.py'],
'ports':['python3','scripts/check_port_contracts.py'],
'naming':['python3','scripts/measure_naming.py','--check'],
'pins':['python3','scripts/check_submodule_docs.py'],
'diagram':['python3','docs/diagrams/submodule_boundaries.gen.py','--check'],
'evidence':['python3','scripts/measure_test_evidence.py','--check'],
'baseline':['python3','syn/ooc/pp_resource_gate.py','check-baseline'],
'params':['python3','protocol-processor/scripts/check-integrator-params.py'],
}
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(packet/'scratch'))
def run(item):
 name,cmd=item
 with (packet/(name+'.log')).open('w') as log:
  log.write('COMMAND '+' '.join(cmd)+'\n');log.flush()
  rc=subprocess.run(cmd,cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT).returncode
 (packet/(name+'.rc')).write_text(str(rc)+'\n')
 print(name,rc,flush=True)
 return rc
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: codes=list(pool.map(run,checks.items()))
sys.exit(any(codes))
