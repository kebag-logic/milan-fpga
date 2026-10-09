#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reviewer regrade: every (plant, arm, test, needle) kill must appear inside a marked
assertion stream of a failure of the named test in that arm's XML report.
usage: regrade_xml.py MUTATIONS_TABLE CAMPAIGN_DIR"""
import json, re, sys
import xml.etree.ElementTree as ET
from pathlib import Path
table = json.loads(Path(sys.argv[1]).read_text()); camp = Path(sys.argv[2])
def canon(name):
    suite, case = name.split('.', 1)
    return suite.split('/')[-1] + '.' + case.split('/')[0]
kills = bad = 0; problems = []
for plant in table:
    module = Path(plant['path']).stem
    default = 'maap_debug' if any(k['test'].startswith('MaapDebug.') for k in plant['kills']) else module
    for kill in plant['kills']:
        kills += 1
        xml = camp / plant['name'] / (kill.get('arm', default) + '.xml')
        want = canon(kill['test'])
        texts = []
        if xml.exists():
            for case in ET.parse(xml).getroot().iter('testcase'):
                if canon(case.get('classname') + '.' + case.get('name')) == want:
                    for f in case.findall('failure'):
                        texts += re.findall(r'TSN_MESSAGE_BEGIN_\w+\n(.*?)\nTSN_MESSAGE_END_\w+',
                                            f.get('message', ''), re.S)
        if not any(kill['needle'] in t for t in texts):
            bad += 1; problems.append((plant['name'], kill.get('arm', default), kill['test']))
print(f'plants {len(table)} kills {kills} not confirmed {bad} {problems[:5]}')
sys.exit(1 if bad else 0)
