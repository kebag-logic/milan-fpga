#!/usr/bin/env python3
"""Read exact-head hosted state; never starts jobs or changes public metadata."""
import datetime
import json
import subprocess
from pathlib import Path

packet = Path(__file__).resolve().parent
head = "12f00129349c889e6dbbb7de11529ab38c9d164d"
repo = "repos/kebag-logic/milan-fpga"
raw = subprocess.check_output(["gh", "api", f"{repo}/commits/{head}/check-runs?per_page=100"])
(packet / "hosted-checks-final.json").write_bytes(raw)
checks = json.loads(raw)["check_runs"]
assert all(item["head_sha"] == head for item in checks)
summary = {
    "observed_at": datetime.datetime.now(datetime.UTC).isoformat(),
    "head": head,
    "checks": [{key: item.get(key) for key in
                ("name", "status", "conclusion", "id", "html_url", "started_at", "completed_at")}
               for item in checks],
}
(packet / "hosted-summary.json").write_text(json.dumps(summary, indent=2) + "\n")
for item in summary["checks"]:
    print(item["name"], item["status"], item["conclusion"])
