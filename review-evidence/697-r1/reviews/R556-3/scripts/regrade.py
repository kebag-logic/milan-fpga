#!/usr/bin/env python3
# Independent regrade of a mutation campaign from its per-plant gtest XML reports.
# argv[1] = tree root (for tests/mutations.json), argv[2] = campaign work directory.
import json, sys
import xml.etree.ElementTree as ET
from pathlib import Path
table = json.load(open(Path(sys.argv[1]) / 'tests/mutations.json'))
work = Path(sys.argv[2])
summary = {r['name']: r['status'] for r in json.load(open(work / 'results.json'))}
caught = missed = 0
for plant in table:
    failures = {}
    reports = sorted((work / plant['name']).glob('*.xml'))
    for report in reports:
        root = ET.parse(report).getroot()
        for case in root.iter('testcase'):
            msgs = '\n'.join(f.get('message', '') for f in case.findall('failure'))
            if msgs:
                failures[case.get('classname') + '.' + case.get('name')] = failures.get(case.get('classname') + '.' + case.get('name'), '') + msgs
    ok = bool(plant['kills']) and bool(reports)
    for kill in plant['kills']:
        t = kill['test']
        hit = any((name.startswith(t) if t.endswith('/') else name == t) and kill['needle'] in msg
                  for name, msg in failures.items())
        ok = ok and hit
    caught += ok; missed += not ok
    if not ok or summary.get(plant['name']) != 'CAUGHT':
        print('MISMATCH', plant['name'], summary.get(plant['name']))
print(f'plants {len(table)} regraded caught {caught} not caught {missed}; driver summary CAUGHT '
      f"{sum(v == 'CAUGHT' for v in summary.values())} of {len(summary)}; killers {sum(len(p['kills']) for p in table)}")
