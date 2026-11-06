#!/usr/bin/env python3
"""This round's planted defects of THE TRANSMIT (the loop's and SRP's) and the plants whose text moved, through the
control and SRP campaigns' own planting and grading. A pre-check; the gates run every campaign whole.

usage: newplants.py CHECKOUT WORK [NAME,...]
"""
import sys
from pathlib import Path

checkout, work = (Path(a).resolve() for a in sys.argv[1:3])
ONLY = set(sys.argv[3].split(',')) if len(sys.argv) > 3 else None
sys.path.insert(0, str(checkout / 'sw/firmware/ctrl/test'))
sys.path.insert(0, str(checkout / 'sw/firmware/gtest'))
import ctrl_mutants  # noqa: E402
import srp_mutants  # noqa: E402
import fw_gtest  # noqa: E402
from ctrl_build import CTRL, Tree  # noqa: E402
from ctrl_reuse import cut_reuse  # noqa: E402

CTRL_NEW = {m.name for m in ctrl_mutants.MUTANTS if m.name.startswith(('transmit-', 'tick-'))} | {
    'step-before-the-polls', 'retry-before-the-polls', 'retry-age-read-after-the-input', 'rx-pass-unbounded'}
SRP_NEW = {d.name for d in srp_mutants.DEFECTS if d.name.startswith('transmit-')} | {
    'short-leave', 'latency-leave-origin', 'walk-leave-shortened', 'reclaim-forgotten-while-owed',
    'srp-term-poll-frames-uncapped', 'failed-interface-starves-peer', 'latency-missing-startup'}
if ONLY:
    CTRL_NEW, SRP_NEW = CTRL_NEW & ONLY, SRP_NEW & ONLY
print('ctrl:', sorted(CTRL_NEW))
print('srp:', sorted(SRP_NEW), flush=True)
failed = False
if CTRL_NEW:
    ctrl_mutants.MUTANTS = tuple(m for m in ctrl_mutants.MUTANTS if m.name in CTRL_NEW)
    ctrl_mutants.unnamed_tests = lambda: []   # the whole table names every test; this run plants a part of it
    tree = Tree(CTRL, work / 'checkout', work / 'reuse', fw_gtest.Build(jobs=4))
    cut_reuse(tree.reuse)
    failed = ctrl_mutants.campaign(work / 'mutants', tree.reuse, 4) or failed
if SRP_NEW:
    srp_mutants.DEFECTS = tuple(d for d in srp_mutants.DEFECTS if d.name in SRP_NEW)
    for interfaces in (1, 2):
        failed = srp_mutants.campaign(work / f'srp-mutants-if{interfaces}', checkout / 'third_party/lwSRP', 4,
                                      interfaces) or failed
print(f'new plants: {"FAIL" if failed else "every one caught"}')
sys.exit(1 if failed else 0)
