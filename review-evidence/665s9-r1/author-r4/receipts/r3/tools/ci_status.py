#!/usr/bin/env python3
"""ci_status.py <head12>: the replay's finished jobs and any step with a non-zero rc."""
import json, sys
from pathlib import Path
root = Path("<scratch>/ci") / sys.argv[1] / "jobs"
done = bad = 0
for j in sorted(root.iterdir()):
    r = j / "result.json"
    if not r.exists():
        print("running/claimed:", j.name); continue
    d = json.loads(r.read_text()); done += 1
    fails = [(s["step"], s["rc"]) for s in d["steps"] if isinstance(s["rc"], int) and s["rc"] != 0]
    if d["result"] != "success" and d["result"] != "skipped" or fails:
        bad += 1; print("FAIL", j.name, d["result"], fails)
print(f"{done} finished, {bad} failed")
