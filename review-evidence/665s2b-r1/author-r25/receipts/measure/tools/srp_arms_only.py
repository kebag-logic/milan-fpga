#!/usr/bin/env python3
"""Scratch: build and run only the SRP gtest arms (both interface counts) of a firmware checkout.
usage: srp_arms_only.py CHECKOUT OUT [suite.cpp ...]"""
import sys
from pathlib import Path
ck, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
suites = sys.argv[3:] or ["srp_mbx.cpp", "srp_rx_retry.cpp", "srp_app.cpp", "test_acmp_mbx.cpp", "srp_latency.cpp",
                          "srp_walk.cpp"]
sys.path.insert(0, str(ck / "sw/firmware/ctrl/test")); sys.path.insert(0, str(ck / "sw/firmware/gtest"))
import fw_gtest, srp_arms
from ctrl_build import Tree, CTRL
tree = Tree(CTRL, out / "checkout", out / "reuse", fw_gtest.Build(jobs=4))
bad = 0
for i in (1, 2):
    for s in suites:
        o = srp_arms.arm_srp(tree, (ck / "third_party/lwSRP").resolve(), i, test=s)
        fails = sorted({l for l in o.log.splitlines() if l.startswith('[  FAILED  ]') and '(' in l})
        print(f"{o.arm}: rc={o.rc} {'; '.join(fails)}", flush=True)
        bad |= o.rc
sys.exit(bad)
