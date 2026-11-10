#!/usr/bin/env python3
"""Fail unless every `run:` step of every job of the named workflows at this head has an rc of 0 or a stated reason.

usage: verify_wf.py <head sha> <scratch root> <workflow file name>... [--matrix job=key:v1,v2,...]
The rows come from the workflows at the head, so a step left out is a red here. A job run once per matrix value is
verified once per value given.
"""
import json, subprocess, sys
from pathlib import Path
import yaml
args = [a for a in sys.argv[1:] if not a.startswith('--matrix=')]
head, root, workflows = args[0], Path(args[1]), args[2:]
matrices = {}
for a in sys.argv[1:]:
    if a.startswith('--matrix='):
        job, spec = a.removeprefix('--matrix=').split('=', 1)
        key, values = spec.split(':', 1)
        matrices[job] = [(key, v) for v in values.split(',')]
logs = root / "logs"
NOT_RUN = json.loads(Path(__file__).with_name("not_run.json").read_text())
bad = ran = skipped = 0
print("| Workflow | Job | Step | Name | rc | Log or reason |\n|---|---|---|---|---:|---|")
for workflow in workflows:
    text = subprocess.run(["git", "-C", "$LANES/665-s15-32x32", "show", f"{head}:.github/workflows/{workflow}"],
                          check=True, capture_output=True, text=True).stdout
    wf = yaml.safe_load(text)
    w = workflow.removesuffix('.yml')
    for job, body in wf["jobs"].items():
        for key, value in matrices.get(job, [(None, None)]):
            mtag = f"-{value}" if key else ""
            for n, step in enumerate(body["steps"]):
                if "run" not in step:
                    continue
                sid = step.get("id") or f"step{n}"
                tag = f"{w}__{job}{mtag}__{sid}"
                reason = (NOT_RUN.get(f"{workflow}/{job}/{sid}") or NOT_RUN.get(f"{workflow}/{job}") or
                          NOT_RUN.get(f"{workflow}/{sid}") or NOT_RUN.get(sid))
                rc_file = logs / f"{tag}.rc"
                name = (step.get("name") or "").replace("|", "/")
                if reason:
                    skipped += 1
                    print(f"| {w} | {job}{mtag} | {sid} | {name} | NOT RUN | {reason} |")
                elif not rc_file.exists():
                    bad += 1
                    print(f"| {w} | {job}{mtag} | {sid} | {name} | MISSING | |")
                else:
                    rc = rc_file.read_text().strip()
                    first = (logs / f"{tag}.log").read_text(errors="replace").splitlines()[0]
                    ok = rc == "0" and head in first
                    bad += not ok
                    ran += 1
                    print(f"| {w} | {job}{mtag} | {sid} | {name} | {rc if ok else 'BAD ' + rc} | `{tag}.log` |")
print(f"\n{ran} steps ran, {skipped} not run with a reason, {bad} bad")
sys.exit(1 if bad else 0)
