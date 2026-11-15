#!/usr/bin/env python3
"""Fail unless every `run:` step of rtl-fast, elaborate and rtl at this head has an rc of 0 or a stated reason.

docs.yml runs through the 829 docs runner, whose logs and table (verify_docs_yml.py) are its own.

usage: verify_wf_r5.py <head sha>[,<head sha>...] <scratch root> [<matrix totals as job=n> ...]
Round 5 (#871): a step may have run at any of the listed heads, each named in its log's first line, which
the table records; the workflows are read at the first head.
The rows come from the workflows at the head, so a step left out of a table is a red here. A matrix job's rows are
one per shard, `job.kofn`.
"""
import json, subprocess, sys
from pathlib import Path
import yaml
heads, root = sys.argv[1].split(","), sys.argv[2]
head = heads[0]
totals = dict(a.split("=") for a in sys.argv[3:])
root = Path(root); logs = root / "logs"
NOT_RUN = json.loads(Path("<scratch>/gates/tools/wf/not_run.json").read_text())
bad = ran = skipped = 0
print("| Workflow | Job | Step | Name | rc | Log or reason |\n|---|---|---|---|---:|---|")
for wfname in ("rtl-fast", "elaborate", "rtl"):
    text = subprocess.run(["git", "-C", "<lane>", "show", f"{head}:.github/workflows/{wfname}.yml"],
                          check=True, capture_output=True, text=True).stdout
    wf = yaml.safe_load(text)
    for job, body in wf["jobs"].items():
        n_shards = int(totals.get(f"{wfname}/{job}", 0))
        variants = [f"{wfname}.{job}.{k}of{n_shards}" for k in range(n_shards)] if n_shards else [f"{wfname}.{job}"]
        for n, step in enumerate(body["steps"]):
            if "run" not in step:
                continue
            sid = step.get("id") or f"step{n}"
            name = (step.get("name") or "").replace("|", "/")
            reason = (NOT_RUN.get(f"{wfname}/{job}/{sid}") or NOT_RUN.get(f"{wfname}/{sid}")
                      or NOT_RUN.get(f"{wfname}/{job}/*"))
            if reason:
                skipped += 1
                print(f"| {wfname} | {job} | {sid} | {name} | NOT RUN | {reason} |")
                continue
            for tag_job in variants:
                tag = f"{tag_job}__{sid}"
                rc_file = logs / f"{tag}.rc"
                if not rc_file.exists():
                    bad += 1
                    print(f"| {wfname} | {tag_job} | {sid} | {name} | MISSING | |")
                    continue
                rc = rc_file.read_text().strip()
                first = (logs / f"{tag}.log").read_text(errors="replace").splitlines()[0]
                at = next((h[:8] for h in heads if h in first), None)
                ok = rc == "0" and at is not None
                bad += not ok
                ran += 1
                print(f"| {wfname} | {tag_job} | {sid} | {name} | {rc if ok else 'BAD ' + rc} | `{tag}.log` at {at} |")
print(f"\n{ran} steps ran, {skipped} not run with a reason, {bad} bad")
sys.exit(1 if bad else 0)
