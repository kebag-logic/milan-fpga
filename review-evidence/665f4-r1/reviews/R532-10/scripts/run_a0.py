#!/usr/bin/env python3
# Reused verbatim from the round-9 packet of this reviewer (665f4-r532-9-packet/scripts).
"""Build and run the ACMP core suite (test_acmp.cpp) of a ctrl tree copy.

usage: run_a0.py REPO CTRL_SRC OUT [asan]
CC/CXX in the environment choose the compilers. A plant is applied to the
copy beforehand (plant_a0.py). Prints the run log and the A0 lines.
"""
import sys
from pathlib import Path


def main() -> int:
    repo, src, out = (Path(a).resolve() for a in sys.argv[1:4])
    asan = len(sys.argv) > 4 and sys.argv[4] == "asan"
    sys.path.insert(0, str(repo / "sw/firmware/ctrl/test"))
    sys.path.insert(0, str(repo / "sw/firmware/gtest"))
    import fw_gtest
    from ctrl_build import Tree, compile_c, compile_tests, link, execute, sources, PORTABLE, HOST, Refusal
    from ctrl_arms import REENTRY_ASSERT
    tree = Tree(src, out, out / "reuse", fw_gtest.Build(address_sanitizer=asan, jobs=4))
    try:
        objs = (compile_c(tree, sources(tree, PORTABLE), "acmp", REENTRY_ASSERT) +
                compile_c(tree, sources(tree, HOST), "acmp/host", measured=False) +
                compile_tests(tree, ("test_acmp.cpp",), "acmp/tests"))
        outcome = execute("acmp", link(tree, "test_acmp", objs))
    except Refusal as error:
        print(f"REFUSAL: {error}")
        return 2
    print(outcome.log)
    print(f"ARM rc={outcome.rc}")
    return 1 if outcome.rc else 0


if __name__ == "__main__":
    sys.exit(main())
