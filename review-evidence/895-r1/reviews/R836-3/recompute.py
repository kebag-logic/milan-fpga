#!/usr/bin/env python3
"""Reproduce bounded analytical checks; no source mutation or build banks."""
import concurrent.futures
import os
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
out = Path(__file__).resolve().parent
scratch = out / "scratch"
scratch.mkdir(exist_ok=True)
env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", TMPDIR=str(scratch))
commands = {
    "flip-1x1": ["python3", "-I", "tb/verilator/ctrl_service_budget/flip_grade.py", "--check", "--point", "1x1/1if"],
    "load": ["python3", "-I", "tb/verilator/ctrl_service_budget/load_grade.py", "--check"],
    "tier-grid": ["python3", "-I", "tb/verilator/ctrl_service_budget/tier_grid.py", "--point", "1x1/1if"],
    "memory-ledger": ["python3", "-I", "sw/litex/test_ctrl_memory.py"],
}

def run(item):
    name, argv = item
    with (out / (name + ".log")).open("w") as log:
        log.write("Command: " + " ".join(argv) + "\n")
        log.flush()
        p = subprocess.run(argv, cwd=root, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=540)
    (out / (name + ".rc")).write_text(str(p.returncode) + "\n")
    return name, p.returncode

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    for name, rc in pool.map(run, commands.items()):
        print(name, rc, flush=True)
