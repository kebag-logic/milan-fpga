#!/usr/bin/env python3
"""Audit published final CPU cost tables, completeness receipts and image carry.
Usage: python3 check_cpu.py AUTHOR_R7
"""
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
for point, step, table in [('1x1', 'step16', 'CPU-TABLE-8c5e2b4f.md'),
                           ('8x8-1if', 'step15', 'CPU-TABLE-92de01f7.md')]:
    text = (root / table).read_text()
    if point == '8x8-1if':
        text = text.split('## 8x8/1if\n', 1)[1]
    rows = []
    for line in text.splitlines():
        cells = [c.strip() for c in line.split('|')[1:-1]]
        if len(cells) == 7 and cells[1].replace(',', '').isdigit():
            cycles, rule, stated = (int(cells[i].replace(',', '')) for i in (1, 3, 4))
            computed = ((cycles * 105 + 49999) // 50000) * 5
            assert computed == rule and rule <= stated and cells[5] == 'within', line
            rows.append(cells)
    assert len(rows) == 68, len(rows)
    print(f'{point}: independently rounded all 68 ordinary statement rows; none exceeded')
    print('  Inactive combined-build/retained labels showing zero are not execution evidence;')
    print('  build_one, item.record and separate long-notice receipts carry the active paths.')
    measure = root / f'receipts/{step}/measure'
    ordinary = (measure / f'out/survey-{point}/compare-ordinary.txt').read_text()
    for cells in rows:
        cost, cycles, _, rule, stated, verdict, where = cells
        matching = list({s for s in ordinary.splitlines() if s.startswith(cost + ' ') and s.endswith(where)})
        assert len(matching) == 1, (point, cost, where)
        tokens = matching[0].split()
        assert tokens[1] == cycles and tokens[3:6] == [rule, stated, verdict]
    classes = (measure / f'out/record-classes-{point}.txt').read_text()
    assert classes.rstrip().endswith('RESULT: PASS') and 'REFUSED' not in classes
    print(f'{point}: ordinary rows agree with the survey; class-aware record gate PASS')
    # Labelled/non-completing records are reported under record_classes.py's explicit scope.
    print('  Reported exceptions: ' + str(sum(s.startswith('REPORTED ') for s in classes.splitlines())))
    parts = list((measure / f'legs-{point}').glob('*/parts.json'))
    groups = sum(json.loads(p.read_text())['groups'] for p in parts)
    count = sum(len(json.loads(p.read_text())['parts']) for p in parts)
    assert count == 64 and groups == (241 if point == '1x1' else 240), (point, count, groups)
    for partfile in parts:
        variant = partfile.parent.name
        states = {}
        logs = sorted(partfile.parent.parent.glob(variant + '*.log'),
                      key=lambda p: ('resume' in p.name, p.name))
        for log in logs:
            for number, rc in re.findall(r'^part (\d+) rc=(\d+)', log.read_text(), re.M):
                states[int(number)] = int(rc)
        expected = {i: 0 for i in range(len(json.loads(partfile.read_text())['parts']))}
        assert states == expected, (point, variant, states, expected)
    print(f'{point}: every part exit checked, including recorded resumptions: 64/64 rc=0')
    summary = (measure / f'out/parts-{point}.txt').read_text().splitlines()
    assert len(summary) == count
    passes = 0
    over = []
    misses = []
    for line in summary:
        m = re.search(r'(\d+) refusals, (\d+) budget misses.*?, (\d+) of (\d+) work passes over', line)
        assert m and int(m[1]) == 0, line
        if int(m[3]):
            over.append((line.split(':')[0], int(m[3])))
        passes += int(m[4])
        if int(m[2]):
            assert int(m[2]) == 7
            assert 'backlog-owed' in (measure / f'legs-{point}' / line.split('.part')[0] / 'parts.json').read_text()
            misses.append(line.split(':')[0])
    assert over == ([] if point == '1x1' else [('answering-ports.part13.log', 2), ('declaring-outputs.part3.log', 2)])
    print(f'{point}: {count} parts, {groups} groups, zero refusals, {sum(n for _, n in over)}/{passes} passes over share;')
    print('  Recorded share diagnostics (not represented as passes): ' + str(over))
    print('  seven recorded held-egress misses in each applicable backlog-owed leg: ' + ', '.join(misses))
    names = {g for p in parts for part in json.loads(p.read_text())['parts'] for g in part['groups']}
    assert {'srp-talker', 'srp-talker-loss', 'srp-talker-held'} <= names
    assert all('talker-notice-' + str(i) in names for i in range(8))
    print(f'{point}: Talker initial declaration, loss/hold initiation, held load and all eight notice phases present')
    long = (measure / f'out/survey-{point}/compare-long.txt').read_text()
    assert '# 0 exceeded' in long
    print(long.strip())

def hashes(step):
    return {tuple(row.split()[:2]): row.split()[2]
            for row in (root / f'receipts/{step}/images/hashes.txt').read_text().splitlines()}

old, new = hashes('step15'), hashes('step16')
for key in old:
    if key[0].startswith('8x8'):
        assert old[key] == new[key]
        print('Image carry ' + ' '.join(key) + ': ' + new[key])
print('1x1 image changes require the step16 full remeasurement; step15 and step16 both contain step14 code.')
print('PASS')
