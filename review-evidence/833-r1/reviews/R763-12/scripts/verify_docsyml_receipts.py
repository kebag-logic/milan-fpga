#!/usr/bin/env python3
"""Independently check the author's docs.yml receipts against the workflow at the reviewed head.

usage: verify_docsyml_receipts.py <repo> <head> <logs dir> <not_run.json>
Every `run:` step must have <job>__<id>.rc == 0 with the head in the log's first line,
or a stated not-run reason. Prints a count and every non-conforming step.
"""
import json, subprocess, sys
from pathlib import Path
import yaml
repo, head, logs, nr = sys.argv[1:5]
logs = Path(logs)
NOT_RUN = json.loads(Path(nr).read_text())
wf = yaml.safe_load(subprocess.run(["git", "-C", repo, "show", f"{head}:.github/workflows/docs.yml"],
                                   check=True, capture_output=True, text=True).stdout)
ran = skipped = bad = 0
used = set()
for job, body in wf["jobs"].items():
    for n, step in enumerate(body.get("steps", [])):
        if "run" not in step:
            continue
        sid = step.get("id") or f"step{n}"
        key = f"{job}/{sid}"
        reason = NOT_RUN.get(key) or NOT_RUN.get(sid)
        if reason:
            used.add(key if key in NOT_RUN else sid)
            skipped += 1
            print(f"NOTRUN {key}: {reason}")
            continue
        rc = logs / f"{job}__{sid}.rc"
        lg = logs / f"{job}__{sid}.log"
        if not rc.exists() or not lg.exists():
            bad += 1; print(f"MISSING {key}"); continue
        first = lg.read_text(errors="replace").splitlines()[:1]
        if rc.read_text().strip() != "0" or not first or head not in first[0]:
            bad += 1; print(f"BAD {key} rc={rc.read_text().strip()} first={first}")
        else:
            ran += 1
print(f"ran={ran} notrun={skipped} bad={bad} unused_notrun_keys={sorted(set(NOT_RUN) - used)}")
sys.exit(1 if bad else 0)
