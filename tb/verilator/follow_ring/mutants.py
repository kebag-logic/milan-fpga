#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""follow_ring's mutation arm: each planted defect must fail its named check.

  mutants.py [--mdir DIR]

W1: a switch between two followed sources passes servo IDLE (the design's
rejected W1, MEDIA_CLOCK_FOLLOWING.md "Switching sources"), so the trim
restarts from the bare MMCM plan and the DUT reads 5.92 ppm fast again while
the servo re-acquires. The b8 leg sets AAF where the loopback ring is left
within a tenth of a tick of its empty edge, so that re-acquisition must slip
the ring at the AAF-to-CRF switch: "[SW] no ring slip across the AAF to CRF
switch" must fail. The clean build runs the same leg in `make b8` and passes.

The mutant is a compile-time define (FR_MUT_W1) on a copy of the build, never
an edit of a tracked file. Exit 0 = every mutant killed by its named check.
"""

import argparse
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

#: (define, the leg's arguments, the check that must fail)
MUTANTS = (
    ("FR_MUT_W1",
     ["--case", "b8", "--dwell-s", "1.0", "--set-phase", "0.5", "--hold-s", "10",
      "--switch-hold-s", "8"],
     "[SW] no ring slip across the AAF to CRF switch"),
)


def main() -> int:
    """Build each mutant through the suite's own recipe and require its failure."""
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--mdir", type=Path, default=HERE / "obj_mut")
    a = ap.parse_args()
    survivors = 0
    for define, leg, check in MUTANTS:
        mdir = a.mdir / define.lower()
        build = subprocess.run(["make", "-s", "--no-print-directory", "-C", str(HERE), "build",
                                f"MDIR={mdir}", f"MUT_DEFS=+define+{define}"], check=False)
        if build.returncode != 0:
            print(f"[MUTANT] {define}: did not build (rc {build.returncode})")
            survivors += 1
            continue
        run = subprocess.run([str(mdir / "Vfollow_ring"), *leg], capture_output=True, text=True, check=False)
        killed = run.returncode != 0 and f"[FAIL] {check}" in run.stdout
        print(f"[MUTANT] {define}: {'caught' if killed else 'SURVIVED'} by \"{check}\" (rc {run.returncode})")
        if not killed:
            print(run.stdout)
            survivors += 1
    print(f"follow_ring mutants: {len(MUTANTS) - survivors}/{len(MUTANTS)} caught")
    return 0 if survivors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
