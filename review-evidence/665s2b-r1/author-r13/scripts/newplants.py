#!/usr/bin/env python3
"""This round's new planted defects only, through each campaign's own planting and grading: the control campaign's
(THE STEP's loop plants and the platform's store bindings), the SRP campaign's (one build a pass, the reset's
listener_present) and the store's (THE STEP's room). A pre-check; the gates run every campaign whole.

usage: newplants.py CHECKOUT LWSRP WORK
"""
import sys
from pathlib import Path

checkout, lwsrp, work = (Path(a).resolve() for a in sys.argv[1:4])
ONLY = set(sys.argv[4].split(',')) if len(sys.argv) > 4 else None  # a named subset of the new plants
CTRL_NEW = {'step-binds-twice', 'step-binds-no-function', 'step-binds-no-clock', 'step-before-the-polls',
            'step-deadline-read-at-the-end', 'step-deadline-without-the-share', 'step-owed-lets-it-sleep', 'step-beside-input',
            'plat-store-tick-unbound', 'plat-store-step-unbound'}
SRP_NEW = {'joint-reset-builds-both', 'build-turn-ignored', 'build-turn-not-moved', 'build-waits-beside-a-withdrawal',
           'reset-keeps-listener-present'}
NVM_NEW = {'step_ignores_room', 'step_needs_more_room', 'step_owed_once_each', 'step_owed_lost_without_room',
           'step_not_owed_after_a_short_pass', 'step_untaken_when_not_owed'}

if ONLY:
    CTRL_NEW, SRP_NEW, NVM_NEW = CTRL_NEW & ONLY, SRP_NEW & ONLY, NVM_NEW & ONLY
sys.path.insert(0, str(checkout / 'sw/firmware/ctrl/test'))
sys.path.insert(0, str(checkout / 'sw/firmware/ctrl_nvm/test'))
sys.path.insert(0, str(checkout / 'sw/firmware/gtest'))
import ctrl_mutants  # noqa: E402
import srp_mutants  # noqa: E402
import fw_gtest  # noqa: E402
from ctrl_build import CTRL, Tree  # noqa: E402
from ctrl_reuse import cut_reuse  # noqa: E402

failed = False
ctrl_mutants.MUTANTS = tuple(m for m in ctrl_mutants.MUTANTS if m.name in CTRL_NEW)
assert {m.name for m in ctrl_mutants.MUTANTS} == CTRL_NEW, {m.name for m in ctrl_mutants.MUTANTS}
ctrl_mutants.unnamed_tests = lambda: []   # the whole table names every test; this run plants a part of it
tree = Tree(CTRL, work / 'checkout', work / 'reuse', fw_gtest.Build(jobs=4))
cut_reuse(tree.reuse)
failed = ctrl_mutants.campaign(work / 'mutants', tree.reuse, 4) or failed
srp_mutants.DEFECTS = tuple(d for d in srp_mutants.DEFECTS if d.name in SRP_NEW)
assert {d.name for d in srp_mutants.DEFECTS} == SRP_NEW
failed = srp_mutants.campaign(work / 'srp-mutants', lwsrp, 4) or failed
if not NVM_NEW:
    print(f'new plants: {"FAIL" if failed else "every one caught"}')
    sys.exit(1 if failed else 0)
import nvm_mutants  # noqa: E402
import test_ctrl_nvm  # noqa: E402
nvm_mutants.MUTANTS = tuple(m for m in nvm_mutants.MUTANTS if m.name in NVM_NEW)
assert {m.name for m in nvm_mutants.MUTANTS} == NVM_NEW
nvm_mutants.unnamed_checks = lambda names: []
found = test_ctrl_nvm.self_test({}, work / 'nvm', 4)
print('\n'.join(found) if found else f'store plants: {len(NVM_NEW)} of {len(NVM_NEW)} caught')
failed = failed or bool(found)
print(f'new plants: {"FAIL" if failed else "every one caught"}')
sys.exit(1 if failed else 0)
