#!/usr/bin/env python3
"""R575-2: check item 5/6 soak claims of the delta against the archived packet.
Usage: check_soak_records.py <author dir>"""
import json, os, re, sys, glob
a = sys.argv[1]
print(open(os.path.join(a, 'soak/soak-overlap-recovery.txt')).read())
rows = [l.split() for l in open(os.path.join(a, 'soak/soak-overlap-recovery.txt')).read().splitlines()[1:] if l.strip()]
by = {}
for c, prev, port, sub, sid, miss, rec, gap in rows:
    by.setdefault(c, []).append((port, sub, sid, int(miss), rec))
for c, v in sorted(by.items()):
    print('capture', c, 'streams hit', len(v), [(p, s, i, m) for p, s, i, m, _ in v], 'all recovered', all(r == 'all' for *_, r in v))
aaf = [m for v in by.values() for p, s, i, m, _ in v if s == '0x2']; crf = [m for v in by.values() for p, s, i, m, _ in v if s == '0x4']
print('AAF missing range', min(aaf), max(aaf), 'CRF missing', sorted(set(crf)))
print('DUT CRF stream (0001) hit in capture 035:', any(i == '0001' for _, _, i, _, _ in by['035']))
# item 6: console reads from prebind to final
files = [os.path.join(a, 'soak/console-prebind.txt')] + sorted(glob.glob(os.path.join(a, 'soak/console-soak-*.txt'))) + [os.path.join(a, 'restore/console-final.txt')]
n = 0; bad = []
for f in files:
    t = open(f).read()
    mac = re.search(r'0x90000110\s+((?:[0-9a-f]{2} ){4})', t)
    words = []
    for base in ('0x90000200', '0x90000210', '0x90000220', '0x90000230'):
        m = re.search(base + r'\s+((?:[0-9a-f]{2} ){4,16})', t)
        b = bytes.fromhex(m.group(1).replace(' ', ''))
        words += [int.from_bytes(b[i:i + 4], 'little') for i in range(0, len(b), 4)]
    macw = int.from_bytes(bytes.fromhex(mac.group(1).replace(' ', '')), 'little')
    n += 1
    if macw != 0xd or words[1] != 0x1B8 or any(words[4:13]): bad.append((os.path.basename(f), hex(macw), [hex(w) for w in words]))
print('console reads', n, 'deviating (MAC_STATUS!=0xd or STATS_CAP!=0x1B8 or a nonzero lane 0x210-0x230):', bad)
cap = 0x1B8
print('STATS_CAP lanes real:', [n for n in range(9) if cap >> n & 1], 'lane 6 (0x228) bit:', cap >> 6 & 1)
s = json.load(open(os.path.join(a, 'soak/summary.json')))
d = s['counter_deltas_first_to_last_poll']
for k, v in d.items():
    if 'counters' in v and any(x in v['counters'] for x in ('FRAMES_RX', 'FRAMES_TX')):
        print(k, {c: v['counters'][c] for c in v['counters'] if c.startswith(('FRAMES', 'TIMESTAMP_VALID'))})
