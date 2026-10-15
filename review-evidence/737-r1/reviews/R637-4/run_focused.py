#!/usr/bin/env python3
"""Run independent, bounded review checks concurrently; retain every result."""
import concurrent.futures, json, os, pathlib, subprocess, sys, time
root=pathlib.Path(sys.argv[1]).resolve(); out=pathlib.Path(__file__).resolve().parent
scratch=out/'scratch'; scratch.mkdir(exist_ok=True)
commands={
 'gate-workflows':['scripts/ci_gate_workflows_selftest.py'],
 'runtime-evidence':['scripts/ci_runtime_evidence_selftest.py'],
 'fail-fast':['scripts/ci_fail_fast_selftest.py'],
 'generator-check':['scripts/ci_gate_workflows.py','--check'],
 'events-check':['scripts/ci_events.py','--check'],
 'events-selftest':['scripts/ci_events.py','--selftest'],
 'evidence-pins':['scripts/generate_ci_evidence_pins.py','--check'],
 'manifest':['scripts/ci_manifest_selftest.py'],
 'workflow-plan':['scripts/ci_workflow_plan_selftest.py'],
 'case-receipts':['scripts/ci_case_receipts_selftest.py'],
}
def run(item):
 name,args=item; start=time.monotonic()
 env=dict(os.environ,TMPDIR=str(scratch),PYTHONDONTWRITEBYTECODE='1')
 with (out/(name+'.log')).open('w') as f:
  try: rc=subprocess.run([sys.executable,*args],cwd=root,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=560).returncode
  except subprocess.TimeoutExpired: rc=124
 (out/(name+'.rc')).write_text(str(rc)+'\n')
 result={'name':name,'argv':['python3',*args],'rc':rc,'seconds':round(time.monotonic()-start,3)}
 print(json.dumps(result),flush=True); return result
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool: results=list(pool.map(run,commands.items()))
(out/'focused-results.json').write_text(json.dumps(results,indent=2)+'\n')
raise SystemExit(int(any(r['rc'] for r in results)))
