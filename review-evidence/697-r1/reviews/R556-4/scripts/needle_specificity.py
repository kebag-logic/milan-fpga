#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Grade each required killer from a finished campaign's own XML reports.

argv[1] = tree root (tests/mutations.json, tests/*.cpp), argv[2] = campaign work directory.
For every kill: CAUGHT-BY-MESSAGE when the needle occurs in the named test's failure text,
and still occurs only inside the test's own streamed message literals; SHARED when the needle
also matches the failure text after every assertion message literal of that test is removed
(it then also matches default GoogleTest output or streamed values); MISSING otherwise.
Message literals are collected with an independent tokenizer (string and raw-string
literals after a '<<' that follows an assertion macro's closing parenthesis).
"""
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

root, work = Path(sys.argv[1]), Path(sys.argv[2])
STRING = re.compile(r'R"([^ ()\\\t\n]*)\((.*?)\)\1"|"((?:\\.|[^"\\\n])*)"', re.S)


def unescape(s):
    return bytes(s, 'utf-8').decode('unicode_escape').encode('latin-1').decode('utf-8')


literals = set()
for path in (root / 'tests').glob('*.cpp'):
    text = re.sub(r'//[^\n]*|/\*.*?\*/', ' ', path.read_text(), flags=re.S)
    for m in STRING.finditer(text):
        before = text[:m.start()].rstrip()
        if before.endswith('<<') or before.endswith('"') or before.endswith(')"'):
            literals.add(m[2] if m[2] is not None else unescape(m[3]))
literals = sorted((l for l in literals if l.strip()), key=len, reverse=True)
table = json.loads((root / 'tests/mutations.json').read_text())
counts = {'CAUGHT-BY-MESSAGE': 0, 'SHARED': 0, 'MISSING': 0}
for plant in table:
    failures = {}
    for report in sorted((work / plant['name']).glob('*.xml')):
        for case in ET.parse(report).getroot().iter('testcase'):
            text = '\n'.join(f.get('message', '') for f in case.findall('failure'))
            if text:
                key = case.get('classname') + '.' + case.get('name')
                failures[key] = failures.get(key, '') + text
    for kill in plant['kills']:
        t = kill['test']
        texts = [m for n, m in failures.items() if (n.startswith(t) if t.endswith('/') else n == t)]
        if not any(kill['needle'] in m for m in texts):
            status = 'MISSING'
        else:
            stripped = []
            for m in texts:
                for lit in literals:
                    m = m.replace(lit, '\0')
                stripped.append(m)
            status = 'SHARED' if any(kill['needle'] in m for m in stripped) else 'CAUGHT-BY-MESSAGE'
        counts[status] += 1
        if status != 'CAUGHT-BY-MESSAGE':
            print(status, plant['name'], t, repr(kill['needle']))
print(json.dumps(counts), 'kills', sum(counts.values()), 'plants', len(table))
