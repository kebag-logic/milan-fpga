#!/usr/bin/env python3
"""Run focused review checks concurrently, retaining command, output and exit status."""
import concurrent.futures, json, os, pathlib, subprocess, sys, time
root = pathlib.Path(sys.argv[1]).resolve()
out = pathlib.Path(__file__).resolve().parent
scratch = out / "scratch"
scratch.mkdir(exist_ok=True)
commands = {
 "generator-check": ["python3", "scripts/ci_gate_workflows.py", "--check"],
 "generator-controls": ["python3", "scripts/ci_gate_workflows_selftest.py"],
 "event-check": ["python3", "scripts/ci_events.py", "--check"],
 "event-controls": ["python3", "scripts/ci_events.py", "--selftest"],
 "suite-controls": ["python3", "scripts/suite_shards.py", "--selftest"],
 "firmware-dispatch": ["python3", "sw/firmware/ctrl/test/test_ctrl_firmware_shards.py"],
 "runtime-controls": ["python3", "scripts/ci_runtime_evidence_selftest.py"],
 "cancel-controls": ["python3", "scripts/ci_fail_fast_selftest.py"],
}
def run(item):
 name, argv = item
 argv = [argv[0], str(root/argv[1]), *argv[2:]]
 started=time.monotonic()
 env=dict(os.environ, TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE="1")
 with (out/(name+".log")).open("w") as log:
  log.write("COMMAND: "+" ".join(argv)+"\n"); log.flush()
  try:
   result=subprocess.run(argv, cwd=scratch, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=540)
   rc=result.returncode
  except subprocess.TimeoutExpired:
   log.write("TIMEOUT after 540 seconds\n"); rc=124
 elapsed=round(time.monotonic()-started,3)
 (out/(name+".rc")).write_text(str(rc)+"\n")
 return dict(name=name, command=argv, rc=rc, seconds=elapsed)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 rows=list(pool.map(run, commands.items()))
(out/"checks.json").write_text(json.dumps(rows, indent=2)+"\n")
for row in rows: print(row["name"], row["rc"], row["seconds"], flush=True)
raise SystemExit(int(any(row["rc"] for row in rows)))
