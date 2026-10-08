#!/usr/bin/env python3
"""Run one SRP-arm GoogleTest suite of a (probe) tree at one interface count.

usage: run_arm.py TREE LWSRP OUT SUITE FILTER IFCOUNT [CTRL_SRC]
TREE is a checkout of the repository (the probe copy); the arm is imported
from TREE/sw/firmware/ctrl/test so test-file edits in the copy are compiled.
CTRL_SRC, when given, is a planted copy of sw/firmware/ctrl to build instead.
Prints the arm log and exits with the arm's rc (0 pass, 1 fail, 2 refusal).
"""
import sys
from pathlib import Path


def main() -> int:
    tree_root, lwsrp, out, suite, filt, ifs = sys.argv[1:7]
    test_dir = Path(tree_root).resolve() / "sw/firmware/ctrl/test"
    sys.path.insert(0, str(test_dir))
    sys.path.insert(0, str(Path(tree_root).resolve() / "sw/firmware/gtest"))
    import fw_gtest
    import srp_arms
    from ctrl_build import CTRL, Tree, Refusal
    out_path = Path(out).resolve()
    out_path.mkdir(parents=True, exist_ok=True)
    src = Path(sys.argv[7]).resolve() if len(sys.argv) > 7 else CTRL
    tree = Tree(src, out_path / "build", out_path / "reuse", fw_gtest.Build(jobs=4))
    try:
        outcome = srp_arms.arm_srp(tree, Path(lwsrp).resolve(), int(ifs), test=(suite, filt))
    except Refusal as error:
        print(f"REFUSAL: {error}")
        return 2
    print(outcome.log)
    print(f"ARM {outcome.arm} rc={outcome.rc}")
    return 1 if outcome.rc else 0


if __name__ == "__main__":
    sys.exit(main())
