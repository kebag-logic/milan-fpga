#!/usr/bin/env python3
"""Decode the archived raw AVTP headers of item 4 and compare tv/tu/mr/sequence/timestamp to the CSV columns."""
import csv, sys, collections
ten = list(csv.DictReader(open(sys.argv[1] + '/author/item4/startup-first-ten.csv')))
bad = []; sub = collections.Counter()
for t in ten:
    h = bytes.fromhex(t['raw_header'])
    # locate AVTP start: raw header may begin at AVTP subtype; accept either 24-byte AVTP header or with Ethernet/VLAN prefix
    off = 0
    if len(h) >= 18 and h[12:14] == b'\x81\x00' and h[16:18] == b'\x22\xf0':
        off = 18
    elif len(h) >= 14 and h[12:14] == b'\x22\xf0':
        off = 14
    a = h[off:]
    subtype = a[0]; sv = a[1] >> 7; mr = (a[1] >> 3) & 1; tv = a[1] & 1; seq = a[2]; tu = a[3] & 1
    ts = int.from_bytes(a[12:16], 'big')
    sub[(off, subtype)] += 1
    if (str(tv), str(tu), str(mr), str(seq), str(ts)) != (t['tv'], t['tu'], t['mr'], t['sequence'], t['avtp_timestamp']):
        bad.append((t['cycle'], t['pdu'], (tv, tu, mr, seq, ts), (t['tv'], t['tu'], t['mr'], t['sequence'], t['avtp_timestamp'])))
print('header offsets/subtypes', dict(sub), 'rows', len(ten), 'mismatches', len(bad), bad[:3])
