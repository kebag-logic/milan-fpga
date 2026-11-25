#!/usr/bin/env python3
"""R924: bounded concurrent controls; no simulation or synthesis bank."""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys
import time

PACKET = Path(__file__).resolve().parent
CLONE = Path(sys.argv[1]).resolve()
TASKS = {
    "stage-probe": [sys.executable, str(PACKET / "probe_stage.py"), str(CLONE)],
    "workflow-check": [sys.executable, "scripts/ci_gate_workflows.py", "--check"],
    "event-check": [sys.executable, "scripts/ci_events.py", "--check"],
    "case-controls": [sys.executable, "scripts/ci_make_cases_selftest.py"],
    "piece-controls": [sys.executable, "scripts/ci_suite_pieces_selftest.py"],
    "shard-controls": [sys.executable, "scripts/suite_shards.py", "--selftest"],
    "event-controls": [sys.executable, "scripts/ci_events.py", "--selftest"],
}


def run(item):
    label, command = item
    tmp = PACKET / "scratch" / label; tmp.mkdir(exist_ok=True)
    environment = {**os.environ, "TMPDIR": str(tmp), "PYTHONDONTWRITEBYTECODE": "1", "MAKEFLAGS": "-j1 --no-print-directory"}
    start = time.monotonic()
    with (PACKET / (label + ".log")).open("w") as log:
        rc = subprocess.run(command, cwd=CLONE, env=environment, stdout=log, stderr=subprocess.STDOUT, timeout=590).returncode
    (PACKET / (label + ".rc")).write_text(str(rc) + "\n")
    return {"name": label, "command": command[1:], "rc": rc, "wall_seconds": round(time.monotonic()-start, 3)}


def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(run, TASKS.items()))
    (PACKET / "focused-results.json").write_text(json.dumps({"reviewer": "R924", "results": results}, indent=2) + "\n")
    print(json.dumps(results, indent=2))
    return int(any(row["rc"] for row in results))


if __name__ == "__main__":
    raise SystemExit(main())
