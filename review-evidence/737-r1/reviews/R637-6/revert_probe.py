#!/usr/bin/env python3
"""Exercise the committed gate, revert its generator, and restore exact bytes."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

p = argparse.ArgumentParser()
p.add_argument("repo", type=Path)
p.add_argument("packet", type=Path)
a = p.parse_args()
repo, packet = a.repo.resolve(), a.packet.resolve()
env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", TMPDIR=str(packet / "scratch"))
paths = [repo / "scripts/ci_suite_workflows.py", *sorted((repo / ".github/workflows").glob("*.yml"))]
saved = {f: (f.read_bytes(), f.stat().st_mode) for f in paths}
results = []

def run(label, args, expected):
    start = time.monotonic()
    log = packet / "receipts" / (label + ".log")
    with log.open("wb") as stream:
        r = subprocess.run([sys.executable, *args], cwd=repo, env=env,
                           stdout=stream, stderr=subprocess.STDOUT, timeout=540)
    results.append(dict(label=label, command=["python3", *args], rc=r.returncode,
                        seconds=round(time.monotonic()-start, 3), expected=expected,
                        log=str(log.relative_to(packet)),
                        log_sha256=hashlib.sha256(log.read_bytes()).hexdigest()))
    print(label, r.returncode, flush=True)
    assert (r.returncode == 0) if expected == 0 else (r.returncode != 0), label

try:
    run("pristine-gate-selftest", ["scripts/ci_gate_workflows_selftest.py"], 0)
    paths[0].write_bytes(subprocess.check_output(
        ["git", "show", "08adb21a:scripts/ci_suite_workflows.py"], cwd=repo))
    run("reverted-regenerate", ["scripts/ci_gate_workflows.py"], 0)
    run("reverted-freshness", ["scripts/ci_gate_workflows.py", "--check"], 0)
    run("reverted-contract", ["scripts/ci_events.py", "--check"], 0)
    run("reverted-gate-selftest", ["scripts/ci_gate_workflows_selftest.py"], "nonzero")
finally:
    for f, (data, mode) in saved.items():
        f.write_bytes(data)
        f.chmod(mode)
    (packet / "receipts/revert-probe.json").write_text(json.dumps(results, indent=2)+"\n")
    assert all(f.read_bytes() == data and f.stat().st_mode == mode
               for f, (data, mode) in saved.items())
run("restored-freshness", ["scripts/ci_gate_workflows.py", "--check"], 0)
(packet / "receipts/revert-probe.json").write_text(json.dumps(results, indent=2)+"\n")
