#!/usr/bin/env python3
"""Fail unless every `run:` step of a workflow at this head has an rc of 0 or a stated reason.

usage: verify_wf.py <workflow name> <head sha> <scratch root>
The rows come from the workflow at the head, so a step left out of a table is a red here.
"""
import json, subprocess, sys
from pathlib import Path
import yaml
wf_name, head, root = sys.argv[1:4]
root = Path(root); logs = root / "logs"
NOT_RUN = json.loads(Path(__file__).with_name(f"not_run_{wf_name}.json").read_text())
text = subprocess.run(["git", "-C", "<data>/lanes/665-s8-wire-timing", "show", f"{head}:.github/workflows/{wf_name}.yml"],
                      check=True, capture_output=True, text=True).stdout
wf = yaml.safe_load(text)
bad = 0; ran = 0; skipped = 0
print(f"| Job | Step | Name | rc | Log |\n|---|---|---|---:|---|")
for job, body in wf["jobs"].items():
    for n, step in enumerate(body["steps"]):
        if "run" not in step:
            continue
        sid = step.get("id") or f"step{n}"
        tag = f"{wf_name}__{job}__{sid}"
        reason = NOT_RUN.get(f"{job}/{sid}") or NOT_RUN.get(f"{job}/*") or NOT_RUN.get(sid)
        rc_file = logs / f"{tag}.rc"
        name = (step.get("name") or "").replace("|", "/")
        if reason:
            skipped += 1
            print(f"| {job} | {sid} | {name} | NOT RUN | {reason} |")
        elif not rc_file.exists():
            bad += 1
            print(f"| {job} | {sid} | {name} | MISSING | |")
        else:
            rc = rc_file.read_text().strip()
            first = (logs / f"{tag}.log").read_text(errors="replace").splitlines()[0]
            ok = rc == "0" and head in first
            bad += not ok
            ran += 1
            print(f"| {job} | {sid} | {name} | {rc if ok else 'BAD ' + rc} | `{tag}.log` |")
print(f"\n{ran} steps ran, {skipped} not run with a reason, {bad} bad")
sys.exit(1 if bad else 0)
