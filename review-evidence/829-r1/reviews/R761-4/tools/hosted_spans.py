#!/usr/bin/env python3
"""Print hosted job spans and builder-leg step spans for named workflow runs."""
import datetime as d, json, subprocess, sys
REPO = "repos/kebag-logic/milan-fpga/actions/runs"
def p(s): return d.datetime.fromisoformat(s.replace("Z", "+00:00")) if s else None
def span(a, b): return int((p(b) - p(a)).total_seconds()) if a and b else None
for run in sys.argv[1:]:
    out = subprocess.run(["gh", "api", f"{REPO}/{run}/jobs?per_page=100"],
                         capture_output=True, text=True, check=True).stdout
    jobs = json.loads(out)["jobs"]
    print(f"run {run}")
    for job in jobs:
        if not job["name"].startswith(("docs-gates", "elaborate-gates", "Collect")):
            continue
        steps = {s["name"]: span(s["started_at"], s["completed_at"]) for s in job["steps"]
                 if "gates, leg" in s["name"] or "Standalone LiteX" in s["name"]}
        print(f"  {job['name']:20} {job['status']:11} {str(job['conclusion']):8} "
              f"{span(job['started_at'], job['completed_at'])} {steps}")
    starts = [j["started_at"] for j in jobs if j["started_at"]]
    ends = [j["completed_at"] for j in jobs if j["completed_at"] and j["name"] == "Collect CI manifest"]
    if starts and ends:
        print(f"  first job start to collector end: {span(min(starts), max(ends))} s")
