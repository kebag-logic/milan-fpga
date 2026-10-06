#!/usr/bin/env python3
"""Focused CI, coverage-control, and documentation checks; no builder bank."""
import os,pathlib,subprocess,sys,json,time
repo=pathlib.Path(sys.argv[1]).resolve();packet=pathlib.Path(__file__).resolve().parents[1]
env={**os.environ,'TMPDIR':str(packet/'scratch/tmp'),'PYTHONDONTWRITEBYTECODE':'1','PYTHON_CPU_COUNT':'1','PYTHONUNBUFFERED':'1'}
checks={
'ci-events-check':['scripts/ci_events.py','--check'],
'ci-events-selftest':['scripts/ci_events.py','--selftest'],
'ci-scope-selftest':['scripts/ci_scope.py','--selftest'],
'coverage-selftest':['sw/firmware/gtest/fw_coverage.py','--selftest'],
'docs-check':['scripts/docs_check.py'],
'doc-style':['scripts/check_doc_style.py'],
'em-dash':['scripts/check_em_dash.py','--base','6714181d0c8a16e2983f85b724f4d688f5111835'],
}
results={}
for name,args in checks.items():
 start=time.monotonic()
 with (packet/'scratch/raw'/(name+'.log')).open('w') as log:
  r=subprocess.run([sys.executable,*args],cwd=repo,env=env,stdout=log,stderr=subprocess.STDOUT)
 (packet/'receipts'/(name+'.rc')).write_text(str(r.returncode)+'\n')
 results[name]={'command':['python3',*args],'rc':r.returncode,'elapsed_seconds':round(time.monotonic()-start,2)}
 print(name,r.returncode,flush=True)
(packet/'receipts/contract-checks.json').write_text(json.dumps(results,indent=2)+'\n')
sys.exit(any(r['rc'] for r in results.values()))
