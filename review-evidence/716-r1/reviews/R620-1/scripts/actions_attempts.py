#!/usr/bin/env python3
"""Recompute firmware job wall-clock times for every attempt of one rtl-fast run.

Usage: python3 -I actions_attempts.py RUN_ID ATTEMPTS OUT_JSON
Reads the public Actions API through `gh api` (read-only) and prints a table.
"""
import json
import subprocess
import sys
from datetime import datetime

REPO = "kebag-logic/milan-fpga"
FIRMWARE = ("firmware-unit", "firmware-control-mutants", "firmware-aecp-mutants", "firmware-srp-mutants")


def api(path):
    out = subprocess.run(["gh", "api", path], check=True, capture_output=True, text=True).stdout
    return json.loads(out)


def ts(text):
    return datetime.fromisoformat(text.replace("Z", "+00:00"))


def main():
    run_id, attempts, out_path = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    record = []
    for n in range(1, attempts + 1):
        run = api(f"repos/{REPO}/actions/runs/{run_id}/attempts/{n}")
        jobs = api(f"repos/{REPO}/actions/runs/{run_id}/attempts/{n}/jobs?per_page=100")["jobs"]
        row = {"attempt": n, "head_sha": run["head_sha"], "event": run["event"],
               "run_conclusion": run["conclusion"], "jobs": {}}
        for job in jobs:
            secs = None
            if job.get("started_at") and job.get("completed_at"):
                secs = int((ts(job["completed_at"]) - ts(job["started_at"])).total_seconds())
            row["jobs"][job["name"]] = {"id": job["id"], "conclusion": job["conclusion"],
                                        "started_at": job["started_at"],
                                        "completed_at": job["completed_at"], "seconds": secs,
                                        "steps": [(s["name"], s["conclusion"]) for s in job.get("steps", [])]}
        record.append(row)
    with open(out_path, "w") as fh:
        json.dump(record, fh, indent=1)
    print("attempt head event run " + " ".join(FIRMWARE) + " rtl-fast")
    worst = (0, None)
    for row in record:
        cells = []
        for name in FIRMWARE:
            j = row["jobs"].get(name)
            cells.append(f"{j['seconds']}s/{j['conclusion']}" if j else "absent")
            if j and j["seconds"] is not None and j["seconds"] > worst[0]:
                worst = (j["seconds"], (row["attempt"], name))
        agg = row["jobs"].get("rtl-fast", {}).get("conclusion")
        print(row["attempt"], row["head_sha"][:12], row["event"], row["run_conclusion"], *cells, agg)
    print(f"slowest: {worst[0]} s at {worst[1]} = {100 * worst[0] / 2700:.1f} % of 2700 s")


if __name__ == "__main__":
    main()
