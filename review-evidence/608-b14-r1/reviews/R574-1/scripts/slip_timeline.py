#!/usr/bin/env python3
"""List every console read of 0x900008d4 (SLIP_LB, SLIP_TDM, RENDER_STAT) in the
packet, in time order. usage: slip_timeline.py <packet-author-dir>"""
import os, re, sys
A = sys.argv[1]
out = []
for root, _, files in os.walk(A):
    for f in files:
        p = os.path.join(root, f)
        try: t = open(p, errors='replace').read()
        except Exception: continue
        for m in re.finditer(r"### (\S+) cmd='mem_read 0x900008d4 12'.*?\n0x900008d4\s+((?:[0-9a-f]{2} ){12})", t, re.S):
            b = bytes.fromhex(m.group(2).replace(' ', ''))
            lb = int.from_bytes(b[0:4], 'little'); tdm = int.from_bytes(b[4:8], 'little'); rs = int.from_bytes(b[8:12], 'little')
            out.append((m.group(1), os.path.relpath(p, A), lb, tdm, rs))
seen = set()
for r in sorted(out):
    k = (r[0], r[2], r[3], r[4])
    if k in seen: continue
    seen.add(k)
    print('%s %-45s SLIP_LB=0x%08x SLIP_TDM=0x%08x RENDER_STAT=0x%08x rails=%d' % (r[0], r[1], r[2], r[3], r[4], (r[4] >> 16) & 0xff))
