#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Collect physical suite logs only after every executed case union succeeds."""

import argparse
import json
from pathlib import Path
import shutil

from ci_suite_pieces import PIECE_SECONDS, expand_suites, union
from suite_shards import ROOT, WORKER_OVERHEAD_SECONDS, balance, sweep_suites


def collect(workers: Path, unions: Path, output: Path, head: str) -> None:
    """Refuse extra, missing, misplaced or duplicate logs before the original tally."""
    physical = sweep_suites(ROOT / "tb/verilator")
    pieces = expand_suites(physical)
    total = len(WORKER_OVERHEAD_SECONDS)
    owners, _ = balance(pieces, total)
    expected_roots = {"suite-logs-" + str(leg) for leg in range(total)}
    if {path.name for path in workers.iterdir()} != expected_roots:
        raise ValueError("worker artifact inventory differs")
    output.mkdir(parents=True, exist_ok=False)
    for leg in range(total):
        directory = workers / ("suite-logs-" + str(leg))
        expected = {name for name in pieces if owners[name] == leg}
        if {path.stem for path in directory.glob("*.log")} != expected:
            raise ValueError(f"worker {leg}: executed suite ownership differs")
        if directory.joinpath("TARGET_SHA").read_text() != head + "\n":
            raise ValueError("worker target differs")
        for name in expected:
            if "__" not in name:
                shutil.copyfile(directory / (name + ".log"), output / (name + ".log"))
    if {path.name for path in unions.iterdir()} != {"suite-union-" + suite for suite in PIECE_SECONDS}:
        raise ValueError("union artifact inventory differs")
    for suite in PIECE_SECONDS:
        directory = unions / ("suite-union-" + suite)
        receipt = json.loads(directory.joinpath("union.json").read_text())
        if receipt["head"] != head or receipt["suite"] != suite or receipt["union"] != "pass":
            raise ValueError("suite union did not pass at this head")
        rebuilt = union(suite, sorted(workers.iterdir()), output / "proofs" / suite,
                        head, receipt["tree"])
        if rebuilt != receipt:
            raise ValueError("union receipt differs from retained case observations")
        observed = output / "proofs" / suite / (suite + ".log")
        if observed.read_bytes() != (directory / (suite + ".log")).read_bytes():
            raise ValueError("union log differs from retained execution logs")
        shutil.copyfile(observed, output / (suite + ".log"))
    if {path.stem for path in output.glob("*.log")} != set(physical):
        raise ValueError("complete physical suite inventory differs")


def main() -> int:
    """Collect downloaded workflow artifacts without interpreting their test verdicts."""
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("workers", "unions", "output"):
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument("--head", required=True)
    args = parser.parse_args()
    try:
        collect(args.workers, args.unions, args.output, args.head)
    except (OSError, ValueError, KeyError) as exc:
        print(f"suite collection refused: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
