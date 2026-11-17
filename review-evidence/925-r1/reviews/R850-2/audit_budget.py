#!/usr/bin/env python3
"""Cross-check published budget rows and the measurement rounding rule."""
import argparse
from collections import Counter
import json
import re
import subprocess
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('--repo', type=Path, required=True)
a = p.parse_args()
base = '22239840693f38be230410d189dc9f4d16303feb:review-evidence/925-r1/author-r3/receipts/'
def read(path):
    return subprocess.check_output(['git', '--no-replace-objects', '-C', str(a.repo), 'show', base + path]).decode()
reports = []
for shape in ['1x1-1if', '8x8-1if']:
    summary = read('budget/' + shape + '-summary.md')
    costs = []
    for line in summary.splitlines():
        cells = [x.strip() for x in line.split('|')[1:-1]]
        if len(cells) != 7 or not cells[0].startswith(('polls.', 'stated.')):
            continue
        old, new, delta, rounded = map(int, cells[1:5])
        expected = ((new * 105 + 49999) // 50000) * 5
        assert delta == new - old and rounded == expected, line
        costs.append(cells[0])
    rows = []
    for line in summary.splitlines():
        cells = [x.strip() for x in line.split('|')[1:-1]]
        if len(cells) == 5 and cells[0].startswith(('held.srp', 'mrpdu', 'service.srp', 'srp.')):
            assert float(cells[1]) <= float(cells[2]) and cells[3] == 'True'
            rows.append(cells)
    stated = Counter()
    log = read('budget/' + shape + '.log')
    for line in log.splitlines():
        if not line.startswith('STATED '):
            continue
        if "a pass's polls base" in line:
            stated['polls.base'] += 1
        elif 'a acmp item' in line:
            stated['polls.acmp'] += 1
        elif 'a declined ACMP offer' in line:
            stated['polls.acmp_declined'] += 1
        else:
            raise AssertionError(line)
    assert len(costs) == 16 and len(rows) == 8
    table = read('budget/' + shape + '-table.md')
    table_rows = [line for line in table.splitlines() if line.startswith('|') and
                  re.search(r'\b(SRP|TRANSMIT)\b|held\.srp|service\.srp|mrpdu', line)]
    reports.append({'shape': shape, 'cost_rounding_checks': len(costs),
                    'srp_transmit_maxima': rows, 'stated_categories': dict(stated),
                    'selected_table_rows': table_rows})
print(json.dumps({'passed': True, 'points': reports}, indent=2))
