#!/usr/bin/env python3
"""Read exact-head hosted status and public review artifacts; never write to the remote."""
import concurrent.futures
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys

packet = Path(sys.argv[1]).resolve()
head = "bc89f84e6757f8fcddf21958e99f40f17bc0ee1e"
prefix = "repos/kebag-logic/milan-fpga/"

def read(endpoint):
    return json.loads(subprocess.check_output(["gh", "api", prefix + endpoint]))

endpoints = {
    "checks": f"commits/{head}/check-runs?per_page=100",
    "runs": f"actions/runs?head_sha={head}&per_page=100",
    "comments": "issues/702/comments?per_page=100",
    "reviews": "pulls/702/reviews?per_page=100",
    "review-comments": "pulls/702/comments?per_page=100",
}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    data = dict(zip(endpoints, pool.map(read, endpoints.values())))
for name, value in data.items():
    (packet / "receipts" / ("final-hosted-" + name + ".json")).write_text(json.dumps(value, indent=2) + "\n")
assert all(run["head_sha"] == head for run in data["runs"]["workflow_runs"])
assert all(run["head_sha"] == head for run in data["checks"]["check_runs"])
assert all(len(data[name]) < 100 for name in ("comments", "reviews", "review-comments"))
assert data["checks"]["total_count"] < 100 and data["runs"]["total_count"] < 100
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    jobs = list(pool.map(read, [f'actions/runs/{run["id"]}/jobs?per_page=100' for run in data["runs"]["workflow_runs"]]))
summary = {"observed_utc": datetime.now(timezone.utc).isoformat(), "head": head, "jobs": []}
for run, result in zip(data["runs"]["workflow_runs"], jobs):
    assert result["total_count"] < 100
    (packet / "receipts" / f'final-hosted-jobs-{run["id"]}.json').write_text(json.dumps(result, indent=2) + "\n")
    for job in result["jobs"]:
        summary["jobs"].append({"workflow": run["name"], "name": job["name"],
                                "status": job["status"], "conclusion": job["conclusion"],
                                "successful_steps": sum(step["conclusion"] == "success" for step in job.get("steps", [])),
                                "url": job["html_url"]})
summary["review_audit"] = {
    "conversation_count": len(data["comments"]), "reviews_count": len(data["reviews"]),
    "inline_review_comments_count": len(data["review-comments"]),
    "conversation_ids": [comment["id"] for comment in data["comments"]],
}
(packet / "receipts/public-state-final.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps(summary, indent=2))
