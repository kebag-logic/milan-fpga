# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Run slice K of N of the firmware's control or AECP mutation phase, the calls test_ctrl_firmware.py's
run_selected makes for that phase, with the table partition the drivers already offer
(ctrl_mutants.campaign's shard, aecp_mutants.campaign's shard). The union of slices 0..N-1 is the phase.

Usage: python3 -I phase_slice.py <milan-fpga checkout> <empty work dir> control|aecp K N [jobs]
"""

from __future__ import annotations

import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
work = Path(sys.argv[2]).resolve()
phase, k, n = sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
jobs = int(sys.argv[6]) if len(sys.argv) > 6 else 4
sys.path.insert(0, str(repo / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(repo / "sw/firmware/gtest"))

import aecp_mutants  # noqa: E402
import ctrl_mutants  # noqa: E402
import fw_gtest  # noqa: E402
from ctrl_build import CTRL, Tree, stack_pin  # noqa: E402
from ctrl_reuse import cut_reuse  # noqa: E402


def main() -> int:
    print(f"tsn-c-stack at {stack_pin()}", flush=True)
    tree = Tree(CTRL, work / "checkout", work / "reuse", fw_gtest.Build(jobs=jobs))
    cut_reuse(tree.reuse)
    if phase == "control":
        print(f"control slice {k}/{n}: {len(ctrl_mutants.MUTANTS[k::n])} of {len(ctrl_mutants.MUTANTS)}", flush=True)
        failed = ctrl_mutants.campaign(work / "mutants", tree.reuse, jobs, (1, 1), [k, n])
    elif phase == "aecp":
        failed = aecp_mutants.campaign(work / "aecp-mutants", jobs, (k, n))
    else:
        raise SystemExit(f"unknown phase {phase!r}")
    print(f"phase_slice {phase} {k}/{n}: {'FAIL' if failed else 'PASS'}", flush=True)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
