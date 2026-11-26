#!/usr/bin/env python3
"""Reviewer probe: the parent ADP adapter arm at the head, then the five ADP
length plants of the PR plus reviewer-written plants, through the firmware
gate's own campaign machinery (no source of the clone is modified; every plant
is written into the campaign's disposable copy).

usage: fw_adp_probe.py <repo> <work-dir>
"""

from __future__ import annotations

import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
work = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(repo / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(repo / "sw/firmware/gtest"))

import ctrl_arms  # noqa: E402
import ctrl_mutants  # noqa: E402
import fw_gtest  # noqa: E402
from ctrl_build import CTRL, Tree, stack_pin  # noqa: E402
from ctrl_mutant import ADP_C, Mutant  # noqa: E402
from ctrl_reuse import cut_reuse  # noqa: E402

CDL = ctrl_mutants.CDL_BOUND
LONG = "AdpAdapter.PinAcceptsLongDiscoveryThroughMailbox"
SHORT = "AdpAdapter.PinRejectsShortDiscoveryControlLength"
LEN_GUARD = "if (len < ADP_FRAME_BYTES ||"

# Reviewer plants: plausible wrong readings of "read by its first 56 octets".
EXTRA = (
    # require the whole declared PDU to be present (a truncated frame refused)
    Mutant("r937-require-whole-pdu", ADP_C, LEN_GUARD,
           "if (len < ADP_FRAME_BYTES || len < 26u + (wire_be16(frame + ADP_HEADER_BYTES + 2u) & 0x07FFu) ||",
           "adp", LONG, "a longer discovery restarts advertising through the mailbox"),
    # an upper bound at the channel's largest frame (102 octets of control data)
    Mutant("r937-upper-bound-102", ADP_C, CDL,
           CDL + " (wire_be16(frame + ADP_HEADER_BYTES + 2u) & 0x07FFu) > 102u ||",
           "adp", LONG, "a longer discovery restarts advertising through the mailbox"),
    # an upper bound just below the 11-bit maximum
    Mutant("r937-upper-bound-2046", ADP_C, CDL,
           CDL + " (wire_be16(frame + ADP_HEADER_BYTES + 2u) & 0x07FFu) > 2046u ||",
           "adp", LONG, "a longer discovery restarts advertising through the mailbox"),
    # the bound off by one the other way: 55 accepted
    Mutant("r937-bound-55", ADP_C, CDL, CDL.replace("< ADP_CONTROL_DATA_LENGTH", "< 55u"),
           "adp", SHORT, "malformed discovery changes only the discard count"),
)


def main() -> int:
    print(f"toolchain: {fw_gtest.toolchain()}")
    tree = Tree(CTRL, work / "checkout", work / "reuse", fw_gtest.Build(jobs=4))
    print(f"tsn-c-stack at {stack_pin()}")
    cut_reuse(tree.reuse)
    outcome = ctrl_arms.arm_adp(tree)
    lines = [ln for ln in outcome.log.splitlines()
             if "Discovery" in ln and ("[       OK ]" in ln or "[  FAILED  ]" in ln)]
    print("\n".join(lines))
    tally = [ln for ln in outcome.log.splitlines() if "PASSED" in ln or "FAILED" in ln and "tests" in ln]
    print("\n".join(tally[-3:]))
    print(f"clean adp arm rc={outcome.rc}")
    if outcome.rc != 0:
        return 1
    table = tuple(m for m in ctrl_mutants.MUTANTS
                  if m.name in ("pin-adp-discovery-length", "pin-adp-discovery-valid-time",
                                "pin-adp-discovery-length-octet", "pin-adp-long-discovery",
                                "pin-adp-valid-discovery")) + EXTRA
    assert len(table) == 9, [m.name for m in table]
    ctrl_mutants.MUTANTS = table
    ctrl_mutants.unnamed_tests = lambda: []  # this probe plants a subset only
    escaped = ctrl_mutants.campaign(work / "mutants", tree.reuse, 4)
    print(f"probe campaign escaped={escaped}")
    return 1 if escaped else 0


if __name__ == "__main__":
    sys.exit(main())
