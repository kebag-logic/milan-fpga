#!/usr/bin/env python3
"""Run bounded source controls concurrently, retaining each command, status and log."""
import concurrent.futures, json, os, pathlib, subprocess, sys, time
root=pathlib.Path(sys.argv[1]).resolve(); packet=pathlib.Path(__file__).resolve().parents[1]
tmp=packet/'scratch/tmp'; tmp.mkdir(parents=True,exist_ok=True)
env=dict(os.environ,TMPDIR=str(tmp),PYTHONDONTWRITEBYTECODE='1',MAKEFLAGS='-j16 --no-print-directory',VERILATOR_JOBS='4',SIM_JOBS='4')
tests=[('workflow-generation',['scripts/ci_gate_workflows.py','--check']),('event-contract',['scripts/ci_events.py','--check']),('workflow-controls',['scripts/ci_gate_workflows_selftest.py']),('pieces-controls',['scripts/ci_suite_pieces_selftest.py']),('case-controls',['scripts/ci_make_cases_selftest.py']),('stage-controls',['scripts/mutant_stage.py','--selftest']),('fail-fast-controls',['scripts/ci_fail_fast_selftest.py']),('lifecycle-controls',['tb/verilator/gptp_shadow/test_mutant_lifecycle.py']),('receipt-controls',['scripts/ci_case_receipts_selftest.py']),('runtime-controls',['scripts/ci_runtime_evidence_selftest.py']),('preflight',['scripts/run_all_suites.sh',str(packet/'scratch/preflight'),'--preflight-only'])]
launcher="import os,runpy,sys,tempfile; tempfile.tempdir=os.environ['TMPDIR']; p=sys.argv.pop(1); sys.path.insert(0,os.path.dirname(p)); runpy.run_path(p,run_name='__main__')"
def run(row):
 name,args=row; cmd=['bash',*args] if args[0].endswith('.sh') else [sys.executable,'-c',launcher,*args]
 begin=time.monotonic()
 with (packet/'receipts'/f'{name}.log').open('w') as log:
  proc=subprocess.run(cmd,cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=550)
 record={'name':name,'command':args,'returncode':proc.returncode,'wall_seconds':round(time.monotonic()-begin,3)}
 (packet/'receipts'/f'{name}.rc').write_text(str(proc.returncode)+'\n'); print(json.dumps(record),flush=True); return record
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool: results=list(pool.map(run,tests))
(packet/'receipts/controls.json').write_text(json.dumps(results,indent=2)+'\n')
