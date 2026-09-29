#!/usr/bin/env python3
"""Classify the vendor-prefix 16-hex stream IDs in msrp.tsv that no tracked
file carries: does each share the reference peer's entity-ID prefix (first 12
hex, the peer's MAC-derived part)? Prints no identifier.
Usage: stream_id_class.py <archived author dir>"""
import csv, glob, json, os, re, sys
os.chdir(sys.argv[1])
peer = None
for l in open('bind/baseline/snapshot-after.jsonl'):
    d = json.loads(l)
    if d.get('role') == 'peer' and d.get('what', '').startswith('state-5-8'):
        peer = d['response']['listener'].lower()
        break
ids, senders = set(), set()
for f in glob.glob('*/*/msrp.tsv'):
    for r in csv.DictReader(open(f), delimiter='\t'):
        s = r['stream_id'].lower()
        if re.fullmatch(r'[0-9a-f]{16}', s) and re.search('[a-f]', s[:6]) and 'fffe' not in s \
                and not s.startswith(('91e0f0', '020000', '041060')):
            ids.add(s)
            senders.add((r['sender'], r['type']))
print('vendor-prefix stream ids in msrp.tsv:', len(ids))
for s in ids:
    print(' shares the reference peer entity-ID prefix:', s[:12] == peer[:12], '; declared as:', sorted(senders))
