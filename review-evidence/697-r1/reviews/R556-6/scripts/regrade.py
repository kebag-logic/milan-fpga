#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reviewer regrade of a mutation campaign from its per-arm GoogleTest XML.
Every plant must be CAUGHT in the summary, and every required killer
({test, needle, arm}) must have a failure in that arm's XML whose
marker-delimited streamed message contains the needle (default text excluded).
A killer test ending in '/' names a parameterized prefix.

usage: regrade.py MUTATIONS_JSON CAMPAIGN_DIR"""
import json
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET


def main():
    table = json.load(open(sys.argv[1]))
    work = Path(sys.argv[2])
    summary = {r['name']: r for r in json.load(open(work / 'results.json'))}
    markers = json.load(open(work / 'message-markers.json'))
    begin, end = (markers['begin'], markers['end']) if isinstance(markers, dict) else markers
    block = re.compile('\n' + re.escape(begin) + '\n(.*?)\n' + re.escape(end) + '\n', re.S)
    bad, kills = [], 0
    if {p['name'] for p in table} != set(summary) or len(table) != len(summary):
        bad.append('plant name sets differ')
    for plant in table:
        name = plant['name']
        if summary.get(name, {}).get('status') != 'CAUGHT':
            bad.append(f'{name}: summary status {summary.get(name, {}).get("status")}')
        # Same default arm rule as the campaign driver (scripts/mutation.py).
        default = ('maap_debug' if any(k['test'].startswith('MaapDebug.') for k in plant['kills'])
                   else Path(plant['path']).stem)
        for kill in plant['kills']:
            kills += 1
            xml = work / name / (kill.get('arm', default) + '.xml')
            try:
                cases = list(ET.parse(xml).getroot().iter('testcase'))
            except (OSError, ET.ParseError) as error:
                bad.append(f'{name}: {xml.name}: {error}')
                continue
            test = kill['test']
            hit = False
            for case in cases:
                full = case.get('classname') + '.' + case.get('name')
                if not (full.startswith(test) if test.endswith('/') else full == test):
                    continue
                for failure in case.findall('failure'):
                    if any(kill['needle'] in b for b in block.findall(failure.get('message', ''))):
                        hit = True
            if not hit:
                bad.append(f'{name}: {kill.get("arm", default)}: needle {kill["needle"]!r} not streamed by failing {test}')
    print(f'plants {len(table)}; killers {kills}; regrade failures {len(bad)}')
    print('\n'.join(bad))
    return bool(bad)


if __name__ == '__main__':
    raise SystemExit(main())
