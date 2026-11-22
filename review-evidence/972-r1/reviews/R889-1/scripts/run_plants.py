#!/usr/bin/env python3
"""run_plants.py ROOT WORK NAME... - plant each named defect of the tree's own control campaign table
(ctrl_mutants.MUTANTS) into a copy under WORK, with the campaign's own plant(), build each arm its kills name and
report whether every kill (arm, test, words) is caught by the campaign's own caught(). One line per kill."""
import sys
from pathlib import Path

root, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
import ctrl_arms, plat_arms, ctrl_mutants, fw_gtest  # noqa: E402
from ctrl_build import Tree  # noqa: E402

ARMS = {"adp": ctrl_arms.arm_adp,
        "platboot1": lambda t: plat_arms.arm_platboot(t, 1), "platboot2": lambda t: plat_arms.arm_platboot(t, 2)}
table = {m.name: m for m in ctrl_mutants.MUTANTS}
bad = 0
for name in sys.argv[3:]:
    m = table[name]
    w = work / name
    ctrl, stack = ctrl_mutants.plant(m, w)
    tree = Tree(ctrl, w / "build", w / "reuse", fw_gtest.Build(jobs=4), stack)
    outs = {}
    for arm, test, words in m.kills():
        if arm not in ARMS:
            print(f"SKIPPED {name} {arm} {test} :: {words} (arm not run by this driver)", flush=True)
            continue
        if arm not in outs:
            outs[arm] = ARMS[arm](tree)
            (w / f"{arm}.log").write_text(outs[arm].log)
        ok = ctrl_mutants.caught(test, words, outs[arm])
        bad += not ok
        print(f"{'CAUGHT ' if ok else 'ESCAPED'} {name} {arm} {test} :: {words}", flush=True)
sys.exit(1 if bad else 0)
