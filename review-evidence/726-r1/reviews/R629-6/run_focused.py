#!/usr/bin/env python3
"""Run focused counter checks concurrently, retaining raw logs and return codes."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess
import sys

p = argparse.ArgumentParser()
p.add_argument("--root", type=Path, required=True)
p.add_argument("--packet", type=Path, default=Path(__file__).resolve().parent)
p.add_argument("--verilator", required=True)
p.add_argument("--jobs", type=int, default=2)
p.add_argument("tasks", nargs="+")
a = p.parse_args()
root, packet = a.root.resolve(), a.packet.resolve()
env = dict(os.environ, VERILATOR=a.verilator, PYTHONDONTWRITEBYTECODE="1", TMPDIR=str(packet/"scratch"))

def run(task):
    work = packet/"scratch"/task
    work.mkdir(parents=True, exist_ok=True)
    shape = 8 if task.endswith("-8") else 1
    variant = task.rsplit("-", 1)[0]
    cmd = [sys.executable, "tb/verilator/milan_dp/stream_counters.py", "--shape", str(shape), "--work", str(work)]
    local_env = dict(env)
    if variant == "frames-only":
        cmd += ["--output-condition", "frames-only"]
    elif variant == "makeflags":
        local_env["MAKEFLAGS"] = " -w"
    else:
        cmd += ["--variant", variant]
    with (packet/(task+".log")).open("w") as out:
        out.write("Command: "+repr(cmd)+"\n")
        out.flush()
        result = subprocess.run(cmd, cwd=root, env=local_env, stdout=out, stderr=subprocess.STDOUT)
    (packet/(task+".rc")).write_text(str(result.returncode)+"\n")
    for name in ("build.log", "run.log", "escape.log"):
        if (work/name).exists():
            (packet/(task+"-"+name)).write_bytes((work/name).read_bytes())
    print(task, "rc", result.returncode, flush=True)
    return result.returncode

with ThreadPoolExecutor(max_workers=a.jobs) as pool:
    results = list(pool.map(run, a.tasks))
sys.exit(bool(any(results)))
