#!/usr/bin/env python3
"""Run bounded source-head checks, retaining commands, logs and exits.

Usage: focused_checks.py REPO PACKET SIMULATOR [build|run|controller|mutants]
Builds and simulations are foreground children; independent work uses a
bounded pool. Disposable outputs remain in PACKET/scratch.
"""
import concurrent.futures as cf
import json
import os
from pathlib import Path
import subprocess
import sys
import time

repo, packet, sim = map(lambda s: Path(s).resolve(), sys.argv[1:4])
stage = sys.argv[4]
scratch = packet / "scratch"
receipts = packet / "receipts"
scratch.mkdir(parents=True, exist_ok=True)
receipts.mkdir(parents=True, exist_ok=True)
env = dict(os.environ, VERILATOR=str(sim), PYTHONDONTWRITEBYTECODE="1")
env["PATH"] = str(sim.parent) + os.pathsep + env["PATH"]

def run(name, argv, cwd=repo):
    record = {"argv": argv, "cwd": str(cwd.relative_to(repo)) if cwd.is_relative_to(repo) else "scratch"}
    # Commands in receipts use relocatable placeholders.
    display = json.dumps(record, indent=2).replace(str(repo), "<repo>").replace(str(packet), "<packet>").replace(str(sim), "<simulator>")
    (receipts / (name + ".command.json")).write_text(display + "\n")
    start = time.monotonic()
    with (scratch / (name + ".raw.log")).open("w") as log:
        result = subprocess.run(argv, cwd=cwd, env=env, stdout=log, stderr=subprocess.STDOUT, check=False)
    raw = (scratch / (name + ".raw.log")).read_text(errors="replace")
    raw = raw.replace(str(repo), "<repo>").replace(str(packet), "<packet>").replace(str(sim), "<simulator>")
    (receipts / (name + ".log")).write_text(raw)
    (receipts / (name + ".rc")).write_text(str(result.returncode) + "\n")
    print(f"{name}: rc={result.returncode}, elapsed={time.monotonic()-start:.2f}s", flush=True)
    return result.returncode

if stage == "build":
    tasks = [
        ("chmap-build", ["make", "-j16", "-C", "tb/verilator/chmap_capture", "build", "VERILATOR_JOBS=8", f"VERILATOR={sim}", f"MDIR={scratch / 'chmap'}"]),
        ("fine-build", ["make", "-j16", "-C", "tb/verilator/follow_ring", "build", "VERILATOR_JOBS=8", f"VERILATOR={sim}", "CLK_HZ=25000000", "FRAME_DIV=64", f"MDIR={scratch / 'fine'}"]),
    ]
    with cf.ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda task: run(*task), tasks))
elif stage == "run":
    tasks = [
        ("chmap-run", [str(scratch / "chmap/Vchmap_wrap")]),
        ("fine-pulls", ["python3", "tb/verilator/follow_ring/small_pulls.py", "--exe", str(scratch / "fine/Vfollow_ring"), "--out", str(scratch / "fine-results"), "--jobs", "8"]),
    ]
    with cf.ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda task: run(*task), tasks))
elif stage == "controller":
    results = [run("settle-control", ["python3", "tb/verilator/follow_ring/settle_control.py", "--sim", str(sim), "--out", str(scratch / "controller"), "--jobs", "1"])]
elif stage == "mutants":
    results = [run("capture-mutants", ["python3", "tb/verilator/follow_ring/mutants.py", "--mdir", str(scratch / "mutants"), "--jobs", "1", "--select", "SINGLE-DROP", "HELD-DUP", "STARVED-HELD-DUP"])]
else:
    raise SystemExit("unknown stage")
raise SystemExit(int(any(results)))
