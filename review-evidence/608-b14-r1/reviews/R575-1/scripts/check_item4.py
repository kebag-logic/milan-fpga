#!/usr/bin/env python3
"""Recompute item 4 (talker starts) from startup-cycles.csv, startup-first-ten.csv and start-NNN.json polls."""
import csv, json, sys, re, collections
pk, doc = sys.argv[1], sys.argv[2]
b = pk + '/author/item4'
rows = {}
for l in open(doc):
    m = re.match(r'^\| (\d{3}) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \| (-?[\d.]+) \|$', l.strip())
    if m:
        rows[int(m.group(1))] = m.groups()[1:]
cyc = list(csv.DictReader(open(b + '/startup-cycles.csv')))
ten = list(csv.DictReader(open(b + '/startup-first-ten.csv')))
print('doc rows', len(rows), 'csv cycles', len(cyc), 'first-ten rows', len(ten))
mism = []
hist = collections.Counter()
for r in cyc:
    n = int(r['cycle'].split('-')[-1])
    hist[int(r['first_step_ns'])] += 1
    d = rows.get(n)
    exp = (r['early'], r['late'], r['first_sequence'], r['first_step_ns'], '%.1f' % float(r['first_offset_from_steady_ns']))
    if d != exp:
        mism.append((n, d, exp))
    if r['result'] != 'PASS' and r['result'] != 'OK':
        mism.append(('result', n, r['result']))
    if int(r['sequence_gaps']):
        mism.append(('gaps', n))
print('step histogram', dict(hist))
tvtu = collections.Counter((t['tv'], t['tu']) for t in ten)
print('first-ten tv/tu', dict(tvtu), 'cycles', len({t['cycle'] for t in ten}))
# recompute first step from first-ten timestamps and sequence continuity
steps = collections.Counter(); seqbad = 0
by = collections.defaultdict(list)
for t in ten:
    by[t['cycle']].append(t)
for c, ts in by.items():
    ts.sort(key=lambda x: int(x['pdu']))
    a = [int(x['avtp_timestamp']) for x in ts]
    s = [int(x['sequence']) for x in ts]
    steps[(a[1] - a[0]) % 2**32] += 1
    seqbad += sum(1 for i in range(1, len(s)) if (s[i] - s[i - 1]) % 256 != 1)
print('first step from raw headers', dict(steps), 'seq discontinuities in first ten', seqbad)
# EARLY/LATE in every poll of every start
el = 0; polls = 0; binds = 0
for n in range(1, 101):
    j = json.load(open('%s/start-%03d.json' % (b, n)))
    for p in j['polls']:
        if p['phase'] == 'pre-bind':
            continue
        polls += 1
        if p['counters'].get('EARLY') or p['counters'].get('LATE'):
            el += 1
    binds += j['result']['result'] == 'OK'
print('polls after bind', polls, 'polls with EARLY/LATE>0', el, 'starts OK', binds)
print('mismatches', mism)
