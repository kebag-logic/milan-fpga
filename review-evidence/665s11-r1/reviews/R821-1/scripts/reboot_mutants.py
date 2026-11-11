#!/usr/bin/env python3
"""The author's REBOOT planted defects alone, through the repository's own campaign code.

    python3 -B reboot_mutants.py CLONE OUT {aecp|plat}

aecp: aecp_mutants.DEFECTS whose name starts with `reboot-`; plat: ctrl_mutants.MUTANTS whose name starts with
`plat-reboot-`, and `plat-loop-before-ready`, whose anchor the change moved. Each is planted into a copy of the
firmware tree and must fail its named test on the check's own words (the campaign's own `caught`).
"""
from __future__ import annotations

import sys
from pathlib import Path

CLONE = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2]).resolve()
WHICH = sys.argv[3]
sys.path.insert(0, str(CLONE / 'sw/firmware/ctrl/test'))
sys.path.insert(0, str(CLONE / 'sw/firmware/gtest'))

if WHICH == 'aecp':
    import aecp_mutants
    aecp_mutants.DEFECTS = tuple(d for d in aecp_mutants.DEFECTS if d.name.startswith('reboot-'))
    print(f'{len(aecp_mutants.DEFECTS)} REBOOT defects', flush=True)
    # the full-table drift check is the shipped driver's; this run plants a subset of that table
    aecp_mutants.controls = lambda: None
    escaped = aecp_mutants.campaign(OUT, jobs=4)
else:
    import ctrl_mutants
    ctrl_mutants.MUTANTS = tuple(m for m in ctrl_mutants.MUTANTS
                                 if m.name.startswith('plat-reboot-') or m.name == 'plat-loop-before-ready')
    print(f'{len(ctrl_mutants.MUTANTS)} platform REBOOT defects', flush=True)
    escaped = ctrl_mutants.campaign(OUT, OUT / 'reuse', 4)
print('ESCAPED' if escaped else 'ALL CAUGHT')
raise SystemExit(1 if escaped else 0)
