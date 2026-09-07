#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Require setup failures to omit unexecuted cumulative audio assertions."""

from pathlib import Path
import subprocess
import re
import tempfile


NEGATIVE_CASES = ["generated AEM image missing", "talker admission withheld", "talker admission withdrawn"]
LABELS = (
    "all monitored audio payload errors, excluding declared warm-up",
    "all monitored audio sample ordering errors",
    "all monitored AAF packet sequence errors",
)


def main() -> int:
    """Run the real binary without its image; grade only executed evidence."""
    binary = (Path(__file__).resolve().parent.parent
              / "milan_dp/obj_ax1x1gptp/Vmilan_dp_ax1x1gptp")
    checks = 0
    failures = 0
    for error in NEGATIVE_CASES[:1]:
        # An empty run directory withholds the relative AEM input without
        # renaming the shared generated image or racing another build.
        with tempfile.TemporaryDirectory(prefix="ax1x1gptp-abort-") as run_dir:
            result = subprocess.run([str(binary)], cwd=run_dir, text=True,
                                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = result.stdout
        outcomes = [
            ("setup error exits nonzero", result.returncode == 1 and f"[FAIL] {error}" in output),
            ("setup failure runs zero cycles", "simulated_duration_seconds=0.000000000 cycles=0" in output),
            ("only the executed setup failure is counted",
             "checks: 1   failures: 1" in output and "[ ok ]" not in output),
        ]
        outcomes.extend((f"uncounted omission: {label}",
                         f"NOT RUN: {label} (no comparisons; uncounted)" in output)
                        for label in LABELS)
        for label, passed in outcomes:
            checks += 1
            failures += not passed
            print(f"[{' ok ' if passed else 'FAIL'}] {label}")
        if failures:
            print(output)
    print(f"== ax1x1gptp setup abort: checks: {checks}   failures: {failures} ==")
    return int(failures != 0) | verify_no_tx(binary)


WINDOW_LABELS = (
    "audio sample order, no duplicates or gaps",
    "AAF packet sequence order",
    "AAF uncertainty matches public stable state",
)


def verify_no_tx(binary: Path) -> int:
    """Withhold admission on real RTL; unexecuted window checks must not pass."""
    checks = 0
    failures = 0
    for switch, previous in (("--no-tx-control", 0), ("--stop-tx-control", 1)):
        result = subprocess.run([str(binary), switch], cwd=binary.parent.parent, text=True,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = result.stdout
        # Keep the failing DUT transcript separate from the positive meta-test
        # tally: the common reader must never swallow those failures.
        (binary.parent / f"{switch[2:]}.log").write_text(output)
        windows = re.findall(r"AUDIO result rx=(\d+) tx=(\d+) samples=(\d+)", output)
        counters = re.search(r"AUDIO comparisons payload=(\d+) sample_order=(\d+) packet_sequence=(\d+)",
                             output)
        outcomes = [
            ("silent talker retains a nonzero DUT verdict", result.returncode == 1),
            ("silent window has RX traffic and zero TX or samples",
             bool(windows) and windows[-1] == ("160", "0", "0")),
            ("activity and payload assertions still fail",
             all(any("[FAIL]" in line and label in line for line in output.splitlines())
                 for label in ("both eight-channel packet directions active",
                               "all eight channel payloads match the supplied ramp"))),
            ("comparison history matches the selected control",
             bool(counters) and all((int(value) > 0) == bool(previous) for value in counters.groups())),
        ]
        for label in WINDOW_LABELS:
            outcomes.extend([
                (f"uncounted window omission: {label}",
                 f"NOT RUN: {label} (no comparisons in this window; uncounted)" in output),
                (f"passes only from executed windows: {label}",
                 sum("[ ok ]" in line and label in line for line in output.splitlines()) == previous),
            ])
        for label, passed in outcomes:
            checks += 1
            failures += not passed
            print(f"[{' ok ' if passed else 'FAIL'}] {switch}: {label}")
        if failures:
            print(output)
    print(f"== ax1x1gptp no-TX accounting: checks: {checks}   failures: {failures} ==")
    return int(failures != 0)


if __name__ == "__main__":
    raise SystemExit(main())
