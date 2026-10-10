#!/usr/bin/env python3
"""Print the packet figures behind items 5-8 of the findings page: soak counter
deltas, capture statistics, coverage gaps, overlap recovery, MAAP summary and
the restore comparison basis. usage: check_soak_maap_restore.py <packet-author-dir>"""
import collections, json, os, re, sys
A = sys.argv[1]
s = json.load(open(os.path.join(A, 'soak', 'summary.json')))
print('soak polls', s['polls'], 'elapsed', s['last_elapsed_s'], 'timing reads', s['timing_reads'], 'timing changes', s['timing_changes'], 'polls_with_errors', s['polls_with_errors'], 'rule increments', next(v for k, v in s.items() if k.endswith('_rule_increments')))
for k, v in s['counter_deltas_first_to_last_poll'].items():
    if 'counters' in v:
        print('  ', k, v['valid_mask'], {c: x['delta'] for c, x in v['counters'].items() if x['delta']})
    else:
        print('  ', k, v)
drops = collections.Counter(); n = 0
for l in open(os.path.join(A, 'soak', 'capture-receipts.jsonl')):
    d = json.loads(l); n += 1
    txt = json.dumps(d)
    m = re.search(r'(\d+) packets dropped by kernel', txt)
    drops[m.group(1) if m else 'no-statistic'] += 1
print('capture receipts', n, 'kernel-drop values', dict(drops))
print(open(os.path.join(A, 'soak', 'soak-coverage.txt')).read().strip())
rec = [l.split() for l in open(os.path.join(A, 'soak', 'soak-overlap-recovery.txt')).read().strip().split('\n')[1:]]
by = collections.defaultdict(list)
for r in rec: by[r[0]].append((r[2], r[3], r[4], r[5], r[6]))
for c, v in sorted(by.items()): print('capture', c, 'streams with loss', len(v), v)
m = json.load(open(os.path.join(A, 'maap', 'summary.json')))
for k, v in m['by_sender'].items(): print('maap', k.split('/')[0], v['types'], v['ranges'], v['announce_interval_s'])
print('maap overlaps', m['overlaps'], 'non-announce', m['non_announce'], 'console words', m['console_maap_words_distinct'])
print(open(os.path.join(A, 'restore', 'restore-compare.txt')).read().split('\n')[0], '(final vs the 06:22 soak pre-bind inventory)')
for l in open(os.path.join(A, 'item2', 'teardown', 'events.jsonl')):
    d = json.loads(l)
    if d['kind'] == 'restore-compare': print('as-found (05:17-05:20) rows compared at item 2 teardown:', len(d['rows']), 'equal', sum(v['equal'] for v in d['rows'].values()))
