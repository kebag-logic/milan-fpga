#!/usr/bin/env python3
"""Plant the loop-on defect plus AECP's reboot-probes-after-its-success (or either alone) and keep
platboot1's full log. usage: probe_combined_log.py <clone> <work-dir> <jobs> both|loop|probes <log>"""
import sys
from pathlib import Path

clone, work, jobs, which, log = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3]), sys.argv[4], Path(sys.argv[5])
sys.path.insert(0, str(clone / "sw/firmware/ctrl/test"))
import aecp_mutants  # noqa: E402
import ctrl_mutants  # noqa: E402
import fw_gtest  # noqa: E402
import plat_arms  # noqa: E402
from ctrl_build import Tree  # noqa: E402

loop_on = {m.name: m for m in ctrl_mutants.MUTANTS}["plat-reboot-transmits-after-the-departing"]
probes = {d.name: d for d in aecp_mutants.DEFECTS}["reboot-probes-after-its-success"]
noop = ctrl_mutants.Mutant("noop", loop_on.path, loop_on.old, loop_on.old, "", "", "")
ctrl, stack = ctrl_mutants.plant(loop_on if which in ("both", "loop") else noop, work)
if which in ("both", "probes"):
    target = ctrl / probes.path
    text = target.read_text(encoding="utf-8")
    assert text.count(probes.old) == 1
    target.write_text(text.replace(probes.old, probes.new), encoding="utf-8")
tree = Tree(ctrl, work / "work" / "build", work / "reuse", fw_gtest.Build(jobs=jobs), stack)
out = plat_arms.arm_platboot(tree, 1)
log.write_text(out.log)
print(which, "rc", out.rc, "fails", sum("[FAIL]" in ln for ln in out.log.splitlines()))
