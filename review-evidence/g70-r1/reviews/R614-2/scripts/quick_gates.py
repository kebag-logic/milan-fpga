#!/usr/bin/env python3
"""Run independent light gates concurrently; no background processes outlive it.

Usage: quick_gates.py REPO PACKET PINNED_VERILATOR
"""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import os
from pathlib import Path
import subprocess
import sys

repo, packet, verilator = map(lambda p: Path(p).resolve(), sys.argv[1:])
out = packet / "receipts" / "quick"
out.mkdir(parents=True, exist_ok=True)
tmp = packet / "scratch" / "tmp"
tmp.mkdir(parents=True, exist_ok=True)
env = dict(os.environ, PATH=str(verilator.parent) + os.pathsep + os.environ["PATH"], TMPDIR=str(tmp), PYTHONDONTWRITEBYTECODE="1")
identity = subprocess.check_output([str(verilator), "--version"], text=True, env=env)
(out / "identity.txt").write_text(identity)
assert identity.startswith("Verilator 5.050 "), identity
tasks = [("docs", ["make", "-j16", "docs"]),
         ("contract", ["make", "-j16", "contract"]),
         ("lint", ["make", "-j16", "lint"]),
         ("selftest", ["python3", "-B", "syn/ooc/check_ooc_clock.py", "--selftest"]),
         ("static", ["python3", "-B", "syn/ooc/check_ooc_clock.py"])]
def run(task):
    name, cmd = task
    start = datetime.now(timezone.utc).isoformat()
    with (out / (name + ".log")).open("w") as log:
        result = subprocess.run(cmd, cwd=repo, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=540)
    (out / (name + ".rc")).write_text(str(result.returncode) + "\n")
    (out / (name + ".time")).write_text(start + "\n" + datetime.now(timezone.utc).isoformat() + "\n")
    return name, result.returncode
with ThreadPoolExecutor(max_workers=len(tasks)) as pool:
    results = list(pool.map(run, tasks))
for name, rc in results:
    print(f"{name}: rc={rc}")
sys.exit(any(rc for _, rc in results))
