#!/usr/bin/env python3
"""Plant only the #946 sink defects (sink_mutants.py's table) through the control
campaign's own driver (ctrl_mutants.campaign), at the checkout given.

Usage: python3 run_sink_campaign.py <repo checkout> <output dir> [jobs]
Exit 0 when every planted defect was caught by its named test on its own words
and every test of the sink suites is named by some defect of the full table.
"""
import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2]).resolve()
jobs = int(sys.argv[3]) if len(sys.argv) > 3 else 4
sys.path.insert(0, str(repo / "sw/firmware/gtest"))
sys.path.insert(0, str(repo / "sw/firmware/ctrl/test"))

import ctrl_mutants  # noqa: E402
import fw_gtest  # noqa: E402
import sink_mutants  # noqa: E402
import test_ctrl_firmware as gate  # noqa: E402
from ctrl_build import CTRL, Tree  # noqa: E402
from ctrl_mutant import Mutant  # noqa: E402

# every test named by the FULL table (the campaign's own completeness check), computed before narrowing
unnamed = ctrl_mutants.unnamed_tests()
print(f"tests named by no defect of the full table: {len(unnamed)} {unnamed}")
sink_names = {m.name for m in sink_mutants.mutants(Mutant)}
print(f"sink table: {len(sink_names)} defects")
full = ctrl_mutants.MUTANTS
ctrl_mutants.MUTANTS = tuple(m for m in full if m.name in sink_names)
assert len(ctrl_mutants.MUTANTS) == len(sink_names), "every sink defect is in the campaign's table"
ctrl_mutants.unnamed_tests = lambda: unnamed
print(f"toolchain: {fw_gtest.toolchain()}")
tree = Tree(CTRL, out / "checkout", out / "reuse", fw_gtest.Build(jobs=jobs))
gate.cut_reuse(tree.reuse)
failed = ctrl_mutants.campaign(out / "mutants", tree.reuse, jobs)
print(f"sink campaign: {'FAIL' if failed else 'PASS'}")
sys.exit(1 if failed else 0)
