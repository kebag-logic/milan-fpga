#!/usr/bin/env python3
"""Audit downloaded public receipts; argv[1] is the archive's extracted evidence root."""
import hashlib
import json
from pathlib import Path
import re
import sys

root = Path(sys.argv[1])
index = json.loads(Path(__file__).with_name('evidence-index.json').read_text())
for entry in index['files']:
    data = (root / entry['file']).read_bytes()
    assert hashlib.sha256(data).hexdigest() == entry['published_sha256'], entry['file']
print('ARCHIVE', index['archive'])
print('SIGNATURE', index['archive_verification'])
print('SHA256', len(index['files']), 'published files verified; original/redacted hashes are not interchanged')
base = root / 'author-r5/receipts'
doc = (base / 'workflows/verify-docs-at-e2be92b0.md').read_text()
rows = [line.split('|') for line in doc.splitlines() if line.startswith('| docs |')]
executed = [row for row in rows if row[5].strip() == '0']
skipped = [row for row in rows if row[5].strip() == 'NOT RUN']
assert len(executed) == 63 and len(skipped) == 34
summarized = []
for row in executed:
    log = re.search(r'`([^`]+)`', row[6]).group(1)
    logpath = base / 'workflows/logs-at-e2be92b0' / log
    if not logpath.is_file():
        summary = logpath.with_name(logpath.name + '.summary.txt')
        assert summary.is_file(), log
        summarized.append(log)
    assert logpath.with_suffix('.rc').read_text().strip() == '0', log
for row in skipped:
    assert row[6].strip(), row
print('DOCS 63 executed steps rc 0; 34 NOT RUN with reasons; 63 rc files present')
print('DOCS full raw logs', len(executed) - len(summarized), 'summary-only logs', summarized)
for state in sorted((base / 'workflows/logs-at-e2be92b0').glob('*__tree-after.txt')):
    print(state.name, state.read_text().strip().replace('\n', ' | '))
j = json.loads((base / 'budget/regrade-at-e2be92b0.json').read_text())
phase_alls = empty = moved = owned = 0
maxima = {}
for leg in j['legs']:
    name = leg['leg']
    log = (base / f'budget/legs-at-e2be92b0/{name}/regrade.log').read_text()
    rc = (base / f'budget/legs-at-e2be92b0/{name}/regrade.rc').read_text().strip()
    assert 'harness = e2be92b0' in log
    expected_head = ('10b2fe213d4c2bf5ccd32e61fc466129c934e31e' if name.startswith('s') else
                     'e2be92b0e0f9a8f0529dea252f23ed44a21e050a')
    assert f'HEAD {expected_head}' in log
    assert rc == leg['rc'] == leg['rc_round4'] and leg['table_same']
    for group, data in leg['groups'].items():
        assert all(data['same'].values()), (name, group)
        result = data['round5']
        assert not result['failing'] and not result['leave_all_failing']
        assert not any(n for k, n in result['leave_all'].items() if k != 'sent')
        e = data['empty_builds']
        empty += e['count']; moved += e['moved']; owned += e['owners']['recorded']
        assert not e['owners']['none'] and not e['outcome_changed'] and e['late_ms'] == 49
        if name not in ('v1', 'v81'):
            phase_alls += result['leave_all']['sent']
            for row, ms in result['rows'].items():
                maxima[row] = max(ms, maxima.get(row, 0))
    print('LEG', name, 'seed experiment' if name.startswith('s') else 'source head', 'rc', rc, 'table unchanged',
          'known cost failures' if rc == '1' else 'PASS')
assert phase_alls == 44 and len(j['legs']) == 13 and empty == owned == 769 and moved == 334
print('PHASES 11; 22 loaded groups; owned LeaveAll sent', phase_alls)
print('MAXIMA ms', json.dumps(maxima, sort_keys=True))
print('EMPTY builds', empty, 'recorded owners', owned, 'anchors earlier', moved, 'outcome changes 0')
campaign = (base / 'budget/selftest-at-e2be92b0.txt').read_text()
assert sum(line.startswith('MUTANT caught:') for line in campaign.splitlines()) == 261
assert not any(line.startswith('MUTANT ESCAPED:') for line in campaign.splitlines())
print('PUBLISHED SELFTEST 261 mutant catch receipts verified; receipt retains a summary of the complete run')
identity = json.loads((root / 'author-r4/receipts/budget/source-and-image-identity.json').read_text())
assert len(identity) == 13 and all(x['firmware_elf_equal_to_prior_run'] for x in identity)
assert all(x.get('harness_bytes_equal_to_head', True) for x in identity)
print('PUBLISHED IMAGE IDENTITY 13 images equal their prior runs; experiment differences enumerated')
seeds = (base / 'budget/seed-harness-at-e2be92b0.txt').read_text()
assert seeds.count('0 files differ;') == 10
print('PUBLISHED SEED BINDING 10 experiment harness directories equal exact-head harness')
print('LIMIT: audit of published receipts and extracts, not execution of unpublished full traces')
