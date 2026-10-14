#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Schedule driver-owned case partitions and prove their executed union.

Only leg counts and measured durations live here. Case membership always comes
from the owning driver's --list output. The serial sweep remains unchanged.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
from suite_shards import PIECE_SECONDS, expand_suites


def piece_identity(piece: str) -> tuple[str, int, int]:
    """Refuse unknown or noncanonical coordinates before launching anything."""
    suite, separator, value = piece.rpartition("__")
    if (not separator or suite not in PIECE_SECONDS or not value.isdecimal()
            or str(int(value)) != value or int(value) >= len(PIECE_SECONDS[suite])):
        raise ValueError("unknown CI suite piece: " + piece)
    return suite, int(value), len(PIECE_SECONDS[suite])


def driver(suite: str) -> list[str]:
    """The same registered driver supplies inventory and execution."""
    if suite not in PIECE_SECONDS:
        raise ValueError("suite has no registered case driver: " + suite)
    if suite == "milan_dp_mclk":
        return [sys.executable, "tb/verilator/milan_dp_mclk/mclk_mutants.py"]
    if suite in ("capture_coherence", "maap"):
        command = [sys.executable, f"tb/verilator/{suite}/mutants.py", "--whole-suite"]
        # Sixteen local CPUs must not turn the hosted four-case bank into
        # sixteen simultaneous model builds inside one bounded job.
        return command + (["--jobs", str(min(4, len(os.sched_getaffinity(0))))]
                          if suite == "capture_coherence" else [])
    return [sys.executable, "scripts/ci_make_cases.py", "--suite", suite,
            "--jobs", str(min(2, len(os.sched_getaffinity(0))))]


def inventory(suite: str, root: Path = ROOT) -> list[str]:
    """Read the owning driver anew; receipts cannot define their own universe."""
    from ci_case_receipts import validate_inventory
    result = subprocess.run([*driver(suite), "--list"], cwd=root, check=True,
                            capture_output=True, text=True)
    names = json.loads(result.stdout)
    validate_inventory(names)
    return names


def run(piece: str, destination: Path) -> int:
    """Execute one selected leg under the sweep's existing process/timeout owner."""
    suite, leg, total = piece_identity(piece)
    destination.mkdir(parents=True, exist_ok=True)
    if suite == "milan_dp_mclk":
        subprocess.run(["make", "-C", "tb/verilator/milan_dp_mclk", "mclk-build"],
                       cwd=ROOT, check=True)
    command = [*driver(suite), "--shard", f"{leg}/{total}",
               "--receipt", str(destination / (piece + ".json"))]
    environment = dict(os.environ)
    if suite == "capture_coherence":
        cpus = len(os.sched_getaffinity(0))
        jobs = min(4, cpus)
        environment["VERILATOR_JOBS"] = str(max(1, cpus // jobs))
        environment["MAKEFLAGS"] = "-j1 --no-print-directory"
    return subprocess.run(command, cwd=ROOT, env=environment, check=False).returncode


def union(suite: str, roots: list[Path], output: Path, head: str, tree: str) -> dict:
    """Bind executed observations and original log tallies to the fresh inventory."""
    from ci_case_receipts import canonical, read_receipts, verify
    from suite_tally import is_nocount, log_reports_failure, scan
    names = inventory(suite)
    paths = sorted(path for root in roots for path in root.glob(f"cases/{suite}__*.json"))
    observations = verify(names, read_receipts(paths), suite, head, tree)
    expected = {f"{suite}__{leg}" for leg in range(len(PIECE_SECONDS[suite]))}
    logs = [path for root in roots for path in root.glob(f"{suite}__*.log")]
    if len(logs) != len(expected) or {path.stem for path in logs} != expected:
        raise ValueError("missing or duplicated executed leg log")
    text = "\n".join(path.read_text() for path in sorted(logs, key=lambda path: path.name))
    checks, failures, matched, unparsed, skipped = scan(text)
    if (unparsed or is_nocount(checks, failures, matched, skipped)
            or log_reports_failure(text)[1]):
        raise ValueError("combined suite log fails the unchanged tally reader")
    result = {"suite": suite, "head": head, "tree": tree, "inventory": names,
              "legs": [{"shard": value["shard"], "cases": [row["case"] for row in value["results"]]}
                       for value in read_receipts(paths)],
              "union": "pass", "verdicts_sha256": hashlib.sha256(canonical(observations)).hexdigest()}
    output.mkdir(parents=True, exist_ok=True)
    (output / (suite + ".log")).write_text(text)
    (output / "TARGET_SHA").write_text(head + "\n")
    (output / "union.json").write_bytes(canonical(result) + b"\n")
    return result


def main() -> int:
    """Run a selected piece, or verify one complete suite's retained artifacts."""
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="operation", required=True)
    execute = sub.add_parser("run")
    execute.add_argument("piece")
    execute.add_argument("--receipts", required=True, type=Path)
    check = sub.add_parser("union")
    check.add_argument("suite", choices=PIECE_SECONDS)
    check.add_argument("--output", required=True, type=Path)
    check.add_argument("--head", required=True)
    check.add_argument("--tree", required=True)
    check.add_argument("roots", nargs="+", type=Path)
    args = parser.parse_args()
    try:
        if args.operation == "run":
            return run(args.piece, args.receipts)
        result = union(args.suite, args.roots, args.output, args.head, args.tree)
        print(f"{args.suite}: {len(result['inventory'])} cases exactly once; original tally passed")
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        print(f"suite piece refused: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
