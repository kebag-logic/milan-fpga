#!/usr/bin/env python3
"""Record exact-head hosted jobs and steps, preserving skipped conclusions."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess

packet = Path(__file__).resolve().parents[1]
repo = "Mister-M-alt/protocol-processor-control-plane-avb-milan"
head = "bcbf382e5f4d17ccfd8ae75a80bbc45902c75b7d"
def api(path):
    return json.loads(subprocess.check_output(["gh", "api", f"repos/{repo}/{path}"]))
runs = api(f"actions/runs?head_sha={head}&per_page=100")["workflow_runs"]
def snapshot(run):
    assert run["head_sha"] == head
    jobs = api(f"actions/runs/{run['id']}/jobs?per_page=100")["jobs"]
    return {"id": run["id"], "head_sha": run["head_sha"], "event": run["event"],
        "status": run["status"], "conclusion": run["conclusion"], "url": run["html_url"],
        "jobs": [{k: j[k] for k in ("id", "name", "status", "conclusion", "started_at",
                                   "completed_at", "steps", "html_url")} for j in jobs]}
with ThreadPoolExecutor(max_workers=2) as pool:
    records = list(pool.map(snapshot, runs))
out = {"observed_at": datetime.now(timezone.utc).isoformat(), "head": head, "runs": records}
(packet / "receipts/hosted-jobs-steps.json").write_text(json.dumps(out, indent=2) + "\n")
for r in records:
    print(r["id"], r["event"], r["status"], r["conclusion"])
    for j in r["jobs"]:
        print(" ", j["name"], j["status"], j["conclusion"])
        for s in j["steps"]:
            if s["conclusion"] != "success":
                print("   ", s["name"], s["status"], s["conclusion"])
