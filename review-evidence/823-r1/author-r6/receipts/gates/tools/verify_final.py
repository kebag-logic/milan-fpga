#!/usr/bin/env python3
"""Fail unless every `run:` step of the four workflows at the final head has an rc of 0 at that head, an rc of 0 at a
carried head with its reason, or a stated reason for not running.

usage: verify_final.py <final head> <final root> <carried head> <carried root> <carried.json> [job=n ...]
verify_wf.py's table, extended by one rule: a job named in carried.json (`workflow/job` -> reason) is read from the
carried root and must carry the carried head in each log's first line. The rows come from the workflows at the final
head, so a step left out of every table is a red here.
"""
import json, subprocess, sys
from pathlib import Path
import yaml
head, root, c_head, c_root, carried_path = sys.argv[1:6]
totals = dict(a.split("=") for a in sys.argv[6:])
CARRIED = json.loads(Path(carried_path).read_text())
NOT_RUN = json.loads(Path(__file__).with_name("not_run.json").read_text())
bad = ran = skipped = carried = 0
print("| Workflow | Job | Step | Name | rc | Head | Log or reason |\n|---|---|---|---|---:|---|---|")
for wfname in ("rtl-fast", "elaborate", "rtl", "docs"):
    text = subprocess.run(["git", "-C", "<lane>", "show", f"{head}:.github/workflows/{wfname}.yml"],
                          check=True, capture_output=True, text=True).stdout
    wf = yaml.safe_load(text)
    for job, body in wf["jobs"].items():
        n_shards = int(totals.get(f"{wfname}/{job}", 0))
        variants = [f"{wfname}.{job}.{k}of{n_shards}" for k in range(n_shards)] if n_shards else [f"{wfname}.{job}"]
        why = CARRIED.get(f"{wfname}/{job}")
        logs, want = (Path(c_root) / "logs", c_head) if why else (Path(root) / "logs", head)
        for n, step in enumerate(body["steps"]):
            if "run" not in step:
                continue
            sid = step.get("id") or f"step{n}"
            name = (step.get("name") or "").replace("|", "/")
            reason = (NOT_RUN.get(f"{wfname}/{job}/{sid}") or NOT_RUN.get(f"{wfname}/{sid}")
                      or NOT_RUN.get(f"{wfname}/{job}/*"))
            if reason:
                skipped += 1
                print(f"| {wfname} | {job} | {sid} | {name} | NOT RUN | | {reason} |")
                continue
            for tag_job in variants:
                tag = f"{tag_job}__{sid}"
                rc_file = logs / f"{tag}.rc"
                if not rc_file.exists():
                    bad += 1
                    print(f"| {wfname} | {tag_job} | {sid} | {name} | MISSING | {want[:8]} | |")
                    continue
                rc = rc_file.read_text().strip()
                first = (logs / f"{tag}.log").read_text(errors="replace").splitlines()[0]
                ok = rc == "0" and want in first
                bad += not ok
                ran += 1
                carried += bool(why)
                note = f"`{tag}.log`" + (f"; carried: {why}" if why else "")
                print(f"| {wfname} | {tag_job} | {sid} | {name} | {rc if ok else 'BAD ' + rc} | {want[:8]} | {note} |")
print(f"\n{ran} steps ran ({ran - carried} at {head[:8]}, {carried} carried from {c_head[:8]}), "
      f"{skipped} not run with a reason, {bad} bad")
sys.exit(1 if bad else 0)
