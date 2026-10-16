#!/usr/bin/env python3
"""Decode a ProfiShark tap capture of gPTP Pdelay and compare the turnaround seen AT THE TAP
with the turnaround the responder CLAIMS (t3 - t2), per responder."""
import struct, sys, statistics as st
raw = open(sys.argv[1], 'rb').read()
magic = struct.unpack('<I', raw[:4])[0]
assert magic in (0xa1b2c3d4, 0xa1b23c4d), hex(magic)
off = 24; recs = []
while off + 16 <= len(raw):
    ts_s, ts_f, incl, orig = struct.unpack('<IIII', raw[off:off+16]); off += 16
    pkt = raw[off:off+incl]; off += incl
    if len(pkt) < 28 + 14 + 34: continue
    h = struct.unpack('<III', pkt[:12]); port = h[2]
    tsraw = struct.unpack('<Q', pkt[12:20])[0]
    fr = pkt[28:]
    et = struct.unpack('>H', fr[12:14])[0]; p = fr[14:]
    if et == 0x8100: et = struct.unpack('>H', fr[16:18])[0]; p = fr[18:]
    if et != 0x88f7: continue
    mtype = p[0] & 0xF; seq = struct.unpack('>H', p[30:32])[0]
    src = p[20:30].hex()
    def ts10(b): return int.from_bytes(b[0:6], 'big') * 10**9 + int.from_bytes(b[6:10], 'big')
    body_ts = ts10(p[34:44]); corr = int.from_bytes(p[8:16], 'big', signed=True) / 65536.0
    req_id = p[44:54].hex() if mtype in (3, 0xA) else ''
    recs.append(dict(port=port, tsraw=tsraw, mtype=mtype, seq=seq, src=src, sa=fr[6:12].hex(), body=body_ts, corr=corr, req=req_id))
print("records:", len(recs), "ports:", sorted(set(r['port'] for r in recs)), "types:", sorted(set(r['mtype'] for r in recs)))
# decide the tap timestamp unit from consecutive Pdelay_Req of one source (1 s apart)
reqs = [r for r in recs if r['mtype'] == 2]
by = {}
for r in reqs: by.setdefault(r['src'], []).append(r)
unit = None
for s, l in by.items():
    if len(l) > 3:
        d = st.median([b['tsraw'] - a['tsraw'] for a, b in zip(l, l[1:])])
        print("src", s, "sa", l[0]['sa'], "port", l[0]['port'], "n", len(l), "median raw delta between requests", d)
        unit = unit or d
scale = 1.0
if unit and unit > 1e15: scale = 2**32          # ns * 2^32
print("timestamp scale divisor:", scale)
for s, l in by.items():
    rows = []
    for rq in l:
        rs = [r for r in recs if r['mtype'] == 3 and r['req'] == s and r['seq'] == rq['seq'] and r['tsraw'] > rq['tsraw']]
        fu = [r for r in recs if r['mtype'] == 0xA and r['req'] == s and r['seq'] == rq['seq']]
        if not rs or not fu: continue
        tap_turn = (rs[0]['tsraw'] - rq['tsraw']) / scale
        claimed = (fu[0]['body'] + fu[0]['corr']) - (rs[0]['body'] + rs[0]['corr'])
        rows.append((tap_turn, claimed, tap_turn - claimed, rs[0]['sa']))
    if rows:
        d = [x[2] for x in rows]
        print(f"requester {s}: responder sa {rows[0][3]} exchanges {len(rows)} tap_turnaround median {st.median(x[0] for x in rows):.0f} ns, "
              f"claimed t3-t2 median {st.median(x[1] for x in rows):.0f} ns, DIFF (tap - claimed) median {st.median(d):.1f} ns, min {min(d):.1f}, max {max(d):.1f}")
