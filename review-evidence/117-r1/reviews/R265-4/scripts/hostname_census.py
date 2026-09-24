#!/usr/bin/env python3
"""Census of host names carried in the captures' own protocol fields (value withheld).

usage: hostname_census.py <archive-root: .../review-evidence/117-r1>
For every capture: DHCP option 12 (Host Name) and mDNS A/AAAA owner names, by source MAC
prefix and record class (tapped, or envelope-less = the capture host's own traffic). Each name
is classified as MASKED (only '#'), ROLE (a short host role name the archive itself uses: the
suffix after '<bench-host-prefix>' in its clock files), or OTHER. OTHER prints its octet length
and label shape only, never the value.
"""
import collections
import glob
import json
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tapdec  # noqa: E402

root = sys.argv[1]
roles = set()
for f in glob.glob(os.path.join(root, '**', 'clock-*.jsonl'), recursive=True):
    for ln in open(f):
        h = json.loads(ln).get('host', '')
        if '>' in h:
            roles.add(h.split('>')[-1])


def classify(name):
    if name and set(name) <= {'#', '\0'}:
        return 'MASKED'
    base = name.split('.')[0]
    if base in roles:
        return 'ROLE'
    return 'OTHER (%d octets, %d labels)' % (len(name), name.count('.') + 1)


out = collections.Counter()
for p in sorted(glob.glob(os.path.join(root, '**', '*.pcap'), recursive=True)):
    rel = os.path.relpath(p, root)
    for h, f in tapdec.pcap_records(p):
        env = len(f) >= 42 and f[:4] == b'\x06\x00\x00\x00' and f[8] in (2, 3)
        fr = f[28:] if env else f
        rc = 'tapped' if env else ('envelope-less' if os.path.basename(p).startswith(('tap', 'probe-tap')) else 'host capture')
        d = tapdec.decode(fr)
        if d.get('kind') == 'DHCP':
            u = d['udp']
            if len(u) < 240 or u[236:240] != b'\x63\x82\x53\x63':
                continue
            i = 240
            while i < len(u):
                o = u[i]
                if o == 0:
                    i += 1
                    continue
                if o == 255:
                    break
                ln = u[i + 1]
                v = u[i + 2:i + 2 + ln]
                i += 2 + ln
                if o == 12:
                    out[(rel, rc, d['src'][:6], 'DHCP option 12', classify(v.rstrip(b'\0').decode('latin-1')))] += 1
        elif d.get('kind') in ('mDNS', 'mDNS6'):
            for sec, name, rt, rdata, off in tapdec.dns_records(d['udp']):
                if rt in (1, 28) and sec != 'q':
                    nm = '.'.join(x.decode('latin-1') for x in name)
                    out[(rel, rc, d['src'][:6], 'mDNS %s owner' % ('A' if rt == 1 else 'AAAA'), classify(nm[:-len('.local')] if nm.endswith('.local') else nm))] += 1
print('role names the archive keeps:', sorted(roles))
print('capture | record class | source MAC OUI | field | class | count')
for k, v in sorted(out.items()):
    print(' | '.join(k), '|', v)
tot = collections.Counter()
for k, v in out.items():
    tot[k[4].split(' (')[0]] += v
print('totals by class:', dict(tot))
