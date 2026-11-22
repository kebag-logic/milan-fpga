#!/usr/bin/env python3
"""Run every SRP GoogleTest arm the firmware gate's normal suites run (test_ctrl_firmware.run_suites' SRP part, debug
arms excepted) on a milan-fpga tree, each graded by its own tally.

Usage: python3 -I allsrp.py <repo-root> <out-dir>
"""
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(root / "sw/firmware/gtest"))
import fw_gtest  # noqa: E402
import srp_arms  # noqa: E402
from ctrl_build import CTRL, Tree, stack_pin  # noqa: E402
from ctrl_reuse import cut_reuse  # noqa: E402

assert CTRL.resolve().is_relative_to(root), (CTRL, root)
lw = root / "third_party/lwSRP"
out.mkdir(parents=True, exist_ok=True)
tree = Tree(CTRL, out / "checkout", out / "reuse", fw_gtest.Build(jobs=4))
print("tsn-c-stack", stack_pin())
cut_reuse(tree.reuse)
outcomes = []
for i in (1, 2):
    outcomes.append(srp_arms.arm_srp(tree, lw, i))
    for suite in ("srp_rx_retry.cpp", "srp_app.cpp", "test_acmp_mbx.cpp", "srp_latency.cpp", "srp_walk.cpp"):
        outcomes.append(srp_arms.arm_srp(tree, lw, i, test=suite))
outcomes.extend(srp_arms.talker_arms(tree, lw))
outcomes.extend(srp_arms.listener_arms(tree, lw))
outcomes.extend(srp_arms.mbx_entity_arms(tree, lw))
bad = 0
for idx, o in enumerate(outcomes):
    print(f"ARM {idx}:{o.arm} rc={o.rc}")
    (out / f"{idx:02d}-{o.arm}.log").write_text(o.log, encoding="utf-8")
    bad |= o.rc != 0
print("ALL-PASS" if not bad else "SOME-FAIL")
sys.exit(1 if bad else 0)
