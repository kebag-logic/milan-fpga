#!/usr/bin/env python3
"""Scratch: run only the named planted defects through their own campaigns (the drivers' code, a filtered table).
usage: (from sw/firmware/ctrl/test) new_mutants.py ROOT NAME..."""
import sys
from pathlib import Path
sys.path.insert(0, '.')
import aecp_mutants, srp_mutants
root, names = Path(sys.argv[1]), set(sys.argv[2:])
aecp = tuple(d for d in aecp_mutants.DEFECTS if d.name in names)
srp = tuple(d for d in srp_mutants.DEFECTS if d.name in names)
assert len(aecp) + len(srp) == len(names), 'unknown defect name'
failed = False
if aecp:
    aecp_mutants.controls()          # on the whole table, as the campaign runs it
    aecp_mutants.controls = lambda: None
    aecp_mutants.DEFECTS = aecp
    failed |= aecp_mutants.campaign(root / 'aecp', jobs=4)
if srp:
    srp_mutants.DEFECTS = srp
    lw = Path('../../../../third_party/lwSRP').resolve()
    failed |= srp_mutants.campaign(root / 'srp', lw, jobs=4)
print('NEW DEFECTS:', 'ESCAPED' if failed else 'all caught')
sys.exit(1 if failed else 0)
