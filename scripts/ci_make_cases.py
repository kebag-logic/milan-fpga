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
        with ThreadPoolExecutor(max_workers=jobs) as pool:
            results = list(pool.map(lambda name: execute(directory, name, forms[name]), selected))
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
