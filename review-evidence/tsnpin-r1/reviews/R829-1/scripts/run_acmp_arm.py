# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Run the firmware's `acmp` GoogleTest arm (ctrl_arms.arm_acmp) on one checkout, unplanted, and print
its failing checks. Used for the P6 demonstration: a scratch copy of the head with a check added to
test_acmp_mbx.cpp, with and without P6 in acmp_mbx.c.

Usage: python3 -I run_acmp_arm.py <milan-fpga checkout> <empty work dir> [jobs]
"""

from __future__ import annotations

import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
work = Path(sys.argv[2]).resolve()
jobs = int(sys.argv[3]) if len(sys.argv) > 3 else 4
sys.path.insert(0, str(repo / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(repo / "sw/firmware/gtest"))

import ctrl_arms  # noqa: E402
import fw_gtest  # noqa: E402
from ctrl_build import CTRL, Tree, stack_pin  # noqa: E402
from ctrl_reuse import cut_reuse  # noqa: E402


def main() -> int:
    print(f"tree {CTRL}; tsn-c-stack at {stack_pin()}", flush=True)
    tree = Tree(CTRL, work / "checkout", work / "reuse", fw_gtest.Build(jobs=jobs))
    cut_reuse(tree.reuse)
    outcome = ctrl_arms.arm_acmp(tree)
    fails = [ln.strip() for ln in outcome.log.splitlines() if "[FAIL]" in ln]
    for ln in fails:
        print(ln)
    print(f"acmp arm rc {outcome.rc}: {len(fails)} failing check(s)")
    return outcome.rc


if __name__ == "__main__":
    sys.exit(main())
