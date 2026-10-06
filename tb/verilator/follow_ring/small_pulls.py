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
    ("negative-sub-arm", "40.690104167", "210.42"),
    ("no-hold", "0", "204.4"),
)


def run_case(exe: Path, out: Path, case: tuple[str, str, str]) -> int:
    """Run one named physical hold and preserve its original verdict."""
    name, hold, latency = case
    argv = [str(exe), "--case", "pullin", "--hold-us", hold,
            "--latency-us", latency, "--after-s", "1.5"]
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
        results = list(pool.map(lambda case: run_case(args.exe.resolve(), args.out, case), CASES))
    print(f"small pulls: {sum(rc == 0 for rc in results)}/{len(results)} passed")
    return int(any(results))


if __name__ == "__main__":
    raise SystemExit(main())
