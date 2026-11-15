#!/usr/bin/env python3
"""Audit published receipts: python3 -B audit_receipts.py SOURCE PACKET.

Requires public archive ea30c5a0 in SOURCE's object database. Does not read
review reports or author working directories. Scratch extraction is separate.
"""
import ast
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

source, packet = (Path(x).resolve() for x in sys.argv[1:])
rev = 'ea30c5a0abb21abc91db12d7bf5e5c3d15150966'
prefix = 'review-evidence/895-r1/'
def git(*args):
    return subprocess.check_output(['git', '-C', str(source), *args])
manifest = json.loads(git('show', rev + ':' + prefix + 'MANIFEST.json'))
selected = [r for r in manifest if r['file'].split('/')[0] in
            ('author-r8', 'author-r9', 'author-r10') and '/reviews/' not in r['file']]
bad = []
for r in selected:
    data = git('show', rev + ':' + prefix + r['file'])
    if hashlib.sha256(data).hexdigest() != r['published_sha256']:
        bad.append(r['file'])
    target = packet / 'scratch/public' / r['file']
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
assert not bad, bad
root = packet / 'scratch/public/author-r10'
out = {'archive': rev, 'verified_published_files': len(selected), 'bad_hashes': bad,
       'git_signature_status': git('log', '-1', '--format=%G?', rev).decode().strip()}
def image_map(path):
    return {line.split()[1]: line.split()[0] for line in path.read_text().splitlines() if line.strip()}
a = image_map(root / 'receipts/identity/image-sha256-final-056d619d.txt')
b = image_map(root / 'receipts/identity/image-sha256-final-1215bd82.txt')
assert len(a) == len(b) == 552 and a == b
out['image_hash_entries_identical'] = len(a)
out['survey'] = {}
for point in ('1x1', '8x8'):
    path = root / f'receipts/classes/survey-final/survey-{point}.txt'
    rows = [[s.strip() for s in line.strip('|').split('|')]
            for line in path.read_text().splitlines() if line.startswith('| ')][1:]
    unstaged = []
    for row in rows:
        cycles, rule, stated = int(row[3].replace(',', '')), int(row[4]), int(row[2])
        if cycles:
            expected = ((cycles * 105 + 49999) // 50000) * 5
            assert rule == expected and rule <= stated, row
        else:
            unstaged.append(row[0] + ':' + row[1])
    assert len(rows) == 63 and len(unstaged) == 6
    out['survey'][point] = {'statements': len(rows), 'measured': len(rows)-len(unstaged),
                            'not_staged': unstaged, 'under': 0}
plants = root / 'receipts/classes/plants'
out['class_controls'] = {}
for point in ('1x1-1if', '8x8-2if'):
    for plant in ('control', 'paced-over', 'stream-info-over'):
        expected = 0 if plant == 'control' else 1
        vals = {}
        for path in ('record_classes', 'survey-corrected', 'survey-round8'):
            rc = int((plants / f'{plant}-{point}-{path}.rc').read_text())
            assert rc == (0 if path == 'survey-round8' else expected)
            vals[path] = rc
        out['class_controls'][f'{plant}-{point}'] = vals
inventory = (root / 'receipts/docs/superseded-inventory.md').read_text()
entries = [line for line in inventory.splitlines() if re.match(r'\| [^|]+:\d+ \|', line)]
assert len(entries) == 178
out['inventory_entries'] = len(entries)
out['receipt_indexes'] = {}
for revision in ('author-r8', 'author-r9', 'author-r10'):
    base = packet / 'scratch/public' / revision / 'receipts'
    group, checked = '.', 0
    for line in (base / 'INDEX.md').read_text().splitlines():
        if line.startswith('## '):
            group = line[3:].strip()
        match = re.match(r'\| ([^|]+) \| (\d+) \| `([a-f0-9]{64})` \|', line)
        if match:
            name, size, sha = match.groups()
            data = (base / group / name.strip()).read_bytes()
            assert len(data) == int(size) and hashlib.sha256(data).hexdigest() == sha
            checked += 1
    out['receipt_indexes'][revision] = checked
table = (root / 'receipts/gates/verify-table.md').read_text()
rows = [line.split('|') for line in table.splitlines() if line.startswith('| ')][1:]
counts = Counter('carried' if r[5].strip().startswith('carried:') else r[5].strip() for r in rows)
assert counts == {'0':86, 'carried':53, 'NOT RUN':226}, counts
out['workflow_steps'] = dict(counts)
sys.path.insert(0, str(source / 'tb/verilator/ctrl_service_budget'))
import record_classes as rc
assert rc.controls() == []
out['class_selftest_controls'] = len(rc.CONTROLS)
out['command_sensitive_probe'] = {}
for point, cycles in [('1x1/1if', 20363), ('8x8/2if', 17511)]:
    leg = rc.Leg(point, 'answering-ports', 100000000, 100000000,
                 {'aecp-fanout':[rc.Record(0,cycles,rc.SET_STREAM_INFO,0)]})
    assert rc.held(leg,'aecp-fanout','other',rc.SET_STREAM_INFO)
    assert not rc.held(leg,'aecp-fanout','other')
    bound = rc.statements(point)['other']
    assert rc.rule(cycles, leg.cpu_hz) <= bound < rc.rule(30000, leg.cpu_hz)
    out['command_sensitive_probe'][point] = {'measured_us':rc.rule(cycles,leg.cpu_hz),
                                            'stated_us':bound,'planted_us':315}
leg.point = '8x8/1if'
assert not rc.held(leg,'aecp-fanout','other',rc.SET_STREAM_INFO)
out['8x8_1if_report_only'] = True
(packet/'receipt-audit.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
