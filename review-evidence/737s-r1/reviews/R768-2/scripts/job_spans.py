#!/usr/bin/env python3
"""Print each job's start, end and span in seconds from the first job start, and its queue wait.

Usage: python3 -I job_spans.py <jobs-api.json>   (GET /repos/{o}/{r}/actions/runs/{id}/jobs)
"""
import json
import sys
from datetime import datetime


def t(stamp):
    return datetime.fromisoformat(stamp.replace("Z", "+00:00")).timestamp()


jobs = json.load(open(sys.argv[1]))["jobs"]
first = min(t(job["started_at"]) for job in jobs if job["started_at"])
for job in sorted(jobs, key=lambda job: job["started_at"] or ""):
    if not job["completed_at"]:
        print(f"{job['name']:28} {job['status']}")
        continue
    start, end = t(job["started_at"]), t(job["completed_at"])
    print(f"{job['name']:28} queued {start - t(job['created_at']):5.0f} start+{start - first:6.0f} "
          f"end+{end - first:6.0f} span {end - start:5.0f} {job['conclusion']}")
