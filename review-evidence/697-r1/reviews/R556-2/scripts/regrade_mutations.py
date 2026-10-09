#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Independent regrade of a mutation work directory from its per-arm XML reports.

usage: regrade_mutations.py <repo> <mutation-work-dir>
Each kill must name a test whose <failure> message contains the needle, in the
XML of that kill's arm, and the XML must be complete (tests attr == testcases,
every case run/completed). Prints a summary JSON and exits nonzero on any miss.
"""
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

repo, work = Path(sys.argv[1]), Path(sys.argv[2])
table = json.loads((repo / 'tests/mutations.json').read_text())
caught, missed, kills = 0, [], 0
for m in table:
    module = Path(m['path']).stem
    default = 'maap_debug' if any(k['test'].startswith('MaapDebug.') for k in m['kills']) else module
    ok = True
    for k in m['kills']:
        kills += 1
        arm = k.get('arm', default)
        xml = work / m['name'] / (arm + '.xml')
        try:
            root = ET.parse(xml).getroot()
        except (OSError, ET.ParseError) as e:
            ok = False
            missed.append((m['name'], arm, 'no report: ' + str(e)))
            continue
        cases = list(root.iter('testcase'))
        if int(root.get('tests', -1)) != len(cases) or not all(
                c.get('status') == 'run' and c.get('result') == 'completed' for c in cases):
            ok = False
            missed.append((m['name'], arm, 'incomplete report'))
            continue
        hit = False
        for c in cases:
            name = c.get('classname') + '.' + c.get('name')
            match = name.startswith(k['test']) if k['test'].endswith('/') else name == k['test']
            if match and any(k['needle'] in f.get('message', '') for f in c.findall('failure')):
                hit = True
        if not hit:
            ok = False
            missed.append((m['name'], arm, k['test'], k['needle']))
    caught += ok
print(json.dumps({'plants': len(table), 'kills': kills, 'caught_by_name': caught,
                  'missed': missed}, indent=1))
sys.exit(1 if missed or caught != len(table) else 0)
