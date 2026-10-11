#!/usr/bin/env python3
"""Run one tree's srp_latency arm at one and two interfaces against one lwSRP checkout.

usage: latency_arm.py TREE OUT LWSRP [SUITE]

TREE is a milan-fpga checkout; its own sw/firmware/ctrl/test drivers (and so its
own lwSRP pin check) are imported. OUT receives the builds. Exit 0 only when
every arm passed; each arm's verdict line and log are printed.
"""
import sys
from pathlib import Path


def main() -> int:
    tree_root, out, lwsrp = (Path(a).resolve() for a in sys.argv[1:4])
    suite = sys.argv[4] if len(sys.argv) > 4 else "srp_latency.cpp"
    sys.path.insert(0, str(tree_root / "sw/firmware/ctrl/test"))
    from ctrl_build import CTRL, Tree  # noqa: E402  (also puts sw/firmware/gtest on the path)
    import fw_gtest  # noqa: E402
    import srp_arms  # noqa: E402
    assert CTRL.resolve() == (tree_root / "sw/firmware/ctrl").resolve(), CTRL
    out.mkdir(parents=True, exist_ok=True)
    tree = Tree(CTRL, out / "checkout", out / "reuse", fw_gtest.Build(jobs=4))
    failed = 0
    for interfaces in (1, 2):
        o = srp_arms.arm_srp(tree, lwsrp, interfaces, test=suite)
        print(f"[{'ok' if o.rc == 0 else 'FAIL'}] arm {o.arm}")
        print(o.log)
        failed |= o.rc != 0
    print(f"latency_arm: {'FAIL' if failed else 'PASS'}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
