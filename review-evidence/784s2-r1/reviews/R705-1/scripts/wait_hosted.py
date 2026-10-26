#!/usr/bin/env python3
"""Read-only: poll the hosted workflow runs of one head until all complete or a time budget ends.
Usage: wait_hosted.py <head-sha> <budget-seconds>
Prints each run's status and conclusion at the end; exit 0 when all runs completed, 3 otherwise.
"""
import json
import subprocess
import sys
import time

head, budget = sys.argv[1], int(sys.argv[2])
deadline = time.monotonic() + budget
while True:
    raw = subprocess.run(["gh", "api", f"repos/kebag-logic/milan-fpga/actions/runs?head_sha={head}&per_page=50"],
                         capture_output=True, text=True, check=True).stdout
    runs = json.loads(raw)["workflow_runs"]
    done = all(r["status"] == "completed" for r in runs)
    if done or time.monotonic() >= deadline:
        break
    time.sleep(60)
for r in runs:
    print(r["id"], r["name"], r["status"], r["conclusion"], sep="\t")
sys.exit(0 if done else 3)
