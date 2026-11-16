#!/usr/bin/env python3
"""Run the two focused application arms concurrently, retaining raw receipts."""
import concurrent.futures
import os
from pathlib import Path
import subprocess
import sys

repo = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
def run(interfaces):
    name = f"aecp-app-if{interfaces}"
    cmd = [sys.executable, "-B", "sw/firmware/ctrl/test/aecp_arms.py", "--app",
           "--interfaces", str(interfaces), "--output", str(packet / "scratch" / name)]
    env = dict(os.environ, TMPDIR=str(packet / "scratch"), PYTHONDONTWRITEBYTECODE="1")
    with (packet / f"{name}.log").open("w") as log:
        log.write("command: " + repr(cmd) + "\n"); log.flush()
        result = subprocess.run(cmd, cwd=repo, env=env, stdout=log, stderr=subprocess.STDOUT)
    (packet / f"{name}.rc").write_text(str(result.returncode) + "\n")
    print(name, result.returncode, flush=True)
    return result.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    results = list(pool.map(run, (1, 2)))
sys.exit(any(results))
