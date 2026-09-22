#!/usr/bin/env python3
"""Record focused controls, with exact source identity and process statuses.

Usage: python3 checks.py LANE OUTPUT_DIRECTORY
The runner bank currently includes its Makefile integration check and will
fail until integration is implemented; this script never suppresses a gate.
An external 120-second guard on the process-based runner bank is a hang guard,
not a simulation timeout or passing result. No expensive native banks run here.
"""
import argparse
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

BASE = "483a133ed08867ea0d300d2b4a027b5b48a4282f"
COMMANDS = (
    ("runner", ["timeout", "120s", "python3", "-u", "tb/verilator/milan_dp/test_sim_pool.py"]),
    ("phase-observation", ["python3", "tb/verilator/milan_dp/test_render_phase_observation.py"]),
    ("tally-controls", ["python3", "scripts/suite_tally.py", "--selftest"]),
    ("ownership-controls", ["python3", "scripts/suite_shards.py", "--selftest"]),
    ("docs", ["python3", "scripts/docs_check.py"]),
    ("contents", ["python3", "scripts/gen_toc.py", "--check"]),
    ("em-dash", ["python3", "scripts/check_em_dash.py", "--base", BASE]),
    ("python-idiom", ["python3", "scripts/check_py_idiom.py"]),
    ("shell-idiom", ["python3", "scripts/check_sh_idiom.py"]),
    ("hygiene", ["python3", "scripts/check_hygiene.py", "--check"]),
    ("evidence", ["python3", "scripts/measure_test_evidence.py", "--check"]),
    ("fail-fast", ["python3", "scripts/measure_fail_fast.py", "--check"]),
    ("todo", ["python3", "scripts/check_todo_ownership.py"]),
)


def capture(cmd, lane):
    return subprocess.check_output(["rtk", "proxy", *cmd], cwd=lane, text=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("lane", type=Path)
    ap.add_argument("out", type=Path)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    receipts = dict(head=capture(["git", "rev-parse", "HEAD"], args.lane).strip(),
                    tree=capture(["git", "rev-parse", "HEAD^{tree}"], args.lane).strip(),
                    status=capture(["git", "status", "--porcelain"], args.lane),
                    sources={str(p.relative_to(args.lane)): hashlib.sha256(p.read_bytes()).hexdigest()
                             for p in (args.lane / "tb/verilator/milan_dp").glob("*sim_pool.py")},
                    checks=[])
    for name, cmd in COMMANDS:
        started = time.monotonic()
        with (args.out / f"{name}.log").open("wb") as log:
            rc = subprocess.run(["rtk", "proxy", *cmd], cwd=args.lane,
                                stdout=log, stderr=subprocess.STDOUT).returncode
        receipts["checks"].append(dict(name=name, command=["rtk", "proxy", *cmd], exit=rc,
                                      wall_seconds=time.monotonic()-started))
        (args.out / "receipts.json").write_text(json.dumps(receipts, indent=2) + "\n")
        print(name, "exit", rc, flush=True)
    return int(any(r["exit"] for r in receipts["checks"]))


if __name__ == "__main__":
    sys.exit(main())
