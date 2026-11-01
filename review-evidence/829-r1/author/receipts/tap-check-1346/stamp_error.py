#!/usr/bin/env python3
"""Stamp error from a bench tap capture: wire turnaround (tap clock) minus the responder's claimed t3-t2, per responder."""
import statistics, struct, sys
ts = lambda b: int.from_bytes(b[:6], "big") * 10**9 + int.from_bytes(b[6:10], "big")
def frames(path):
    d = open(path, "rb").read(); o = 24
    while o + 16 <= len(d):
        _, _, cap, _ = struct.unpack("<IIII", d[o:o+16]); r = d[o+16:o+16+cap]; o += 16 + cap
        if len(r) < 42: continue
        hi, lo = struct.unpack("<II", r[12:20]); yield (hi << 32) | lo, r[28:]
req, resp, fu = {}, {}, {}
for t, e in frames(sys.argv[1]):
    if struct.unpack(">H", e[12:14])[0] != 0x88F7: continue
    src, p = e[6:12].hex(":"), e[14:]; mt, seq = p[0] & 0xF, struct.unpack(">H", p[30:32])[0]
    if mt == 2: req[(src, seq)] = t
    if mt == 3: resp[(src, seq)] = (t, ts(p[34:44]))
    if mt == 10: fu[(src, seq)] = ts(p[34:44])
srcs = {k[0] for k in resp}
for s in sorted(srcs):
    wire, claim, err = [], [], []
    for (rs, seq), (t, t2) in resp.items():
        if rs != s or (rs, seq) not in fu: continue
        q = [v for (qs, qseq), v in req.items() if qseq == seq and qs != rs]
        if not q: continue
        w, c = t - q[0], fu[(rs, seq)] - t2
        wire.append(w); claim.append(c); err.append(w - c)
    if err:
        print(f"responder {s}: n={len(err)} wire turnaround {statistics.mean(wire):.0f} ns, claimed t3-t2 {statistics.mean(claim):.0f} ns, "
              f"wire minus claimed mean {statistics.mean(err):.1f} ns, min {min(err)}, max {max(err)}, stdev {statistics.pstdev(err):.1f}")
