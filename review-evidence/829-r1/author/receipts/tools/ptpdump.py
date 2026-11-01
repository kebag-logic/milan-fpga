#!/usr/bin/env python3
"""Summarise gPTP frames in a tap capture: per (source, type) counts, rate, and the first rows. usage: ptpdump.py <pcap> [rows]"""
import struct, sys, collections
names = {0:'Sync',2:'PdReq',3:'PdResp',8:'FU',10:'PdRFU',11:'Ann',12:'Sig'}
d = open(sys.argv[1],'rb').read(); o = 24; rows = int(sys.argv[2]) if len(sys.argv) > 2 else 0
ct = collections.Counter(); first = {}; last = {}; ports = collections.Counter(); oth = collections.Counter()
n = 0; base = None
while o + 16 <= len(d):
    s, us, cap, ln = struct.unpack("<IIII", d[o:o+16]); r = d[o+16:o+16+cap]; o += 16 + cap
    if len(r) < 42: continue
    hi, lo = struct.unpack("<II", r[12:20]); t = (hi << 32) | lo; e = r[28:]
    if base is None: base = t
    ports[r[20:28].hex()] += 0
    et = struct.unpack(">H", e[12:14])[0]; src = e[6:12].hex(':'); dst = e[:6].hex(':')
    if et != 0x88f7:
        oth[(src, dst, hex(et))] += 1
        continue
    p = e[14:]; mt = p[0] & 0xf; seq = struct.unpack(">H", p[30:32])[0]
    k = (src, names.get(mt, mt)); ct[k] += 1; first.setdefault(k, t); last[k] = t
    if n < rows:
        print(f"{(t-base)/1e9:10.5f} hdr={r[:28].hex()[-24:]} {src} {names.get(mt,mt):6} seq={seq:5} flags={p[6:8].hex()} rq={p[44:54].hex() if mt in (3,10) else ''} clk={p[20:30].hex()}")
    n += 1
for k, v in sorted(ct.items()):
    span = (last[k]-first[k])/1e9
    print(k, v, f"interval {span/(v-1):.3f} s" if v > 1 and span else "")
print("other", oth.most_common(12))
