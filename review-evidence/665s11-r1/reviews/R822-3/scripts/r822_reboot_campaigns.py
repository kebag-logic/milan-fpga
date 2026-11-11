#!/usr/bin/env python3
"""R822-2 spot-check: the head's own REBOOT planted defects, through each driver's own campaign().

Usage: python3 -B r822_reboot_campaigns.py <probe-tree> <out-dir> plat|aecp

plat: ctrl_mutants.MUTANTS narrowed to names starting 'plat-reboot-'.
aecp: aecp_mutants.DEFECTS narrowed to names starting 'reboot-' (its table-drift control first).
Each campaign plants into its own copy under <out-dir>; the probe tree is not edited.
Exit 0 when every selected defect is caught on its own words.
"""
import sys
from pathlib import Path

tree, out, which = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3]
sys.path.insert(0, str(tree / 'sw/firmware/ctrl/test'))
out.mkdir(parents=True, exist_ok=True)
if which == 'plat':
    import ctrl_mutants as cm
    cm.MUTANTS = tuple(m for m in cm.MUTANTS if m.name.startswith('plat-reboot-'))
    cm.unnamed_tests = lambda: []
    print(f'selected {len(cm.MUTANTS)}: {[m.name for m in cm.MUTANTS]}', flush=True)
    escaped = cm.campaign(out, out / 'reuse', 8)
else:
    import aecp_mutants as am
    am.controls()
    am.DEFECTS = tuple(d for d in am.DEFECTS if d.name.startswith('reboot-'))
    am.controls = lambda: None
    print(f'selected {len(am.DEFECTS)}: {[d.name for d in am.DEFECTS]}', flush=True)
    escaped = am.campaign(out, jobs=8, stack=am.STACK.resolve())
print('RESULT:', 'ESCAPED' if escaped else 'ALL CAUGHT', flush=True)
sys.exit(1 if escaped else 0)
