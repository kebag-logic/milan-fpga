#!/usr/bin/env python3
"""The platform's host arms, or a selection of the control campaign's defects, from a checkout, every build under
WORK (outside the checkout). Lane helper, not part of the tree.

usage: plat_quick.py CHECKOUT WORK arms
       plat_quick.py CHECKOUT WORK mutants NAME...
       plat_quick.py CHECKOUT WORK plants FILE   (FILE: a JSON list of [name, path, old, new, arm, test, needle])
"""
import json
import sys
from pathlib import Path

checkout = Path(sys.argv[1]).resolve()
work = Path(sys.argv[2]).resolve()
mode = sys.argv[3]
sys.path.insert(0, str(checkout / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(checkout / "sw/firmware/gtest"))

import ctrl_mutants  # noqa: E402
import fw_gtest  # noqa: E402
import plat_arms  # noqa: E402
from ctrl_build import CTRL, Tree  # noqa: E402
from ctrl_mutant import Mutant  # noqa: E402
from ctrl_reuse import cut_reuse  # noqa: E402

work.mkdir(parents=True, exist_ok=True)
reuse = work / "reuse"
cut_reuse(reuse)
if mode == "arms":
    tree = Tree(CTRL, work / "checkout", reuse, fw_gtest.Build(jobs=4))
    rc = 0
    for outcome in (plat_arms.arm_plat(tree), plat_arms.arm_platboot(tree, 1), plat_arms.arm_platboot(tree, 2)):
        print(f"==== arm {outcome.arm}: rc {outcome.rc}")
        print(outcome.log)
        rc = max(rc, outcome.rc)
    print(f"plat_quick arms: rc {rc}")
    raise SystemExit(rc)
if mode == "armlog":
    # one defect planted as the campaign plants it, and its arm's whole log
    m = next(m for m in ctrl_mutants.MUTANTS if m.name == sys.argv[4])
    ctrl, stack = ctrl_mutants.plant(m, work / "planted")
    arm = {"plat": plat_arms.arm_plat, "platboot1": lambda t: plat_arms.arm_platboot(t, 1)}[m.arm]
    outcome = arm(Tree(ctrl, work / "planted" / "work" / "build", reuse, fw_gtest.Build(jobs=4), stack))
    print(outcome.log)
    print(f"plat_quick armlog {m.name}: arm {m.arm} rc {outcome.rc}; caught {ctrl_mutants.caught(m.test, m.needle, outcome)}")
    raise SystemExit(0 if ctrl_mutants.caught(m.test, m.needle, outcome) else 1)
if mode == "noasan":
    # the same defects with the plat arm's sanitizer withheld: what the sanitizer alone catches escapes here
    import types
    real = plat_arms.dataclasses.replace
    plat_arms.dataclasses = types.SimpleNamespace(
        replace=lambda obj, **kw: obj if "address_sanitizer" in kw else real(obj, **kw))
if mode in ("mutants", "noasan"):
    table = tuple(m for m in ctrl_mutants.MUTANTS if m.name in set(sys.argv[4:]))
    assert len(table) == len(sys.argv[4:]), [m.name for m in table]
else:
    table = tuple(Mutant(*row) for row in json.loads(Path(sys.argv[4]).read_text()))
ctrl_mutants.MUTANTS = table
ctrl_mutants.NAMED_SOURCES = ()
failed = ctrl_mutants.campaign(work / "mutants", reuse, 4)
print(f"plat_quick {mode}: {'SOME ESCAPED' if failed else 'ALL CAUGHT'}")
raise SystemExit(1 if failed else 0)
