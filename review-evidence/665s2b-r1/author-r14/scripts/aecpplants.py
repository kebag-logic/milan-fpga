#!/usr/bin/env python3
"""The AECP campaign with only the named planted defects (a pre-check; the gate plants every one).
usage: aecpplants.py CHECKOUT WORK NAME,..."""
import sys
from pathlib import Path

checkout, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
names = set(sys.argv[3].split(','))
sys.path.insert(0, str(checkout / 'sw/firmware/ctrl/test'))
sys.path.insert(0, str(checkout / 'sw/firmware/gtest'))
import aecp_mutants  # noqa: E402
aecp_mutants.DEFECTS = tuple(d for d in aecp_mutants.DEFECTS if d.name in names)
aecp_mutants.controls = lambda: None   # the whole table claims every test; this run plants a part of it
assert {d.name for d in aecp_mutants.DEFECTS} == names
failed = aecp_mutants.campaign(work / 'aecp-mutants', 4)
print(f'aecp plants: {"FAIL" if failed else "every one caught"}')
sys.exit(1 if failed else 0)
