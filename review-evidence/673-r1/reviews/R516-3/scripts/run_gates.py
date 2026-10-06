#!/usr/bin/env python3
"""Run focused composition gates concurrently, with foreground child waits."""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys
import time

repo = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parents[1]
env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", GIT_NO_REPLACE_OBJECTS="1",
           TMPDIR=str(packet / "scratch"))
gates = {
    "docs_check": ["python3", "scripts/docs_check.py"],
    "toc_check": ["python3", "scripts/gen_toc.py", "--check"],
    "toc_anchors": ["python3", "scripts/gen_toc.py", "--verify-anchors"],
    "em_dash": ["python3", "scripts/check_em_dash.py", "--base", "28cdb5891b2b2d8a79b94a5bc2fb703c9fa8c721"],
    "ci_events_check": ["python3", "scripts/ci_events.py", "--check"],
    "ci_events_selftest": ["python3", "scripts/ci_events.py", "--selftest"],
    "evidence_check": ["python3", "scripts/measure_test_evidence.py", "--check"],
    "evidence_selftest": ["python3", "scripts/measure_test_evidence.py", "--selftest"],
    "scope_selftest": ["python3", "scripts/ci_scope.py", "--selftest"],
    "shards_selftest": ["python3", "scripts/suite_shards.py", "--selftest"],
    "shell_syntax": ["bash", "-n", "scripts/run_all_suites.sh"],
    "suite_inventory": ["bash", "scripts/run_all_suites.sh", "--list"],
}
suffix = "_retry" if len(sys.argv) > 2 else ""
if len(sys.argv) > 2:
    gates = {name: gates[name] for name in sys.argv[2:]}

def run(item):
    name, cmd = item
    started = time.monotonic()
    with (packet / "receipts" / (name + suffix + ".log")).open("wb") as log:
        result = subprocess.run(["rtk", "proxy", *cmd], cwd=repo, env=env,
                                stdout=log, stderr=subprocess.STDOUT, timeout=540)
    row = {"name": name, "command": cmd, "rc": result.returncode,
           "seconds": round(time.monotonic() - started, 3)}
    (packet / "receipts" / (name + suffix + ".rc")).write_text(str(result.returncode) + "\n")
    print(json.dumps(row), flush=True)
    return row

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    rows = list(pool.map(run, gates.items()))
(packet / "receipts" / ("gates" + suffix + ".json")).write_text(json.dumps(rows, indent=2) + "\n")
sys.exit(any(row["rc"] for row in rows))
