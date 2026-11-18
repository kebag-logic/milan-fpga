#!/usr/bin/env python3
"""Reviewer-chosen disposable probes of the #946 platform code, planted through the
control campaign's own driver (ctrl_mutants.campaign) at the checkout given.
Each probe names the test it is expected to break; a probe the suites do not
catch prints [ESCAPED], which is the probe's finding (a test gap), not a gate.

Usage: python3 run_extra_probes.py <repo checkout> <output dir> [jobs]
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
import test_ctrl_firmware as gate  # noqa: E402
from ctrl_build import CTRL, Tree  # noqa: E402
from ctrl_mutant import Mutant  # noqa: E402

PLAT = "plat/ctrl_plat.c"
S2 = "Sinks.S2SetStreamFormatMovesOnlyThatContextAndABoundInputRefuses"
S5 = "Sinks.S5AChangeOfAnotherKindLeavesEveryContextInForce"
PROBES = (
    # R1: an immediate SET_STREAM_FORMAT write rewrites every context, not that input's alone
    Mutant("r867-change-writes-every-context", PLAT, "\t\tsink_write(index);\n\t} else {",
           "\t\tsink_write(SINK_ALL);\n\t} else {", "platsinks8", S2, "S2 that input's context alone is written"),
    # R2: the poll never clears what is owed, so it rewrites every context on every pass after the first change
    Mutant("r867-poll-never-clears-owed", PLAT, "\t\tsinks.owed = false;\n\t\tsink_write(SINK_ALL);\n\t}\n\treturn",
           "\t\tsink_write(SINK_ALL);\n\t}\n\treturn", "platsinks8", S5, "S5"),
    # R3: the poll writes what is owed on every pass once owed, from boot (the commit count never compared)
    Mutant("r867-poll-writes-every-pass", PLAT, "\tif (sinks.owed && p->face.commits != sinks.commits) {",
           "\tif (true) {", "platsinks8", S5, "S5"),
)
unnamed = ctrl_mutants.unnamed_tests()
ctrl_mutants.MUTANTS = PROBES
ctrl_mutants.unnamed_tests = lambda: unnamed
print(f"toolchain: {fw_gtest.toolchain()}")
tree = Tree(CTRL, out / "checkout", out / "reuse", fw_gtest.Build(jobs=jobs))
gate.cut_reuse(tree.reuse)
failed = ctrl_mutants.campaign(out / "mutants", tree.reuse, jobs)
print(f"extra probes: {'SOME ESCAPED' if failed else 'ALL CAUGHT'}")
sys.exit(0)
