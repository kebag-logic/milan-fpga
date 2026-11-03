#!/usr/bin/env python3
"""Per-job span, queue, Verilator build, gate-step and setup seconds for one hosted run.

Usage: python3 -I run_timing.py JOBS_JSON [JOBS_JSON ...]
JOBS_JSON is the saved output of `gh api repos/OWNER/REPO/actions/runs/RUN/jobs?per_page=100`
(optionally /attempts/N/jobs). Setup is the job span less its gate steps
("Elaboration gates, leg ..." and "Standalone LiteX simulation aggregate, leg ...")
and less "Build Verilator from source on cache miss", the definition the
elaboration projection documentation uses. Offsets are from the first job start.
"""
import datetime
import json
import sys


def ts(value):
    return datetime.datetime.fromisoformat(value.replace("Z", "+00:00")) if value else None


def secs(start, end):
    return round((ts(end) - ts(start)).total_seconds()) if start and end else None


def main(paths):
    for path in paths:
        jobs = json.load(open(path))["jobs"]
        first = min(ts(job["started_at"]) for job in jobs if job["started_at"])
        print("== " + path)
        for job in sorted(jobs, key=lambda job: job["name"]):
            span = secs(job["started_at"], job["completed_at"])
            queue = secs(job["created_at"], job["started_at"])
            end = round((ts(job["completed_at"]) - first).total_seconds()) if job["completed_at"] else None
            gates = build = 0
            named = []
            for step in job.get("steps", []):
                took = secs(step["started_at"], step["completed_at"]) or 0
                if step["name"].startswith(("Elaboration gates, leg", "Standalone LiteX simulation aggregate, leg")):
                    gates += took
                    named.append(step["name"] + " " + str(took))
                elif step["name"] == "Build Verilator from source on cache miss":
                    build += took
            setup = span - gates - build if span is not None and named else None
            print(f"  {job['name']:<28} {str(job['conclusion']):<9} queue {queue} span {span} end+{end} "
                  f"gates {gates} verilator-build {build} setup {setup} | " + " | ".join(named))


if __name__ == "__main__":
    main(sys.argv[1:])
