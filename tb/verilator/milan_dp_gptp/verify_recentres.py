#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Plant two ordering faults through the physical leg's real wire checker."""

import argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import re
import subprocess


def run_case(binary: Path, switch: str) -> list[tuple[str, bool]]:
    """Run one real-wire control and account for its exact expected failures."""
    result = subprocess.run([str(binary), switch], cwd=binary.parent.parent,
                            text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = result.stdout
    (binary.parent / f"{switch[2:]}.log").write_text(output)
    errors = re.findall(r"ORDER ERROR output_pdu=(\d+).*recentre=(\d+)", output)
    declared = set(re.findall(r"RECENTRE output=\d+ input_pdu=\d+ output_pdu=(\d+)", output))
    failures = [line for line in output.splitlines() if "[FAIL]" in line]
    large = switch == "--large-step-control"
    position = bool(errors) and all((frame in declared) == large for frame, _ in errors)
    wire_steps = re.findall(r"RECENTRE WIRE .*declared_step=(-?\d+) observed_step=(-?\d+)", output)
    repeats = re.findall(r"ORDER ERROR .*last=(\d+) index=(\d+) expected_delta=1 recentre=0", output)
    measured_fault = (any(int(observed) == int(declared_step) - 1
                          for declared_step, observed in wire_steps) if large
                      else any(previous == current for previous, current in repeats))
    return [
        (f"{switch}: control ran", "planted=1" in output),
        (f"{switch}: wire ordering oracle rejects the planted step",
         result.returncode == 1 and any("all monitored audio sample ordering errors" in line
                                       for line in failures)),
        (f"{switch}: error belongs to the required PDU location", position),
        (f"{switch}: the measured wire step is the planted fault", measured_fault),
        (f"{switch}: payload and packet sequence remain valid",
         not any("all monitored audio payload errors" in line
                 or "all monitored AAF packet sequence errors" in line for line in failures)),
        (f"{switch}: declared step and both unchanged counters were observed",
         bool(re.search(r"RECENTRE output=.*step_events=-\d+ dup=0->0 skip=0->0", output))),
        (f"{switch}: no unrelated failing assertion",
         bool(failures) and all("audio sample order, no duplicates or gaps" in line
                               or "all monitored audio sample ordering errors" in line
                               for line in failures)),
    ]


def main() -> int:
    """Execute both independent controls with an explicit concurrency limit."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jobs", type=int, default=2)
    args = parser.parse_args()
    if args.jobs < 1:
        parser.error("--jobs must be positive")
    binary = (Path(__file__).resolve().parent.parent
              / "milan_dp/obj_ax1x1gptp/Vmilan_dp_ax1x1gptp")
    switches = ("--extra-repeat-control", "--large-step-control")
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        batches = list(pool.map(lambda switch: run_case(binary, switch), switches))
    results = [result for batch in batches for result in batch]
    for label, passed in results:
        print(f"[{' ok ' if passed else 'FAIL'}] {label}")
    failures = sum(not passed for _, passed in results)
    print(f"== ax1x1gptp recentre controls: checks: {len(results)}   failures: {failures} ==")
    return int(failures != 0)


if __name__ == "__main__":
    raise SystemExit(main())
