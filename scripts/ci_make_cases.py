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


def execute(directory: Path, name: str) -> tuple[str, int, str]:
    """Build and execute one original case; missing or failing tallies refuse it."""
    command = ["make", "-s", "--no-print-directory", "-C", str(directory)]
    built = subprocess.run([*command, "build-" + name], check=False)
    if built.returncode:
        return "build-failed", built.returncode, "build failed before case execution\n"
    ran = subprocess.run([*command, "exec-" + name], capture_output=True, text=True, check=False)
    output = ran.stdout + ran.stderr
    checks, failures, matched, unparsed, skipped = scan(output)
    _, failed = log_reports_failure(output)
    passed = (ran.returncode == 0 and not failed and not unparsed
              and not is_nocount(checks, failures, matched, skipped))
    return "pass" if passed else "failed", ran.returncode, output


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
        selected = partition(names, args.shard)
        receipt = Receipt(ROOT, args.suite, names, args.shard, args.receipt)
        failed = False
        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            results = list(pool.map(lambda name: execute(directory, name), selected))
        for name, (outcome, rc, output) in zip(selected, results):
            print(f"======== {args.suite}/{name} ========", flush=True)
            sys.stdout.write(output)
            receipt.record(name, outcome, rc, output)
            failed |= outcome != "pass"
        receipt.finish()
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"case execution refused: {exc}", file=sys.stderr)
        return 1
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
