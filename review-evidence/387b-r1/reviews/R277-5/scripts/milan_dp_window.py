#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""R276-5 reviewer probe: read-only measurement of the hosted milan_dp window.

For each rtl-full workflow run id, find the Verilator shard job whose log
carries `PASS     milan_dp` (or FAIL/TIMEOUT), and print the time from its
`shard: k/n` line to that verdict line, the check tally, and the margin to the
2700 s per-suite budget. Uses only `gh api` GETs.
Usage: milan_dp_window.py <run id> ...
"""
import json
import re
import subprocess
import sys
from datetime import datetime

REPO = "repos/kebag-logic/milan-fpga"
BUDGET_S = 2700.0
TS = re.compile(r"^(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d+)Z (.*)$")
ESC = re.compile(r"\x1b\[[0-9;]*m")


def gh(path: str, raw: bool = False) -> str:
    cmd = ["gh", "api", path] + (["--allow-escape-sequences"] if raw else [])
    return subprocess.run(cmd, capture_output=True, text=True, check=True).stdout


def stamp(s: str) -> datetime:
    return datetime.fromisoformat(s[:26])


def main() -> int:
    for run in sys.argv[1:]:
        meta = json.loads(gh(f"{REPO}/actions/runs/{run}"))
        jobs = json.loads(gh(f"{REPO}/actions/runs/{run}/jobs?per_page=100"))["jobs"]
        found = False
        for job in jobs:
            if not job["name"].startswith("Verilator shard"):
                continue
            log = ESC.sub("", gh(f"{REPO}/actions/jobs/{job['id']}/logs", raw=True))
            start = verdict = checks = None
            for line in log.splitlines():
                m = TS.match(line)
                if not m:
                    continue
                t, body = m.groups()
                if body.startswith("shard: "):
                    start = t
                if re.match(r"(PASS|FAIL|TIMEOUT)\s+milan_dp$", body):
                    verdict = (t, body.split()[0])
                if body.startswith("checks: ") and verdict:
                    checks = body
            if verdict and start:
                w = (stamp(verdict[0]) - stamp(start)).total_seconds()
                print(f"run={run} sha={meta['head_sha'][:10]} event={meta['event']} "
                      f"job={job['id']} ({job['name']}) milan_dp={verdict[1]} "
                      f"window_s={w:.1f} margin_s={BUDGET_S - w:.1f} "
                      f"margin_pct={100 * (BUDGET_S - w) / BUDGET_S:.1f} [{checks}]")
                found = True
                break
        if not found:
            print(f"run={run} sha={meta['head_sha'][:10]}: no milan_dp verdict found")
    return 0


if __name__ == "__main__":
    sys.exit(main())
