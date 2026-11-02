#!/usr/bin/env python3
"""Fail unless every rtl-fast step that reads scripts/ or docs/ at this head has an rc of 0 or a stated reason.

usage: verify_rtl_fast.py <head sha> <clean clone at that head> <scratch root>
"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from select_rtl_fast import selected
head, tree, root = sys.argv[1:4]
logs = Path(root) / "logs"
NOT_RUN = json.loads(Path(__file__).with_name("rtl_fast_not_run.json").read_text())
bad = ran = skipped = 0
print("| Job | Step | Name | Reads | rc | Log |\n|---|---|---|---|---:|---|")
for job, sid, name, how in selected(Path(tree)):
    tag = f"{job}__{sid}"
    reason = NOT_RUN.get(f"{job}/{sid}") or NOT_RUN.get(sid)
    rc_file = logs / f"{tag}.rc"
    if reason:
        skipped += 1
        print(f"| {job} | {sid} | {name} | {how} | NOT RUN | {reason} |")
    elif not rc_file.exists():
        bad += 1
        print(f"| {job} | {sid} | {name} | {how} | MISSING | |")
    else:
        rc = rc_file.read_text().strip()
        ok = rc == "0" and head in (logs / f"{tag}.log").read_text(errors="replace").splitlines()[0]
        bad += not ok
        ran += 1
        print(f"| {job} | {sid} | {name} | {how} | {rc if ok else 'BAD ' + rc} | `{tag}.log` |")
print(f"\n{ran} steps ran, {skipped} not run with a reason, {bad} bad")
sys.exit(1 if bad else 0)
