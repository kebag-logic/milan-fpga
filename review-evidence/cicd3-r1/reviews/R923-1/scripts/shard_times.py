#!/usr/bin/env python3
"""Compare hosted job and suite-step minutes between two rtl-full runs.

usage: shard_times.py BASE_JOBS.json HEAD_JOBS.json

Each file is the Actions API jobs listing of one run. For every job present
in either run: whole-job minutes and, for Verilator workers, the minutes of
the "Run this exhaustive suite shard" step.
"""

import datetime
import json
import sys


def minutes(a, b):
    """Minutes between two ISO timestamps, or None."""
    if not a or not b:
        return None
    t = lambda x: datetime.datetime.fromisoformat(x.replace("Z", "+00:00"))
    return round((t(b) - t(a)).total_seconds() / 60, 1)


def table(path):
    """job name -> (conclusion, job minutes, suite-step minutes)."""
    rows = {}
    for job in json.load(open(path))["jobs"]:
        step = [s for s in job["steps"] if s["name"] == "Run this exhaustive suite shard"]
        rows[job["name"]] = (job["conclusion"], minutes(job["started_at"], job["completed_at"]),
                             minutes(step[0]["started_at"], step[0]["completed_at"]) if step else None)
    return rows


def main() -> int:
    base, head = table(sys.argv[1]), table(sys.argv[2])
    print(f"{'job':<40} {'base':>18} {'head':>18}")
    for name in sorted(set(base) | set(head)):
        b, h = base.get(name, ("-", None, None)), head.get(name, ("-", None, None))
        print(f"{name:<40} {str(b[0]):>8} {str(b[1]):>5}/{str(b[2]):>5} {str(h[0]):>8} {str(h[1]):>5}/{str(h[2]):>5}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
