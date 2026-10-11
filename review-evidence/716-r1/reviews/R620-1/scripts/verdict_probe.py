#!/usr/bin/env python3
"""Show that, at the reviewed head, one failing entry in each phase turns that shard's verdict red.

Usage: python3 -s -B verdict_probe.py TREE
Imports the driver from TREE/sw/firmware/ctrl/test, replaces every expensive
entry point with a stand-in (as the shard self-test does), makes exactly one
entry of the selected phase fail, and requires run_selected() to return True.
It also checks the all-passing control returns False for every shard.
"""
import sys
from contextlib import ExitStack, redirect_stdout
from io import StringIO
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

TEST = Path(sys.argv[1]).resolve() / "sw/firmware/ctrl/test"
sys.path.insert(0, str(TEST))
import test_ctrl_firmware as drv  # noqa: E402
from ctrl_build import Outcome, Tree  # noqa: E402

FAIL_POINTS = {0: "suite", 1: "control", 2: "aecp", 3: ("srp-if2", "srp-if1", "pin")}


def run(shard, fail):
    args = SimpleNamespace(shard=(shard, 4), self_test=True, jobs=4, slice=(1, 1), mutation_shard=None,
                           require_rv32=True, lwsrp=drv.CTRL.parents[2] / "third_party/lwSRP")
    tree = Tree(drv.CTRL, Path("v-build"), Path("v-reuse"), drv.fw_gtest.Build(jobs=4))
    seen = {"n": 0}

    def arm(name):
        def record(*a, **k):
            seen["n"] += 1
            # fail the LAST suite outcome only, so an early-exit cannot mask it
            return Outcome(name, 0, "")
        return record

    def report(outcomes):
        return fail == "suite"

    with ExitStack() as cx, redirect_stdout(StringIO()):
        for owner in (drv.ctrl_arms, drv.srp_arms, drv.aecp_arms):
            for name, value in vars(owner).copy().items():
                if callable(value) and (name.startswith("arm_") or name in ("core_arm", "image_arm")):
                    cx.enter_context(patch.object(owner, name, arm(name)))
        cx.enter_context(patch.object(drv.ctrl_arms, "report", report))
        cx.enter_context(patch.object(drv.ctrl_mutants, "campaign", lambda *a, **k: fail == "control"))
        cx.enter_context(patch.object(drv.aecp_mutants, "campaign", lambda *a, **k: fail == "aecp"))
        cx.enter_context(patch.object(drv.srp_mutants, "campaign",
                                      lambda root, lwsrp, jobs=4, interfaces=2: fail == f"srp-if{interfaces}"))
        cx.enter_context(patch.object(drv.ctrl_mutants, "lwsrp_pin_arms", lambda *a, **k: 1 if fail == "pin" else 0))
        return drv.run_selected(args, tree, Path("v-build"))


def main():
    bad = 0
    for shard, points in FAIL_POINTS.items():
        points = points if isinstance(points, tuple) else (points,)
        ok_clean = run(shard, None) is False
        print(f"{'PASS' if ok_clean else 'FAIL'}: shard {shard}/4 all-passing stand-ins -> verdict green")
        bad += not ok_clean
        for point in points:
            red = run(shard, point) is True
            print(f"{'PASS' if red else 'FAIL'}: shard {shard}/4 one failing {point} -> verdict red")
            bad += not red
    print("verdict_probe:", "PASS" if not bad else f"FAIL ({bad})")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
