"""Verify public archive hashes and regrade receipts. Usage: CHECKOUT."""
import collections
import hashlib
import json
import subprocess
import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
revision = '8518f7346a60ad8ef1e6e690d58ee0d785b5c7bf'
prefix = 'review-evidence/sync1115-r1/'

def git(*args):
    return subprocess.check_output(['git', '-C', str(repo), *args])

def read(path):
    return git('show', revision + ':' + prefix + path)

manifest = json.loads(read('MANIFEST.json'))
selected = [x for x in manifest if x['file'].startswith((
    'author-r6/', 'author-r5/receipts/budget/', 'author-r4/receipts/budget/'))]
for item in selected:
    assert hashlib.sha256(read(item['file'])).hexdigest() == item['published_sha256'], item['file']
print('ARCHIVE:', revision, 'published SHA-256 hashes verified:', len(selected))
print('Cryptographic commit signature present:', b'\ngpgsig ' in git('cat-file', 'commit', revision))

base = 'author-r6/receipts/budget/'
old = 'author-r5/receipts/budget/legs-at-e2be92b0/'
report = json.loads(read(base + 'regrade-at-9aa55d3b.json'))
totals = collections.Counter()
timers = collections.Counter()
phases_sent = 0
maxima = collections.defaultdict(float)
for leg in report['legs']:
    name = leg['leg']
    newer = base + 'legs-at-9aa55d3b/' + name + '/'
    older = old + name + '/'
    assert read(newer + 'table.md') == read(older + 'table.md'), name
    assert read(newer + 'regrade.rc') == read(older + 'regrade.rc'), name
    rc = read(newer + 'regrade.rc').decode().strip()
    assert rc == ('0' if name == 'v1' else '1')
    before = json.loads(read(older + 'results.json'))['results']
    after = json.loads(read(newer + 'results.json'))['results']
    before = {r['group']: r for r in before}
    after = {r['group']: r for r in after}
    for group, data in leg['groups'].items():
        a, b = before[group], after[group]
        aj, bj = a['passes']['joins'], b['passes']['joins']
        for key in ('count', 'shortest', 'longest', 'over', 'leave_all', 'failing'):
            assert aj[key] == bj[key], (name, group, key)
        assert a['probes'] == b['probes'], (name, group, 'probes')
        assert not bj['failing']
        totals.update(bj['runs'])
        moves = data['moves']
        assert moves['run_outs'] == sum(bj['runs'].values())
        assert moves['moved'] == len(moves['every'])
        assert aj['runs']['released'] - bj['runs']['released'] == moves['moved']
        assert bj['runs']['empty'] - aj['runs']['empty'] == moves['moved']
        if name.startswith('s') or name == 'p81':
            phases_sent += bj['leave_all']['runs']['sent']
            for row in b['probes']:
                if '.mrpdu.' in row['probe']:
                    key = row['probe'].split('.mrpdu.')[1]
                    maxima[key] = max(maxima[key], row['ms'])
        for move in moves['every']:
            assert (move['round5b'], move['round6']) == ('released', 'empty')
            assert move['answered_by'] and move['owner'] not in move['answered_by']
            assert move['owner_frame_after_opportunity_ms'] is None
            timers[move['timer']] += 1
            print('MOVE:', name, group, move['timer'], move['at_ms'], move['owner'],
                  'previously answered by', ', '.join(move['answered_by']))
    print('LEG:', name, 'table bytes identical; rc unchanged:', rc)
assert sum(totals.values()) == 1871 and sum(timers.values()) == 73
assert timers == {'join': 46, 'periodic': 27}
assert totals['late'] == totals['absent'] == totals['unowned'] == 0
assert phases_sent == 44
print('TOTAL:', dict(totals), 'MOVES:', dict(timers), 'phase LeaveAll sent:', phases_sent)
print('MAXIMUM ROWS MS:', dict(maxima))
receipt = read(base + 'selftest-at-9aa55d3b.txt').decode()
caught = [line for line in receipt.splitlines() if line.startswith('MUTANT caught:')]
assert len(caught) == 265
assert 'PASS lines: 882; MUTANT caught lines: 265; MUTANT lines not caught: 0' in receipt
assert 'self-test: 0 failures' in receipt
print('PUBLISHED SELFTEST: 882 checks reported; 265 named caught mutant records verified')
wf = read('author-r6/receipts/workflows/verify-docs-at-9aa55d3b.md').decode()
assert '63 steps ran, 34 not run with a reason, 0 bad' in wf
assert read('author-r6/receipts/workflows/verify-docs-at-9aa55d3b.rc').strip() == b'0'
print('PUBLISHED DOCS: 63 executed steps, 34 reasoned skips, 0 bad')
print('LIMIT: archived summaries/extracts, not full raw simulation logs; no new simulation or build attestation')
