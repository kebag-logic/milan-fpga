#!/usr/bin/env python3
"""Audit published row arithmetic without claiming a fresh CPU simulation."""
from pathlib import Path
import json
import re
packet = Path(__file__).resolve().parent
evidence = packet/'scratch/public-evidence/author/receipts/measure'
total = 0
for label in ('N10-A1','N10-B1','N10-A8','N10-B8','D10-A1','D10-B1','D10-A8','D10-B8'):
    folder = evidence/label
    data = json.loads((folder/'build.json').read_text())
    table = (folder/'table.md').read_text()
    text = table.split('| Path | Probe | CPU cycles |')[1]
    rows = []
    for line in text.splitlines():
        if not line.startswith('|') or '`' not in line:
            continue
        row = [s.strip() for s in line.split('|')[1:-1]]
        if len(row) != 10:
            continue
        path, probe, cycles, ms, budget, ceiling, verdict, *_ = row
        assert abs(int(cycles.replace(',', ''))/data['cpu_hz']*1000-float(ms)) <= .00051
        assert float(budget) == min(20., float(ceiling)), row
        if verdict != 'fits':
            assert 'owed' in probe, row
        else:
            assert float(ms) <= float(budget) + .00051, row
        rows.append(row)
    assert len(rows) == 49, (label, len(rows))
    assert sum(row[6] != 'fits' for row in rows) == 6
    assert data['cpu_hz'] == data['sys_hz'] == 100000000
    print(label, '49 instances; 43 fit, 6 egress-held misses; CPU/bus 100/100 MHz; arithmetic and per-family bound PASS')
    match = re.search(r'Composed maximum over the 4 backlog windows: ([0-9,]+) CPU cycles', table)
    assert match
    pass_ms = int(match[1].replace(',', '')) / data['cpu_hz'] * 1000
    print('  longest pass', format(pass_ms,'.5f'), 'ms; 20/9 =', format(20/9,'.5f'),
          'ms:', 'OVER' if pass_ms > 20/9 else 'within',
          '; tightest-family 18/9 = 2 ms:', 'OVER' if pass_ms > 2 else 'within')
    total += len(rows)
print(total, 'published instances audited; this is a receipt audit, not source execution')
