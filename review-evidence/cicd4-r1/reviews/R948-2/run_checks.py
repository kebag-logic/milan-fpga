#!/usr/bin/env python3
"""Run bounded independent checks concurrently; wait for all foreground children."""
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess
import sys
import time

root = Path(sys.argv[1]).resolve()
out = Path(__file__).resolve().parent
commands = {
    "workflow-bytes": ["python3", "scripts/ci_gate_workflows.py", "--check"],
    "event-contract": ["python3", "scripts/ci_events.py", "--check"],
    "fast-legs": ["python3", "scripts/ci_fast_legs_selftest.py"],
    "schedule": ["python3", "scripts/suite_shards.py", "--selftest"],
    "documentation": ["python3", "scripts/docs_check.py"],
    "delta-probes": ["python3", str(out / "probe_delta.py"), str(root)],
}
def run(item):
    name, command = item
    work = out / "scratch" / name
    work.mkdir(parents=True,exist_ok=True)
    command = [str(root / arg) if arg.startswith("scripts/") else arg for arg in command]
    start = time.monotonic()
    with (out / (name + ".log")).open("w") as log:
        result = subprocess.run(command, cwd=work, stdout=log, stderr=subprocess.STDOUT,
                                env={**os.environ,"PYTHONDONTWRITEBYTECODE":"1", "TMPDIR":str(work)}, timeout=550)
    record = {"name":name,"command":command,"rc":result.returncode,"seconds":round(time.monotonic()-start,3)}
    (out / (name+".rc")).write_text(str(result.returncode)+"\n")
    return record
with ThreadPoolExecutor(max_workers=6) as pool:
    results = list(pool.map(run, commands.items()))
(out / "checks.json").write_text(json.dumps(results,indent=2)+"\n")
print(json.dumps(results,indent=2))
raise SystemExit(any(r["rc"] for r in results))
