#!/usr/bin/env python3
"""Run two focused negative-control campaigns concurrently in scratch copies."""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import time

packet = Path(__file__).resolve().parents[1]
tree = packet / "scratch/planting-head"
wrapper = packet / "scripts/limited_verilator.py"
wrapper.chmod(0o755)
env = dict(os.environ, MAKEFLAGS="-j16", TMPDIR=str(packet / "scratch"), PYTHONDONTWRITEBYTECODE="1")
cases = [
    ("originator-controls", "notify_mutants.py", 2, ["inflight_highest_free_id", "inflight_match_ignores_seq", "inflight_cancel_keeps_timer", "inflight_shared_seq"]),
    ("validator-control", "d3_mutants.py", 1, ["validator_admits_held_aecp"]),
]

def run(case):
    name, driver, jobs, arms = case
    output = packet / "receipts" / name
    output.mkdir(parents=True, exist_ok=True)
    command = ["python3", "-B", str(tree / "tb/pp_top" / driver), "--output", str(output), "--verilator", str(wrapper), "--jobs", str(jobs), "--only", *arms]
    start = time.monotonic()
    with (output / "campaign.log").open("w") as log:
        p = subprocess.run(command, cwd=tree, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=540)
    (output / "campaign.rc").write_text(str(p.returncode) + "\n")
    assert p.returncode == 0, name
    records = json.loads((output / "results.json").read_text())
    assert sum(r["verdict"] == "KILLED" for r in records) == len(arms)
    assert all(r["verdict"] in ["PASS", "KILLED"] for r in records)
    return {"name": name, "command": command, "rc": p.returncode, "seconds": round(time.monotonic()-start,3), "killed": len(arms), "goldens": sum(r["verdict"] == "PASS" for r in records)}

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    results = list(pool.map(run, cases))
(packet / "receipts/campaign-summary.json").write_text(json.dumps(results, indent=2) + "\n")
print(json.dumps(results, indent=2))
