#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Run the case inventory owned by a suite Makefile, retaining executed receipts.

The suite's ci-list target and default run share their inventory. Each case
has a build target and an exec target. Build diagnostics do not enter the
checked-value transcript, so paths and compiler timing cannot impersonate
simulation observations. Neither compiler flags nor assertions are selected
by this driver.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import os
import re
from pathlib import Path
import subprocess
import sys

from ci_case_receipts import Receipt, partition, validate_inventory
from suite_tally import log_reports_failure, scan, is_nocount

ROOT = Path(__file__).resolve().parents[1]


def inventory(directory: Path) -> list[str]:
    """Ask the owning Makefile for the cases its default invocation executes."""
    out = subprocess.run(["make", "-s", "--no-print-directory", "-C", str(directory), "ci-list"],
                         capture_output=True, text=True, check=True)
    names = out.stdout.splitlines()
    validate_inventory(names)
    if any(not name.replace("-", "").replace("_", "").isalnum() for name in names):
        raise ValueError("case names must be simple Makefile target suffixes")
    return names


def receipt_forms(directory: Path, names: list[str]) -> dict[str, str]:
    """Require the owner's receipt registration for every executed case."""
    out = subprocess.run(["make", "-s", "--no-print-directory", "-C", str(directory), "ci-receipts"],
                         capture_output=True, text=True, check=True)
    rows = [line.split("\t") for line in out.stdout.splitlines()]
    if (any(len(row) != 2 for row in rows) or [row[0] for row in rows] != names
            or any(row[1] not in ("tally", "tally-stdout", "result-stdout") for row in rows)):
        raise ValueError("receipt forms must register every case exactly once")
    return dict(rows)


def execute(directory: Path, name: str, form: str = "tally") -> tuple[str, int, str]:
    """Execute an already built case using its declared observation contract."""
    command = ["make", "-s", "--no-print-directory", "-C", str(directory)]
    ran = subprocess.run([*command, "exec-" + name], capture_output=True, text=True, check=False)
    combined = ran.stdout + ran.stderr
    output = combined if form == "tally" else ran.stdout
    if form != "tally":
        sys.stderr.write(ran.stderr)
    checks, failures, matched, unparsed, skipped = scan(combined)
    _, failed = log_reports_failure(combined)
    if form == "result-stdout":
        verdicts = re.findall(r"^RESULT:.*$", ran.stdout, re.MULTILINE)
        evidence = verdicts == ["RESULT: PASS"]
    else:
        evidence = not unparsed and not is_nocount(checks, failures, matched, skipped)
    passed = ran.returncode == 0 and not failed and evidence
    return "pass" if passed else "failed", ran.returncode, output


#: Measured execution cost per case, in seconds, for the suites whose pieces
#: run more than one case. Only the START order reads it: a piece's cases are
#: submitted longest first, so its longest case no longer waits behind the
#: short ones for a free worker, and every result is still printed and
#: recorded in driver order, so the transcript and the receipt do not change.
#: A case absent here costs 0 and keeps its driver order behind the measured
#: ones; a stale figure can only make a piece slower, never change a verdict.
#: How the figures were taken, and how to retake them: TESTING.md, "Case
#: start order in a piece". Issue #998; REQ-VER-01 and REQ-VER-04.
CASE_SECONDS: dict[str, dict[str, int]] = {
    # 2026-11-24, at fcbc31f3: each case's `exec-<case>` alone on one core of its own, CPU seconds.
    "milan_dp": {
        "aclk": 1558, "render-mutants": 1375, "gptp": 862, "gptp-lat": 838, "dynmap": 617, "notify": 366,
        "counters-8": 300, "counters-8-frames": 296, "crflic": 247, "nxn8": 242, "counters-1": 144,
        "counters-1-frames": 142, "nxn": 101, "nxn4c": 99, "bootsa": 96, "nxndv": 92, "sidmove8": 45,
        "ax1x1": 26, "base": 23, "nolpf": 22, "sidmove": 22, "maprec8": 15, "tspec8": 14, "maprec4": 9,
        "prune": 3, "split": 1,
    },
    # 2026-11-24, at 45d5c35a: each case's log span in one `make -C tb/verilator/media_phase`, three cases at once on
    # four CPUs, wall seconds of its one single-threaded simulation.
    "media_phase": {
        "ramp": 314, "edge": 221, "engage": 189, "step": 189, "phcstep": 180, "mr": 173, "internal": 143,
        "holdover": 135, "burst": 131, "edge2": 118, "slew": 118, "engage2": 104, "carry": 51,
    },
}


def start_order(suite: str, selected: list[str]) -> list[str]:
    """The selected cases longest first by CASE_SECONDS; ties keep driver order."""
    cost = CASE_SECONDS.get(suite, {})
    return sorted(selected, key=lambda name: -cost.get(name, 0))


def execute_all(directory: Path, suite: str, selected: list[str], forms: dict[str, str],
                jobs: int) -> list[tuple[str, int, str]]:
    """Execute every selected case on `jobs` workers, started longest first, with the
    results returned in driver order."""
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        # The pool starts submitted work first-in first-out.
        futures = {name: pool.submit(execute, directory, name, forms[name])
                   for name in start_order(suite, selected)}
        return [futures[name].result() for name in selected]


def build(directory: Path, name: str) -> int:
    """Build a selected case; shared outputs have one sequential owner."""
    return subprocess.run(["make", "-s", "--no-print-directory", "-C", str(directory),
                           "build-" + name], check=False).returncode


def main() -> int:
    """Run the complete inventory by default, or its selected partition."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--suite", required=True)
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--shard")
    parser.add_argument("--jobs", type=int, choices=range(1, 5), default=2)
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    directory = ROOT / "tb/verilator" / args.suite
    if directory.parent != ROOT / "tb/verilator" or not directory.is_dir():
        parser.error("suite must name one local suite directory")
    try:
        names = inventory(directory)
        if args.list:
            print(json.dumps(names))
            return 0
        forms = receipt_forms(directory, names)
        selected = partition(names, args.shard)
        receipt = Receipt(ROOT, args.suite, names, args.shard, args.receipt)
        failed = False
        subprocess.run(["make", "-s", "--no-print-directory", "-C", str(directory),
                        "ci-prepare"], check=True)
        for name in selected:
            rc = build(directory, name)
            if rc:
                receipt.record(name, "build-failed", rc, "build failed before case execution\n")
                receipt.finish()
                return 1
        # Frame dumps deliberately share an output path; presence serializes.
        jobs = 1 if "MILAN_COUNTER_FRAME_OUT" in os.environ else args.jobs
        results = execute_all(directory, args.suite, selected, forms, jobs)
        for name, (outcome, rc, output) in zip(selected, results):
            print(f"======== {args.suite}/{name} ========", flush=True)
            sys.stdout.write(output)
            result_line = "RESULT: PASS" if forms[name] == "result-stdout" and outcome == "pass" else None
            receipt.record(name, outcome, rc, output, result_line=result_line)
            failed |= outcome != "pass"
        receipt.finish()
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"case execution refused: {exc}", file=sys.stderr)
        return 1
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
