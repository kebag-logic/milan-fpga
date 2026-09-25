#!/usr/bin/env python3
"""Compare probe capture rows with the head's measurements.json, row by row.

Usage: python3 compare_rows.py <measurements.json> <packet-dir>
Arms are read from <packet-dir>/scratch/<arm>/capture.log (full or partial runs).
"""
import json
import re
import sys
from pathlib import Path

ARMS = {'h8x8_50_on': ('endstation_ax7101_8x8', 50_000_000, 'on'),
        'y8x8_50_on': ('endstation_ax7101_8x8', 50_000_000, 'on'),
        'h8x8_50_off': ('endstation_ax7101_8x8', 50_000_000, 'off'),
        'h1x1_50_on': ('endstation_ax7101_1x1_tdm8', 50_000_000, 'on'),
        'h1x1_50_off': ('endstation_ax7101_1x1_tdm8', 50_000_000, 'off')}
receipt = json.loads(Path(sys.argv[1]).read_text())
pkt = Path(sys.argv[2])
out = {}
for name, key in ARMS.items():
    log = pkt / 'scratch' / name / 'capture.log'
    if not log.exists():
        continue
    rows = [dict((k, int(v)) for k, v in re.findall(r'(\w+)=(\d+)', line))
            for line in log.read_text(errors='replace').splitlines()
            if line.startswith('CAPTURE index=')]
    arm = next(a for a in receipt['measurements']
               if (a['shape'], a['cpu_hz'], a['traffic']) == key)
    same = [row == arm['rows'][row['index']] for row in rows]
    out[name] = dict(key=list(key), rows_reproduced=len(rows), all_equal=all(same),
                     max_ms_reproduced=max(r['sys_cycles'] for r in rows) / 1e5,
                     receipt_max_ms=arm['maximum_ms'],
                     receipt_argmax=max(range(16), key=lambda i: arm['rows'][i]['sys_cycles']))
    print(name, json.dumps(out[name]))
# Independent recomputation of every published maximum over every arm.
for (shape, clock) in sorted({(a['shape'], a['cpu_hz']) for a in receipt['measurements']}):
    arms = [a for a in receipt['measurements'] if (a['shape'], a['cpu_hz']) == (shape, clock)]
    worst = max(r['sys_cycles'] for a in arms for r in a['rows'])
    per_arm = {a['traffic']: max(r['sys_cycles'] for r in a['rows']) for a in arms}
    print('MAX', shape, clock, worst, worst / 1e5, 'ms', 'margin_vs_49', 49 / (worst / 1e5),
          'per_arm', per_arm, 'below_24.5ms', worst < 2_450_000, 'slack_ms', 24.5 - worst / 1e5)
