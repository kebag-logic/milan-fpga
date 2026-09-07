#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Require setup failures to omit unexecuted cumulative audio assertions."""

from pathlib import Path
import subprocess
import re
import tempfile


NEGATIVE_CASES = ["generated AEM image missing"]
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
    for error in NEGATIVE_CASES:
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
    return int(failures != 0) | verify_no_tx(binary) | verify_no_pdelay(binary)


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


def verify_no_pdelay(binary: Path) -> int:
    """An unanswered real request must not earn first-exchange comparison passes."""
    result = subprocess.run([str(binary), "--no-pdelay-control"], cwd=binary.parent.parent,
                            text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = result.stdout
    (binary.parent / "no-pdelay-control.log").write_text(output)
    events = re.search(r"PDELAY event accounting requests=(\d+) responses=(\d+)", output)
    outcomes = [
        ("missing response retains a nonzero DUT verdict", result.returncode == 1),
        ("a real request was unanswered",
         bool(events) and int(events[1]) > 0 and int(events[2]) == 0),
        ("missing response assertion still fails",
         any("[FAIL]" in line and "first Pdelay response completed" in line for line in output.splitlines())),
        ("first exchange remains incomplete", "NOT RUN TO COMPLETION: first Pdelay exchange" in output),
    ]
    for label in ("one response cannot assert asCapable",
                  "first peer delay matches independent event oracle within 28 ns"):
        outcomes.extend([
            (f"uncounted omission: {label}", f"NOT RUN: {label} (first exchange absent; uncounted)" in output),
            (f"no unexecuted pass: {label}",
             not any("[ ok ]" in line and label in line for line in output.splitlines())),
        ])
    for label, passed in outcomes:
        print(f"[{' ok ' if passed else 'FAIL'}] --no-pdelay-control: {label}")
    failures = sum(not passed for _, passed in outcomes)
    if failures:
        print(output)
    print(f"== ax1x1gptp no-Pdelay accounting: checks: {len(outcomes)}   failures: {failures} ==")
    return int(failures != 0)


if __name__ == "__main__":
    raise SystemExit(main())
