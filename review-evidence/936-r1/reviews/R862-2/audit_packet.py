#!/usr/bin/env python3
"""Verify the public author packet at an immutable archive, and its focused receipts.
Usage: python3 -B audit_packet.py <archive-root>
The root contains MANIFEST.json and author-r2/. No review reports are read.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
entries = [r for r in json.loads((root / 'MANIFEST.json').read_text())
           if r['file'].startswith('author-r2/')]
assert entries
for row in entries:
    actual = hashlib.sha256((root / row['file']).read_bytes()).hexdigest()
    assert actual == row['published_sha256'], row['file']
print(f'PASS: {len(entries)} author-r2 published SHA-256 entries match immutable archive b06d0f563f908f09907579d88b9688c565925dc8')
print('Integrity verification uses published hashes; no cryptographic signature is asserted.')
receipts = root / 'author-r2/receipts'
def summary(path):
    text = path.read_text()
    return json.loads(text[text.index('{'):])
for name in ('r4-tn1', 'r4-tn8', 'r4-dr1', 'r4-de1', 'r4-lt1', 'r4-lt8', 'r4-ev1'):
    run = receipts / 'budget' / name
    identity = json.loads((run / 'build-identity.json').read_text())
    data = summary(run / 'results-summary.json')
    console = (run / 'run-console.txt').read_text()
    assert 'HEAD d1aa4c44 DIRTY 0' in console, name
    assert data['build'] == identity['executable_sha256'], name
    assert identity['cpu_hz'] == identity['sys_hz'] == 100000000
    print(f"{name}: clean exact-head claim; simulator {data['build']}; image {identity['ctrl_app_elf_sha256']}")
    if name in ('r4-tn1', 'r4-tn8'):
        assert not any(data[x] for x in ('refusals', 'misses', 'share_misses', 'notice_misses'))
        assert data['notices']['count'] == data['notices']['within_budget'] == 16
        pattern = r'NOTICE (talker-notice-\d+\.(?:declared|withdrawn)\.if0): committed ([\d.]+) ms after its event\'s commit at sys (\d+), the last of (\d+) recipients at sys (\d+) \(bound ([\d.]+) ms\) within'
        rows = re.findall(pattern, console)
        assert len(rows) == 16, (name, len(rows))
        for label, elapsed, start, recipients, end, bound in rows:
            measured = (int(end) - int(start)) / 100000
            assert int(recipients) == 16 and float(bound) == 20
            assert measured <= 20 and abs(measured - float(elapsed)) <= .00051
            print(f'  {label}: {start}->{end}; 16 recipients; {measured:.5f} ms <= 20 ms')
        assert 'STATED ' not in console
    elif name in ('r4-dr1', 'r4-de1'):
        plant = 'declared-notice-dropped' if name == 'r4-dr1' else 'declared-notice-delayed'
        line = next(l for l in console.splitlines() if l.startswith('CONTROL ' + plant))
        assert 'caught: 16 of 16' in line
        print(line)
    else:
        assert not any(data[x] for x in ('refusals', 'misses', 'notice_misses'))
        print('  existing notice regression: no refusals, budget misses or notice misses')
logs = receipts / 'workflows/logs'
for path in sorted(logs.glob('*__DONE.txt')):
    assert path.read_text().rstrip().endswith('failed 0'), path.name
print(f'PASS: {len(list(logs.glob("*__DONE.txt")))} workflow completion receipts say failed 0')
for campaign, names in (
    ('srp', ('binding-poll-adds-access', 'talker-notice-owed-unreported')),
    ('aecp', ('app-output-notice-dropped', 'app-output-notice-as-an-input', 'app-output-notice-next-source',
              'app-output-notice-kept', 'app-output-notice-owed-unreported')),
):
    text = (logs / f'rtl-fast__firmware-{campaign}-mutants__ci_step_9.log').read_text()
    for name in names:
        hits = [l for l in text.splitlines() if l.startswith('[ok] ' + name + ':')]
        assert hits, name
        print('\n'.join(hits))
print('PASS: focused published receipts checked')
