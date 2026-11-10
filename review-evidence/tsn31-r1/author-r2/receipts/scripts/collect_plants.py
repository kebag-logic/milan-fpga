#!/usr/bin/env python3
"""usage: collect_plants.py WORK -- summarise each plant directory that R811-1's plants.py left in WORK (its per-arm
.out files), for a run that stopped before writing results.json."""
import sys
from pathlib import Path
for d in sorted(p for p in Path(sys.argv[1]).iterdir() if p.is_dir()):
    cells = []
    for arm in ('acmp_tests', 'acmp_wide', 'every_sink_33'):
        f = d / (arm + '.out')
        if not f.exists():
            cells.append(arm + ': not run')
            continue
        lines = f.read_text().splitlines()
        passed = [l for l in lines if l.startswith('[  PASSED  ]')]
        failed = sorted({l.split()[3] for l in lines if l.startswith('[  FAILED  ]') and len(l.split()) > 3 and '.' in l.split()[3]})
        ub = [l for l in lines if 'runtime error' in l][:1]
        cells.append(arm + ': ' + ('pass, ' + passed[0][13:] if passed and not failed else 'FAIL ' + ','.join(failed) + (' ' + ub[0] if ub else '')))
    print(d.name, '|', ' | '.join(cells))
