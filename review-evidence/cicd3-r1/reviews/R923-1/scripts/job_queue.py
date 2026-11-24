#!/usr/bin/env python3
"""Print created/started/completed clock times of a run's Verilator jobs.

usage: job_queue.py JOBS.json
"""

import json
import sys


def clock(text):
    """HH:MM:SS of an ISO timestamp, or '-'."""
    return text[11:19] if text else "-"


def main() -> int:
    jobs = json.load(open(sys.argv[1]))["jobs"]
    for job in sorted(jobs, key=lambda j: j["started_at"] or "z"):
        if job["name"].startswith("Verilator") or job["name"] in ("full-ci-gate", "verilator-suites"):
            print(f"{job['name']:<24} created {clock(job['created_at'])} started {clock(job['started_at'])} "
                  f"completed {clock(job['completed_at'])} {job['conclusion']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
