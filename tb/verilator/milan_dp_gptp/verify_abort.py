#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Require setup failures to omit unexecuted cumulative audio assertions."""

from pathlib import Path
import subprocess
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
            ("only the executed setup failure is counted", "checks: 1   failures: 1" in output and "[ ok ]" not in output),
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
    return int(failures != 0)


if __name__ == "__main__":
    raise SystemExit(main())
