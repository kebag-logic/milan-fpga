#!/usr/bin/env python3
"""Compare the findings page's raw-artifact table with the packet's per-cycle
raw-artifacts.json and top-level RAW-ARTIFACTS.json.
usage: check_hash_table.py <page.md> <packet author dir>"""
import json, re, sys, os
page, pk = sys.argv[1], sys.argv[2]
rows = {}
for line in open(page):
    m = re.match(r'\| (\d+) \| `([^`]+)` \| (\d+) \| `([0-9a-f]{64})` \|', line)
    if m:
        rows[(int(m[1]), m[2])] = (int(m[3]), m[4])
print('page rows:', len(rows))
bad = 0
for c in range(1, 11):
    ra = json.load(open(os.path.join(pk, 'cycle%02d' % c, 'raw-artifacts.json')))
    byname = {os.path.basename(e['path']): e for e in ra}
    for (cc, name), (size, sha) in rows.items():
        if cc != c: continue
        e = byname.get(name)
        if not e or e['size'] != size or e['sha256'] != sha:
            bad += 1; print('MISMATCH cycle', c, name, e)
    for name in ('console.jsonl','controller-wire.pcap','tap.pcap','controller.jsonl','events.jsonl'):
        if (c, name) not in rows: bad += 1; print('page lacks', c, name)
top = json.load(open(os.path.join(pk, 'RAW-ARTIFACTS.json')))
flat = json.dumps(top)
miss = [k for k, v in rows.items() if v[1] not in flat]
print('page hashes absent from RAW-ARTIFACTS.json:', miss)
# events.jsonl in packet vs hash
import hashlib
for c in range(1, 11):
    p = os.path.join(pk, 'cycle%02d' % c, 'events.jsonl')
    h = hashlib.sha256(open(p, 'rb').read()).hexdigest(); s = os.path.getsize(p)
    if rows[(c, 'events.jsonl')] != (s, h):
        print('packet events.jsonl differs from page row, cycle', c, s, h[:12], rows[(c,'events.jsonl')][1][:12])
print('mismatches:', bad)
