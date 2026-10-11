#!/usr/bin/env python3
"""Read exact-head workflow jobs, preserving executed versus skipped status."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess

p = argparse.ArgumentParser()
p.add_argument("--out", type=Path, required=True)
a = p.parse_args()
repo = "kebag-logic/milan-fpga"
head = "2bef9e50489a60f216a8073a9f5ea0645752b33f"
def api(path):
    return json.loads(subprocess.check_output(["gh", "api", "repos/" + repo + "/" + path]))
runs = api("actions/runs?head_sha=" + head + "&per_page=100")["workflow_runs"]
def jobs(run):
    assert run["head_sha"] == head
    result = []
    page = 1
    while True:
        batch = api(f"actions/runs/{run['id']}/jobs?per_page=100&page={page}")["jobs"]
        for job in batch:
            result.append({"workflow": run["name"], "run_id": run["id"],
                           "head": head, "job": job["name"], "url": job["html_url"],
                           "status": job["status"], "conclusion": job["conclusion"],
                           "steps": [{k: s.get(k) for k in ("name", "status", "conclusion")}
                                     for s in job.get("steps", [])]})
        if len(batch) < 100:
            return result
        page += 1
with ThreadPoolExecutor(max_workers=4) as pool:
    rows = [job for group in pool.map(jobs, runs) for job in group]
payload = {"observed_at": datetime.now(timezone.utc).isoformat(), "head": head, "jobs": rows}
a.out.write_text(json.dumps(payload, indent=2) + "\n")
for row in rows:
    ran = sum(s["conclusion"] == "success" for s in row["steps"])
    print(row["workflow"], row["job"], row["status"], row["conclusion"],
          f"successful_steps={ran}, total_steps={len(row['steps'])}", sep="\t")
