#!/usr/bin/env python3
"""Recompute item 4 (talker starts) from the packet's raw first-ten AAF headers
and per-start counter polls; compare with the page's table.
usage: check_item4.py <packet-author-dir> <findings-page>"""
import collections, csv, json, os, re, sys
A, PAGE = sys.argv[1], sys.argv[2]
d = os.path.join(A, 'item4')
hdr = collections.defaultdict(list)
for r in csv.DictReader(open(os.path.join(d, 'startup-first-ten.csv'))):
    hdr[r['cycle']].append(r)
bad = []; res = {}
tvtu = collections.Counter()
for c, rs in sorted(hdr.items()):
    rs.sort(key=lambda r: int(r['pdu']))
    dec = []
    for r in rs:
        b = bytes.fromhex(r['raw_header'])
        assert b[0] == 0x02, (c, 'not AAF')
        tv = b[1] & 1; mr = (b[1] >> 3) & 1; seq = b[2]; tu = b[3] & 1
        ts = int.from_bytes(b[12:16], 'big')
        dec.append((seq, tv, tu, mr, ts))
        tvtu[(tv, tu)] += 1
        if (str(tv), str(tu), str(seq), str(ts)) != (r['tv'], r['tu'], r['sequence'], r['avtp_timestamp']):
            bad.append((c, r['pdu']))
    gaps = sum(1 for a, b in zip(dec, dec[1:]) if (b[0] - a[0]) % 256 != 1)
    step = (dec[1][4] - dec[0][4]) % (1 << 32)
    res[c] = (dec[0][0], step, gaps, len(dec))
print('starts', len(res), 'headers', sum(v[3] for v in res.values()), 'tv/tu', dict(tvtu), 'csv-vs-raw mismatches', bad)
print('first step histogram', dict(collections.Counter(v[1] for v in res.values())))
print('sequence gaps in first ten', sum(v[2] for v in res.values()))
# counters on every poll
el = []; npoll = 0; tags = collections.Counter()
for c in sorted(res):
    j = json.load(open(os.path.join(d, c.replace('cycle', 'start') + '.json' if c.startswith('cycle') else c + '.json')))
    for p in j['polls']:
        npoll += 1; tags[p['phase'].split('-')[0]] += 1
        if p['phase'] == 'pre-bind': continue
        cn = p.get('counters') or {}
        if cn.get('EARLY') or cn.get('LATE'): el.append((c, p['phase'], cn.get('EARLY'), cn.get('LATE')))
print('polls', npoll, 'phases', dict(tags), 'post-bind polls with EARLY/LATE > 0:', el)
tab = {}
for l in open(PAGE):
    m = re.match(r'^\| (\d{3}) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \| (-?[\d.]+) \|$', l.strip())
    if m: tab['start-' + m.group(1)] = m.groups()
mis = [(c, tab.get(c), res[c]) for c in res if not tab.get(c) or int(tab[c][3]) != res[c][0] or int(tab[c][4]) != res[c][1] or tab[c][1] != '0' or tab[c][2] != '0']
print('page rows', len(tab), 'mismatches', mis)
