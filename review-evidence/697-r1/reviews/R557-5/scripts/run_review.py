#!/usr/bin/env python3
"""Run independent target validation concurrently, with bounded parallelism."""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parents[1]
scratch = packet / "scratch"
receipts = packet / "receipts"
env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
lexer = scratch / "clang18/usr/lib/llvm-18/bin/clang"
if lexer.exists():
    env["TSN_CLANG"] = str(lexer)
    env["LD_LIBRARY_PATH"] = str(scratch / "clang18/usr/lib/x86_64-linux-gnu")
commands = {
    "linux": [sys.executable, "scripts/validate.py", "--work", str(scratch / "linux"), "--jobs", "3"],
    "rv32": [sys.executable, "scripts/baremetal.py", "--work", str(scratch / "rv32"), "--jobs", "2"],
}

def run(item):
    name, argv = item
    with (receipts / (name + ".log")).open("w") as log:
        result = subprocess.run(argv, cwd=root, env=env, stdout=log, stderr=subprocess.STDOUT)
    (receipts / (name + ".rc")).write_text(str(result.returncode) + "\n")
    print(name, result.returncode, flush=True)
    return {"name": name, "argv": argv, "rc": result.returncode}

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    results = list(pool.map(run, commands.items()))
(receipts / "review-runs.json").write_text(json.dumps(results, indent=2) + "\n")
raise SystemExit(any(row["rc"] for row in results))
