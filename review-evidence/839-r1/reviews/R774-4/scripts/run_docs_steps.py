#!/usr/bin/env python3
"""Run selected docs.yml run steps in a checkout, GitHub's default bash shell (-eo pipefail).

usage: run_docs_steps.py STEPS.jsonl WORKTREE OUTDIR job:index[,job:index...]
Writes OUTDIR/<job>_<index>.log and a summary line per step to stdout. Env for the em-dash step
is taken from the caller (EVENT_NAME, PUSH_BEFORE_SHA)."""
import json, os, subprocess, sys
steps = {(d["job"], d["i"]): d for d in map(json.loads, open(sys.argv[1], encoding="utf-8"))}
wt, out = sys.argv[2], sys.argv[3]
os.makedirs(out, exist_ok=True)
for key in sys.argv[4].split(","):
    job, i = key.split(":"); d = steps[(job, int(i))]
    log = os.path.join(out, f"{job}_{i}.log")
    with open(log, "w", encoding="utf-8") as fh:
        r = subprocess.run(["bash", "--noprofile", "--norc", "-eo", "pipefail", "-c", d["run"]],
                           cwd=wt, stdout=fh, stderr=subprocess.STDOUT)
    print(f"{job}:{i}\trc={r.returncode}\t{d['name']}", flush=True)
