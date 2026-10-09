#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Grade sub-arm INTERNAL pulls on a 25 MHz model with 1/64-sample holds.

Every case is a standing, gradable stream, including the no-hold control.
Each simulation keeps its own command, log and return code. No expected
value is read from the implementation.
"""

import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import subprocess

CASES = (
    ("cross-2042", "42.64", "204.2"),
    ("cross-2044", "42.64", "204.4"),
    ("cross-2046", "42.64", "204.6"),
    ("above-old-arm", "43.29", "204.4"),
    ("one-quantum", "41.9921875", "204.0"),
    ("eight-quanta", "44.270833333", "210.42"),
    ("negative-sub-arm", "40.690104167", "210.42"),
    ("no-hold", "0", "204.4"),
)

TWO_PULLS = (
    ("second-inside", "0.10", True),
    ("second-outside", "1.50", False),
)


def run_case(exe: Path, out: Path, case: tuple[str, str, str]) -> int:
    """Run one named physical hold and preserve its original verdict."""
    name, hold, latency = case
    argv = [str(exe), "--case", "pullin", "--hold-us", hold,
            "--latency-us", latency, "--after-s", "1.5"]
    return run_argv(out, name, argv)


def run_two_pulls(exe: Path, out: Path, case: tuple[str, str, bool]) -> int:
    """Exercise both sides of the declared recovery residual."""
    name, gap, inside = case
    argv = [str(exe), "--case", "pullin", "--hold-us", "42.64",
            "--latency-us", "204.4", "--after-s", "1.5",
            "--second-after-action-s", gap, "--second-hold-us", "40.690104167"]
    if inside:
        argv.append("--second-inside-recovery")
    return run_argv(out, name, argv)


def run_argv(out: Path, name: str, argv: list[str]) -> int:
    """Keep the stimulus, output and original return code together."""
    (out / f"{name}.command.json").write_text(json.dumps(argv) + "\n")
    with (out / f"{name}.log").open("w") as log:
        rc = subprocess.run(argv, stdout=log, stderr=subprocess.STDOUT, check=False).returncode
    (out / f"{name}.rc").write_text(f"{rc}\n")
    print(f"SMALL PULL {name}: rc {rc}", flush=True)
    return rc


def main() -> int:
    """Run the independent cases concurrently, failing on any failed case."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--exe", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--jobs", type=int, default=4)
    args = parser.parse_args()
    if args.jobs < 1:
        parser.error("--jobs must be positive")
    args.out.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = [pool.submit(run_case, args.exe.resolve(), args.out, case) for case in CASES]
        futures += [pool.submit(run_two_pulls, args.exe.resolve(), args.out, case) for case in TWO_PULLS]
        results = [future.result() for future in futures]
    print(f"small pulls: {sum(rc == 0 for rc in results)}/{len(results)} passed")
    return int(any(results))


if __name__ == "__main__":
    raise SystemExit(main())
