#!/usr/bin/env python3
"""Verify a run_wf.py replay: every `run:` step of every job a pull_request to dev triggers, in the four workflow
files of <clone>, has an rc file holding 0 under <logs>, or a not_run.json entry and its reason. Matrix jobs are
expanded from their matrix (shard x total). Prints one line per step and a summary; exit 1 on any step with
neither, or with a non-zero rc, or on a job whose tree was not clean after it.

usage: verify_wf.py <clone> <logs> [workflow,...]   (default: all four; a list re-verifies a partial re-run)
"""
import fnmatch
import itertools
import json
import sys
from pathlib import Path

import yaml

clone, logs = Path(sys.argv[1]), Path(sys.argv[2])
NOT_RUN = json.loads(Path(__file__).with_name("not_run.json").read_text())
ran = notrun = bad = 0
lines = []
SELECTED = sys.argv[3].split(",") if len(sys.argv) > 3 else ["rtl-fast", "rtl", "docs", "elaborate"]
for wfname in SELECTED:
    wf = yaml.safe_load((clone / ".github/workflows" / f"{wfname}.yml").read_text())
    on = wf.get(True) if True in wf else wf.get("on")
    if "pull_request" not in on:
        lines.append(f"{wfname}: no pull_request trigger")
        continue
    for job, jd in wf["jobs"].items():
        mx = (jd.get("strategy") or {}).get("matrix") or {}
        keys = sorted(k for k in mx if k not in ("include", "exclude"))
        combos = [dict(zip(keys, vals)) for vals in itertools.product(*(mx[k] for k in keys))] if keys else [{}]
        for combo in combos:
            tag0 = f"{wfname}__{job}" + "".join(f"__{k}{v}" for k, v in sorted(combo.items()))
            job_ran = False
            for n, step in enumerate(jd.get("steps", [])):
                if "run" not in step:
                    continue
                sid = step.get("id") or f"step{n}"
                key = f"{wfname}/{job}/{sid}"
                hit = [p for p in NOT_RUN if fnmatch.fnmatchcase(key, p)]
                rc_file = logs / f"{tag0}__{sid}.rc"
                if hit:
                    notrun += 1
                    lines.append(f"NOT RUN\t{tag0}__{sid}\t{NOT_RUN[hit[0]]}")
                elif rc_file.exists() and rc_file.read_text().strip() == "0":
                    ran += 1
                    job_ran = True
                    lines.append(f"rc 0\t{tag0}__{sid}")
                else:
                    bad += 1
                    got = rc_file.read_text().strip() if rc_file.exists() else "missing"
                    lines.append(f"BAD rc={got}\t{tag0}__{sid}")
            tree = logs / f"{tag0}__tree-after.txt"
            if job_ran:
                status = tree.read_text().split("status:\n", 1)[-1].strip() if tree.exists() else "missing"
                if status and not status.startswith("(no .git"):
                    bad += 1
                    lines.append(f"BAD tree\t{tag0}: {status[:200]}")
print("\n".join(lines))
print(f"{ran} steps ran rc 0, {notrun} not run with a reason, {bad} bad")
sys.exit(1 if bad else 0)
