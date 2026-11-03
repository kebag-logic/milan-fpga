#!/usr/bin/env python3
"""This round's new and re-anchored planted defects only, through each campaign's own planting and grading: the
control campaign's (THE STEP's loop plants, its age limit among them) and the SRP campaign's (one build a pass in
both orientations). A pre-check; the gates run every campaign whole.

usage: newplants.py CHECKOUT LWSRP WORK [NAME,...]
"""
import sys
from pathlib import Path

checkout, lwsrp, work = (Path(a).resolve() for a in sys.argv[1:4])
ONLY = set(sys.argv[4].split(',')) if len(sys.argv) > 4 else None
CTRL_NEW = {'step-before-the-polls', 'step-deadline-read-at-the-end', 'step-deadline-without-the-share',
            'step-owed-lets-it-sleep', 'step-beside-input', 'step-age-uncounted', 'step-age-ignored',
            'step-age-at-the-limit', 'step-aged-pass-takes-input', 'step-aged-pass-sleeps',
            'step-aged-deadline-not-read', 'step-aged-pass-uncounted', 'step-age-kept-by-its-pass',
            'step-age-kept-after-a-step', 'step-age-reset-on-deferral'}
SRP_NEW = {'joint-reset-builds-both', 'build-turn-ignored', 'build-turn-not-moved', 'build-waits-beside-a-withdrawal', 'srp-poll-extra-read',
           'build-turn-read-after-its-visit'}
if ONLY:
    CTRL_NEW, SRP_NEW = CTRL_NEW & ONLY, SRP_NEW & ONLY
sys.path.insert(0, str(checkout / 'sw/firmware/ctrl/test'))
sys.path.insert(0, str(checkout / 'sw/firmware/gtest'))
import ctrl_mutants  # noqa: E402
import srp_mutants  # noqa: E402
import fw_gtest  # noqa: E402
from ctrl_build import CTRL, Tree  # noqa: E402
from ctrl_reuse import cut_reuse  # noqa: E402

failed = False
if CTRL_NEW:
    ctrl_mutants.MUTANTS = tuple(m for m in ctrl_mutants.MUTANTS if m.name in CTRL_NEW)
    assert {m.name for m in ctrl_mutants.MUTANTS} == CTRL_NEW, {m.name for m in ctrl_mutants.MUTANTS}
    ctrl_mutants.unnamed_tests = lambda: []   # the whole table names every test; this run plants a part of it
    tree = Tree(CTRL, work / 'checkout', work / 'reuse', fw_gtest.Build(jobs=4))
    cut_reuse(tree.reuse)
    failed = ctrl_mutants.campaign(work / 'mutants', tree.reuse, 4) or failed
if SRP_NEW:
    srp_mutants.DEFECTS = tuple(d for d in srp_mutants.DEFECTS if d.name in SRP_NEW)
    assert {d.name for d in srp_mutants.DEFECTS} == SRP_NEW
    failed = srp_mutants.campaign(work / 'srp-mutants', lwsrp, 4) or failed
print(f'new plants: {"FAIL" if failed else "every one caught"}')
sys.exit(1 if failed else 0)
