#!/usr/bin/env python3
"""Run the docs workflow's gate steps from the tree's own workflow file in one checkout.

Usage: python3 -I run_gates.py TREE OUTDIR BASE_SHA [skip-id ...]
Each step's run block is executed with bash -e in TREE; stdout+stderr go to
OUTDIR/<id>.log and the exit status to OUTDIR/<id>.rc (TIMEOUT after STEP_TIMEOUT seconds, default 420); a summary goes to
OUTDIR/summary.txt. The em-dash gate (gate_8) is run as its final command
against BASE_SHA, since there is no event payload outside the hosted runner.
"""
import os
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor

import yaml

tree, out, base = sys.argv[1], sys.argv[2], sys.argv[3]
skip = set(sys.argv[4:])
STEP_TIMEOUT = int(os.environ.get("STEP_TIMEOUT", "420"))
os.makedirs(out, exist_ok=True)
wf = yaml.safe_load(open(os.path.join(tree, ".github/workflows/docs.yml")))
steps = []
for job in ("docs-gates-0", "docs-gates-2"):
    for s in wf["jobs"][job]["steps"]:
        sid = s.get("id") or ""
        if sid.startswith("gate_") and "run" in s and sid not in skip:
            run = s["run"]
            if sid == "gate_8":
                run = f"python3 scripts/check_em_dash.py --base {base}"
            steps.append((sid, s.get("name"), run))


def one(step):
    sid, name, run = step
    with tempfile.TemporaryDirectory() as rt:
        env = dict(os.environ, RUNNER_TEMP=rt, GITHUB_WORKSPACE=tree)
        with open(os.path.join(out, sid + ".log"), "w") as log:
            start = time.monotonic()
            try:
                rc = subprocess.run(["bash", "-e", "-c", run], cwd=tree, env=env, stdout=log,
                                    stderr=subprocess.STDOUT, timeout=STEP_TIMEOUT).returncode
            except subprocess.TimeoutExpired:
                rc = "TIMEOUT"
            log.write(f"\n[runner] rc={rc} seconds={time.monotonic() - start:.1f}\n")
    open(os.path.join(out, sid + ".rc"), "w").write(f"{rc}\n")
    return sid, name, rc


with ThreadPoolExecutor(max_workers=8) as pool:
    results = list(pool.map(one, steps))
with open(os.path.join(out, "summary.txt"), "w") as summary:
    for sid, name, rc in results:
        summary.write(f"{rc}\t{sid}\t{name}\n")
print(open(os.path.join(out, "summary.txt")).read())
