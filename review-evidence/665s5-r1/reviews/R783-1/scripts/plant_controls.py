#!/usr/bin/env python3
"""Each plant's catch rule (run.py: a finding of the plant's group starting '<words>:') applied to the UNPLANTED
1x1 product-clock run of the plant's arm. A plant whose rule already matches unplanted cannot escape: its
'caught' verdict does not depend on the plant.

Usage: python3 -I plant_controls.py <receipts dir>
"""
import json
import re
import sys
from pathlib import Path

rec = Path(sys.argv[1])
# name: (group, words, arm), from hooks.py at the head under review (Plant(group, words, arm))
PLANTS = {
    'adp-late': ('control', 'LATE H-ADP', 'idle'), 'adp-order': ('hooks-order-adp', 'ORDER H-ADP', 'idle'),
    'disc-late': ('hooks-late-disc', 'LATE H-DISC', 'idle'), 'disc-order': ('acmp-disc', 'ORDER H-DISC', 'idle'),
    'acmp-late': ('hooks-late-acmp', 'LATE H-ACMP', 'idle'), 'acmp-order': ('hooks-order-acmp', 'ORDER H-ACMP', 'idle'),
    'aecp-late': ('hooks-late-aecp', 'LATE H-AECP', 'idle'), 'aecp-order': ('aecp', 'ORDER H-AECP', 'idle'),
    'notify-late': ('hooks-late-notify', 'LATE H-NOTIFY', 'idle'),
    'notify-order': ('aecp-fanout', 'ORDER H-NOTIFY', 'idle'),
    'counters-late': ('hooks-counters', 'LATE H-COUNTERS', 'answering'),
    'counters-order': ('hooks-counters', 'ORDER H-COUNTERS', 'answering'),
    'maap-late': ('hooks-late-maap', 'LATE H-MAAP', 'idle'), 'maap-order': ('maap', 'ORDER H-MAAP', 'idle'),
    'srp-late': ('hooks-late-srp', 'LATE H-SRP', 'idle'), 'srp-order': ('srp', 'ORDER H-SRP', 'idle'),
}
vacuous = 0
for name, (group, words, arm) in PLANTS.items():
    d = json.loads((rec / 'runs' / ('1x1-ans' if arm == 'answering' else '1x1-idle') / 'results.json').read_text())
    # findings carry their group in a trailing '(group)'; the held push's 'never sent' finding has none
    mine = [x for x in d['findings'] if x.endswith(f'({group})') or (group == 'hooks-counters' and 'held push' in x)]
    hit = [x for x in mine if x.startswith(words + ':')]
    rows = [r for r in d['rows'] if r['group'] == group]
    plant_log = (rec / 'plants' / f'plant-{name}.log').read_text()
    m = re.search(r'^PLANT .*$', plant_log, re.M)
    print(f"{name:15s} group {group:18s} unplanted rows {len(rows):3d}; unplanted findings matching '{words}:' "
          f"{len(hit)}{' -> CANNOT ESCAPE' if hit else ''}")
    for x in hit:
        print('    unplanted:', x)
    print('    planted receipt:', m.group(0) if m else 'no PLANT line')
    vacuous += bool(hit)
print('plants whose catch rule already matches unplanted:', vacuous)
