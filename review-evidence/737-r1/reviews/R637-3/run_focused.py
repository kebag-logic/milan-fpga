#!/usr/bin/env python3
"""Run independent focused checks concurrently; retain exits and timing."""
import concurrent.futures, json, os, pathlib, subprocess, sys, time
root=pathlib.Path(sys.argv[1]).resolve()
out=pathlib.Path(__file__).resolve().parent
commands={
 "events-check":["scripts/ci_events.py","--check"],
 "events-selftest":["scripts/ci_events.py","--selftest"],
 "generator-check":["scripts/ci_gate_workflows.py","--check"],
 "evidence-pins":["scripts/generate_ci_evidence_pins.py","--check"],
 "baremetal-check":["scripts/check_baremetal_only.py","--check"],
 "baremetal-selftest":["scripts/check_baremetal_only.py","--selftest"],
 "suite-shards":["scripts/suite_shards.py","--selftest"],
}
for name in ('gate_workflows','case_receipts','make_cases','maap_cases','capture_cases','suite_pieces','suite_collect','fail_fast','runtime_evidence','install_cache','workflow_plan','manifest'):
 commands[name]=['scripts/ci_'+name+'_selftest.py']
env={**os.environ,'TMPDIR':str(out/'scratch'),'PYTHONDONTWRITEBYTECODE':'1'}
def run(item):
 name,args=item; start=time.monotonic()
 with (out/(name+'.log')).open('w') as log:
  p=subprocess.run([sys.executable,*args],cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=590)
 record={'command':['python3',*args],'rc':p.returncode,'seconds':round(time.monotonic()-start,3)}
 (out/(name+'.rc')).write_text(str(p.returncode)+'\n')
 print(name,record,flush=True)
 return name,record
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 results=dict(pool.map(run,commands.items()))
(out/'focused-results.json').write_text(json.dumps(results,indent=2)+'\n')
raise SystemExit(any(r['rc'] for r in results.values()))
