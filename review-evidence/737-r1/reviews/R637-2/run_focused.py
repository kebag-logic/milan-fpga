#!/usr/bin/env python3
"""Run allowed lightweight review controls concurrently, retaining receipts."""
import concurrent.futures, json, os, pathlib, subprocess, sys, time
root=pathlib.Path(sys.argv[1]).resolve()
packet=pathlib.Path(__file__).resolve().parent
scratch=packet/"scratch"; scratch.mkdir(exist_ok=True)
logs=packet/"focused"; logs.mkdir(exist_ok=True)
names=["ci_case_receipts_selftest", "ci_make_cases_selftest", "ci_maap_cases_selftest", "ci_capture_cases_selftest", "ci_suite_pieces_selftest", "ci_suite_collect_selftest", "ci_manifest_selftest", "ci_workflow_plan_selftest", "ci_runtime_evidence_selftest", "ci_fail_fast_selftest", "ci_install_cache_selftest", "ci_gate_workflows_selftest"]
commands=[["python3", "scripts/"+name+".py"] for name in names]
commands += [["python3","scripts/ci_gate_workflows.py","--check"],["python3","scripts/suite_shards.py","--selftest"],["python3","scripts/ci_events.py","--check"],["python3","scripts/ci_events.py","--selftest"]]
names += ["workflow_regeneration", "suite_headroom", "event_contract", "event_controls"]
env=dict(os.environ, TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE="1", PYTHONPYCACHEPREFIX=str(scratch/"pycache"))
def run(item):
 name,cmd=item
 start=time.monotonic()
 with (logs/(name+".log")).open("w") as log:
  try: rc=subprocess.run(cmd,cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=420).returncode
  except subprocess.TimeoutExpired: rc=124
 (logs/(name+".rc")).write_text(str(rc)+"\n")
 return {"name":name,"command":cmd,"returncode":rc,"seconds":round(time.monotonic()-start,2)}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 rows=list(pool.map(run,zip(names,commands)))
(packet/"focused-results.json").write_text(json.dumps(rows,indent=2)+"\n")
for row in rows:print(row)
raise SystemExit(int(any(row["returncode"] for row in rows)))
