#!/usr/bin/env python3
"""Run the parent's adp arm on the checkout, then its ADP input plants and extra mask plants.
Usage: consumer_adp.py PARENT_CHECKOUT WORK"""
import sys
from pathlib import Path
parent, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
for d in ("sw/firmware/ctrl/test", "sw/firmware/gtest", "scripts", "sw/tooling"):
    sys.path.insert(0, str(parent / d))
import ctrl_arms, ctrl_mutants, fw_gtest
from ctrl_build import CTRL, Tree, stack_pin
from ctrl_mutant import Mutant, ADP_C
work.mkdir(parents=True, exist_ok=True)
print("tsn-c-stack at", stack_pin())
tree = Tree(CTRL, work / "build", work / "reuse", fw_gtest.Build(jobs=4))
out = ctrl_arms.arm_adp(tree)
print("adp arm rc", out.rc, [l for l in out.log.splitlines() if "checks:" in l or "RESULT" in l])
if len(sys.argv) > 3:
    F = "(wire_be16(frame + ADP_HEADER_BYTES + 2u) & 0x07FFu) < ADP_CONTROL_DATA_LENGTH ||"
    T = "AdpAdapter.PinAcceptsLongDiscoveryThroughMailbox"
    sel = [m for m in ctrl_mutants.MUTANTS if m.name.startswith("pin-adp-") or m.name in ("foreign-discover-answered",)]
    extra = [Mutant("extra-mask-0x00FF", ADP_C, F, F.replace("0x07FFu", "0x00FFu"), "adp", T, "a longer discovery restarts advertising through the mailbox"),
             Mutant("extra-mask-0x003F", ADP_C, F, F.replace("0x07FFu", "0x003Fu"), "adp", T, "a longer discovery restarts advertising through the mailbox")]
    ctrl_mutants.MUTANTS = tuple(sel + extra)
    ctrl_mutants.unnamed_tests = lambda: []
    ctrl_mutants.campaign(work / "mut", work / "reuse", 4)
