#!/usr/bin/env python3
"""Reviewer probe (R603-2): the base firmware (the PR's source base) graded by
the head's checks 13 and 14, every case, no early stop. Non-vacuity of the
checks against the defect #671 reports.

Usage: probe_base_firmware.py REPO_ROOT BASE_SHA [--shape S] [--jobs N]
Prints the finding count, the count naming the clean-reboot loss, and the
first few findings.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from dataclasses import replace
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("base")
    ap.add_argument("--shape", default="endstation_ax7101_1x1_tdm8")
    ap.add_argument("--jobs", type=int, default=6)
    a = ap.parse_args()
    root = Path(a.root).resolve()
    sys.path.insert(0, str(root / "sw/firmware/nvm_hosttest"))
    import test_nvm_firmware as t  # noqa: E402

    base_text = subprocess.run(["git", "-C", str(root), "show",
                                f"{a.base}:sw/firmware/milan_baremetal/milan_baremetal.c"],
                               capture_output=True, text=True, check=True).stdout
    with tempfile.TemporaryDirectory(prefix="r603base.") as tmp:
        bench = replace(t.make_bench(root / "configs" / f"{a.shape}.yaml", Path(tmp), base_text),
                        jobs=a.jobs)
        got = t.grade_refused_generation(bench) + t.grade_read_faults(bench)
    lost = [x for x in got if "was lost on the clean reboot" in x]
    print(f"base {a.base} on {a.shape}: {len(got)} finding(s), {len(lost)} naming "
          f"'was lost on the clean reboot'")
    for x in got[:3] + lost[:3]:
        print("  " + x[:300])
    return 0


if __name__ == "__main__":
    sys.exit(main())
