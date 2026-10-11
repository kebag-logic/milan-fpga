#!/usr/bin/env python3
"""Run scoped review checks concurrently, with all children awaited."""
import argparse
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ap = argparse.ArgumentParser()
ap.add_argument("repo", type=Path)
ap.add_argument("--simulator-dir", type=Path, required=True)
a = ap.parse_args()
repo = a.repo.resolve()
packet = Path(__file__).resolve().parent
scratch = packet / "scratch"
scratch.mkdir(exist_ok=True)
logs = packet / "receipts"
logs.mkdir(exist_ok=True)
env = dict(os.environ, TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE="1", PYTHONUNBUFFERED="1")
env["PATH"] = str(a.simulator_dir.resolve()) + os.pathsep + env["PATH"]
identity = subprocess.check_output(["verilator", "--version"], env=env, text=True)
assert identity.startswith("Verilator 5.050 "), identity
(logs / "simulator-identity.log").write_text(identity)
wrapper = """import sys
from pathlib import Path
sys.path.insert(0, 'tb/verilator/nvm_cosim')
import run_cases as c
c.BUILD = Path(sys.argv[1]) / 'cosim-build'
c.RUNS = Path(sys.argv[1]) / 'cosim-runs'
sys.argv = ['run_cases.py', '--shapes', '1x1,8x8', '--jobs', '4', '--pool', '4', '--skip-mutants']
raise SystemExit(c.main())
"""
(scratch / "cosim_entry.py").write_text(wrapper)
commands = {
    "host-selftest": [sys.executable, "sw/firmware/nvm_hosttest/test_nvm_firmware.py", "--self-test", "--jobs", "4"],
    "cosim-shipping": [sys.executable, str(scratch / "cosim_entry.py"), str(scratch)],
    "capture-receipt": [sys.executable, "scripts/check_nvm_capture.py"],
}

def run(pair):
    name, cmd = pair
    start = time.monotonic()
    with (logs / (name + ".log")).open("w") as out:
        result = subprocess.run(cmd, cwd=repo, env=env, stdout=out, stderr=subprocess.STDOUT)
    elapsed = time.monotonic() - start
    (logs / (name + ".rc")).write_text(str(result.returncode) + "\n")
    print(f"{name}: rc={result.returncode}, elapsed={elapsed:.2f}s", flush=True)
    return {"check": name, "rc": result.returncode, "elapsed_seconds": round(elapsed, 2)}

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    rows = list(pool.map(run, commands.items()))
(logs / "checks-summary.json").write_text(json.dumps(rows, indent=2) + "\n")
raise SystemExit(int(any(row["rc"] for row in rows)))
