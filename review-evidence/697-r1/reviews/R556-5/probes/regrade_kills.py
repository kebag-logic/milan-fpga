#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Independently regrade a mutation campaign from its raw XML reports.

Usage: regrade_kills.py TREE CAMPAIGN_WORK
For every required killer, in the XML of its own arm, the named test must have a failure element whose text
between the campaign's begin/end marker lines contains the needle, and that failure's
reported source line must be the assertion statement holding the needle literal
(the literal lies between the reported line and the end of that statement).
"""
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

tree, work = Path(sys.argv[1]), Path(sys.argv[2])
plants = json.loads((tree / 'tests/mutations.json').read_text())
begin, end = json.loads((work / 'message-markers.json').read_text())
sources = {p.name: p.read_text().splitlines() for p in (tree / 'tests').glob('*.[ch]pp')}


def arm_of(plant, kill):
    module = Path(plant['path']).stem
    default = 'maap_debug' if any(k['test'].startswith('MaapDebug.') for k in plant['kills']) else module
    return kill.get('arm', default)


def failures_for(directory, arm):
    out = {}
    for xml in directory.glob(arm + '.xml'):
        for case in ET.parse(xml).getroot().iter('testcase'):
            name = case.get('classname') + '.' + case.get('name')
            for failure in case.findall('failure'):
                out.setdefault(name, []).append(failure.get('message', ''))
    return out


def streamed(message):
    parts, lines, inside = [], message.split('\n'), False
    current = []
    for line in lines:
        if line == begin and not inside:
            inside, current = True, []
        elif line == end and inside:
            inside = False
            parts.append('\n'.join(current))
        elif inside:
            current.append(line)
    return parts


def located(message, needle):
    m = re.match(r'(.*?/tests/)?([^/:\n]+\.[ch]pp):(\d+)\n', message)
    if not m or m[2] not in sources:
        return False
    row = int(m[3])
    text = sources[m[2]]
    # The reported line opens the assertion statement; it ends at the first line ending in ';'.
    # Bracket depth is counted outside string literals so blocks inside the statement are skipped.
    i, depth = row - 1, 0
    while i < len(text):
        if needle in text[i]:
            return True
        code = re.sub(r'"(?:\\.|[^"\\])*"', '""', text[i])
        depth += sum(code.count(c) for c in '({[') - sum(code.count(c) for c in ')}]')
        if depth <= 0 and code.rstrip().endswith(';'):
            return False
        i += 1
    return False


rows, bad = [], 0
for plant in plants:
    for kill in plant['kills']:
        failures = failures_for(work / plant['name'], arm_of(plant, kill))
        test, needle = kill['test'], kill['needle']
        names = [n for n in failures if (n.startswith(test) if test.endswith('/') else n == test)]
        ok_stream = any(needle in part for n in names for msg in failures[n] for part in streamed(msg))
        ok_loc = any(located(msg, needle) and any(needle in p for p in streamed(msg))
                     for n in names for msg in failures[n])
        status = 'CONFIRMED' if ok_stream and ok_loc else 'UNCONFIRMED'
        bad += status != 'CONFIRMED'
        rows.append({'plant': plant['name'], 'test': test, 'needle': needle,
                     'streamed': ok_stream, 'assertion_line': ok_loc, 'status': status})
print(json.dumps({'plants': len(plants), 'killers': len(rows), 'confirmed': len(rows) - bad,
                  'unconfirmed': [r for r in rows if r['status'] != 'CONFIRMED']}, indent=1))
