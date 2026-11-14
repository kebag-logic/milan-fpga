#!/usr/bin/env python3
"""The firmware mutant campaigns limited to the named plants (this lane's new and re-anchored ones), each on its own
campaign driver as test_ctrl_firmware.py --self-test runs it. usage: subset_mutants.py TREE OUT ctrl|aecp|srp NAME..."""
import sys
from pathlib import Path
tree = Path(sys.argv[1]).resolve(); out = Path(sys.argv[2]).resolve(); kind = sys.argv[3]; names = set(sys.argv[4:])
test = tree / 'sw/firmware/ctrl/test'
sys.path[:0] = [str(test), str(tree / 'sw/firmware/gtest')]
import ctrl_mutants, aecp_mutants, srp_mutants, fw_gtest
from ctrl_build import CTRL
from ctrl_reuse import cut_reuse
if kind == 'ctrl':
    ctrl_mutants.MUTANTS = tuple(m for m in ctrl_mutants.MUTANTS if m.name in names)
    print('planting', len(ctrl_mutants.MUTANTS), flush=True)
    reuse = out / 'reuse'; reuse.mkdir(parents=True, exist_ok=True); cut_reuse(reuse)
    failed = ctrl_mutants.campaign(out / 'mutants', reuse, 4)
elif kind == 'aecp':
    aecp_mutants.controls = lambda: None   # the subset claims fewer tests than the full table
    aecp_mutants.DEFECTS = tuple(d for d in aecp_mutants.DEFECTS if d.name in names)
    print('planting', len(aecp_mutants.DEFECTS), flush=True)
    failed = aecp_mutants.campaign(out / 'aecp-mutants', 4, (0, 1))
else:
    srp_mutants.DEFECTS = tuple(d for d in srp_mutants.DEFECTS if d.name in names)
    print('planting', len(srp_mutants.DEFECTS), flush=True)
    failed = srp_mutants.campaign(out / 'srp-mutants', tree / 'third_party/lwSRP', 4)
print('SUBSET:', 'FAIL' if failed else 'PASS')
sys.exit(1 if failed else 0)
