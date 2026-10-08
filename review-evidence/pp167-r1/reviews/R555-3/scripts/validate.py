#!/usr/bin/env python3
"""Run the documentation gate, notification unit suite and two focused controls."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import datetime
import json
import os
from pathlib import Path
import shutil
import subprocess

p = argparse.ArgumentParser(description=__doc__)
p.add_argument("repo", type=Path)
a = p.parse_args()
repo = a.repo.resolve()
packet = Path(__file__).resolve().parents[1]
scratch = packet / "scratch"
receipts = packet / "receipts"
env = os.environ.copy()
env["TMPDIR"] = str(scratch)
env["PYTHONDONTWRITEBYTECODE"] = "1"
env["PATH"] = str(scratch / "venv/bin") + os.pathsep + env["PATH"]
env["MAKEFLAGS"] = "-j16"
wrapper = packet / "scripts/limited_verilator.py"
wrapper.chmod(0o755)
unit = scratch / "unit"
if unit.exists():
    shutil.rmtree(unit)
for directory in ("hdl", "tb/common", "tb/aecp_notify"):
    shutil.copytree(repo / directory, unit / directory,
                    ignore=shutil.ignore_patterns("obj*", "__pycache__"))
def run(name, command, cwd):
    start = datetime.datetime.now(datetime.timezone.utc).isoformat()
    with (receipts / (name + ".log")).open("w") as f:
        proc = subprocess.run(command, cwd=cwd, env=env, stdout=f,
                              stderr=subprocess.STDOUT, timeout=540)
    (receipts / (name + ".rc")).write_text(str(proc.returncode) + "\n")
    record = {"command": command, "cwd": str(cwd), "started": start,
              "finished": datetime.datetime.now(datetime.timezone.utc).isoformat(),
              "rc": proc.returncode, "compiler_workers_per_build": 4}
    (receipts / (name + ".json")).write_text(json.dumps(record, indent=2) + "\n")
    print(name, "rc", proc.returncode, flush=True)
    return proc.returncode
jobs = [
    ("make-check", ["make", "-j16", "check"], repo),
    ("notify-suite", ["make", "-j16", "VERILATOR=" + str(wrapper)], unit / "tb/aecp_notify"),
    ("focused-controls", ["python3", str(repo / "tb/pp_top/notify_mutants.py"),
        "--output", str(receipts / "focused-controls"), "--jobs", "2",
        "--verilator", str(wrapper), "--only", "cancel_collision_drops_command",
        "cancel_pending_accepts_failure"], repo),
]
# All child commands are synchronous. The foreground driver waits for every
# independent task; there are no detached or shell-background jobs.
with ThreadPoolExecutor(max_workers=3) as pool:
    results = list(pool.map(lambda job: run(*job), jobs))
raise SystemExit(any(results))
