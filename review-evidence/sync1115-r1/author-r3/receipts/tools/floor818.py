#!/usr/bin/env python3
"""floor818.py ROUTE_RECEIPT_DIR...: every recorded route regraded against #818's resource gate floor (+0.030 ns setup
and 0 ns hold at every signoff corner, on the best of the recipe's three directives; #665 issuecomment-6930885185):
each route's worst setup and hold slack over the four corners its signoff.txt records, whether it meets, and per image
whether its best directive does. Each argument holds <image>/<directive>/signoff.txt."""
import re
import sys
from pathlib import Path

SETUP, HOLD = 0.030, 0.0
DIRECTIVES = ('ExtraPostPlacementOpt', 'ExtraTimingOpt', 'AltSpreadLogic_high')
print('| Round | Image | Directive | Worst setup, ns | Worst hold, ns | Meets #818 |')
print('|---|---|---|---:|---:|---|')
verdicts = []
for root in map(Path, sys.argv[1:]):
    label = root.parent.parent.name
    for image in sorted(p.name for p in root.iterdir() if p.is_dir() and (p / 'ExtraTimingOpt').is_dir()):
        met = []
        for d in DIRECTIVES:
            text = (root / image / d / 'signoff.txt').read_text()
            corners = re.findall(r'^(\w+): WNS ([+-][\d.]+) ns .*?WHS ([+-][\d.]+) ns', text, re.M)
            assert len(corners) == 4, (root, image, d, corners)
            wns, whs = min(float(c[1]) for c in corners), min(float(c[2]) for c in corners)
            ok = wns >= SETUP and whs >= HOLD
            met.append(ok)
            print(f'| {label} | {image} | {d} | {wns:+.3f} | {whs:+.3f} | {"meets" if ok else "no (setup)" if wns < SETUP else "no (hold)"} |')
        verdicts.append(f'{label} {image}: best of three {"MEETS" if any(met) else "MISSES"} #818 '
                        f'({sum(met)} of 3 directives meet)')
print()
print('\n'.join(verdicts))
