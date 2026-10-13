#!/usr/bin/env python3
"""Run a bounded foreground batch; retain each command, output and exit code."""
import argparse
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import time

p = argparse.ArgumentParser()
p.add_argument("spec", type=Path)
p.add_argument("--parallel", type=int, default=2)
a = p.parse_args()
spec = json.loads(a.spec.read_text())
base_env = dict(os.environ, **spec.get("env", {}))
out = Path(spec["receipts"])
out.mkdir(parents=True, exist_ok=True)

def one(job):
    name = job["name"]
    cmd = job["argv"]
    start = time.monotonic()
    print("START " + name, flush=True)
    with (out / (name + ".log")).open("w") as log:
        log.write("COMMAND " + json.dumps(cmd) + "\n")
        log.flush()
        try:
            result = subprocess.run(cmd, cwd=job.get("cwd", spec.get("cwd")),
                                    env=dict(base_env, **job.get("env", {})),
                                    stdout=log, stderr=subprocess.STDOUT,
                                    timeout=job.get("timeout", 7200))
            rc = result.returncode
        except subprocess.TimeoutExpired:
            rc = 124
            log.write("\nTIMEOUT\n")
        log.write(f"\nRECEIPT rc={rc} elapsed_s={time.monotonic()-start:.3f}\n")
    (out / (name + ".rc")).write_text(str(rc) + "\n")
    print(f"END {name} rc={rc} elapsed_s={time.monotonic()-start:.1f}", flush=True)
    return rc

with concurrent.futures.ThreadPoolExecutor(max_workers=a.parallel) as pool:
    results = list(pool.map(one, spec["jobs"]))
raise SystemExit(int(any(results)))
