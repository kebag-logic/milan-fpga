#!/usr/bin/env python3
"""Run the SRP adapter's srp_mbx.cpp arms (1x1 and 8x8 entity, one and two interfaces) and the platsinks arms
(8x8/1if, 1x1/1if) of a milan-fpga tree, each graded by its own GoogleTest tally.

Usage: python3 -I arms.py <repo-root> <out-dir> [filter]
  filter: a GoogleTest filter applied to every arm (default '*').
Prints one line per arm: name, rc, the [  FAILED  ] lines; exit 0 when every arm passed.
"""
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2]).resolve()
flt = sys.argv[3] if len(sys.argv) > 3 else "*"
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(root / "sw/firmware/gtest"))

import ctrl_arms  # noqa: E402
import fw_gtest  # noqa: E402
import plat_arms  # noqa: E402
import srp_arms  # noqa: E402
from ctrl_build import CTRL, Refusal, Tree, stack_pin  # noqa: E402
from ctrl_reuse import cut_reuse  # noqa: E402

assert CTRL.resolve().is_relative_to(root), (CTRL, root)
lwsrp = root / "third_party/lwSRP"
out.mkdir(parents=True, exist_ok=True)
tree = Tree(CTRL, out / "checkout", out / "reuse", fw_gtest.Build(jobs=4))
print("tsn-c-stack", stack_pin())
cut_reuse(tree.reuse)
E8 = root / "configs/endstation_ax7101_8x8.yaml"
outcomes = []
for i in (() if flt.startswith(("Early.", "Sinks.")) else (1, 2)):  # a platform-only filter runs platsinks alone
    outcomes.append(srp_arms.arm_srp(tree, lwsrp, i, test=("srp_mbx.cpp", flt)))
    outcomes.append(srp_arms.arm_srp(tree, lwsrp, i, test=("srp_mbx.cpp", flt), config=E8))
if flt == "*" or flt.startswith(("Early.", "Sinks.")):
    real = fw_gtest.run_binary
    if flt != "*":
        def run_binary(exe, args=(), cwd=None, env=None, _real=real):
            return _real(exe, [a for a in args if not a.startswith("--gtest_filter")] + [f"--gtest_filter={flt}"],
                         cwd=cwd, env=env)
        fw_gtest.run_binary = run_binary
    try:
        outcomes.extend(plat_arms.sink_arms(tree))
    finally:
        fw_gtest.run_binary = real
bad = 0
for idx, o in enumerate(outcomes):
    fails = [ln for ln in o.log.splitlines() if "[  FAILED  ]" in ln or "[  PASSED  ]" in ln]
    print(f"ARM {idx}:{o.arm} rc={o.rc}")
    for ln in fails:
        print("   ", ln)
    (out / f"{idx:02d}-{o.arm}.log").write_text(o.log, encoding="utf-8")
    bad |= o.rc != 0
print("ALL-PASS" if not bad else "SOME-FAIL")
sys.exit(1 if bad else 0)
