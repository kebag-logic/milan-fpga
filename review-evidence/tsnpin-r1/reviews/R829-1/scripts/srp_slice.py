# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Run slice K of N of the firmware's SRP mutation campaigns, as test_ctrl_firmware.py's srp phase
runs them whole (run_srp_mutants): the two-interface table, then the one-interface subset, and on
slice 0 the lwSRP pin refusals. The union of slices 0..N-1 is the whole phase.

Usage: python3 -I srp_slice.py <milan-fpga checkout> <empty work dir> K N [jobs]
"""

from __future__ import annotations

import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
work = Path(sys.argv[2]).resolve()
k, n = int(sys.argv[3]), int(sys.argv[4])
jobs = int(sys.argv[5]) if len(sys.argv) > 5 else 4
sys.path.insert(0, str(repo / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(repo / "sw/firmware/gtest"))

import ctrl_mutants  # noqa: E402
import srp_mutants  # noqa: E402
import srp_pub_mutants  # noqa: E402
from ctrl_build import stack_pin  # noqa: E402

# The one-interface subset, exactly as test_ctrl_firmware.run_srp_mutants selects it.
IF1_PREFIXES = ("four-way-", "binding-", "feedback-", "r10-", "p11-", "srp-bound-", "srp-term-",
                "srp-poll-extra", "srp-send-extra", *srp_pub_mutants.ROUND5)


def main() -> int:
    lwsrp = (repo / "third_party/lwSRP").resolve()
    print(f"tsn-c-stack at {stack_pin()}", flush=True)
    full = srp_mutants.DEFECTS
    if1 = tuple(d for d in full if d.name.startswith(IF1_PREFIXES))
    srp_mutants.DEFECTS = full[k::n]
    print(f"slice {k}/{n}: {len(srp_mutants.DEFECTS)} of {len(full)} two-interface defects", flush=True)
    failed = srp_mutants.campaign(work / "srp-mutants", lwsrp, jobs)
    srp_mutants.DEFECTS = if1[k::n]
    print(f"slice {k}/{n}: {len(srp_mutants.DEFECTS)} of {len(if1)} one-interface defects", flush=True)
    failed = srp_mutants.campaign(work / "srp-if1-mutants", lwsrp, jobs, 1) or failed
    if k == 0:
        failed = ctrl_mutants.lwsrp_pin_arms(work / "mutants", lwsrp) != 0 or failed
    print(f"srp_slice {k}/{n}: {'FAIL' if failed else 'PASS'}", flush=True)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
