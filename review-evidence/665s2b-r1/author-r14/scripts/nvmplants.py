#!/usr/bin/env python3
"""The store's suite with only the named planted defects, through its own planting and grading (a pre-check; the
gate plants every one). usage: nvmplants.py CHECKOUT WORK NAME,..."""
import sys
from pathlib import Path

checkout, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
names = set(sys.argv[3].split(','))
sys.path.insert(0, str(checkout / 'sw/firmware/ctrl_nvm/test'))
sys.path.insert(0, str(checkout / 'sw/firmware/gtest'))
import nvm_mutants  # noqa: E402
import test_ctrl_nvm  # noqa: E402
nvm_mutants.MUTANTS = tuple(m for m in nvm_mutants.MUTANTS if m.name in names)
assert {m.name for m in nvm_mutants.MUTANTS} == names
nvm_mutants.unnamed_checks = lambda names: []
found = test_ctrl_nvm.self_test({}, work / 'nvm', 4)
print('\n'.join(found) if found else f'store plants: {len(names)} of {len(names)} caught')
sys.exit(1 if found else 0)
