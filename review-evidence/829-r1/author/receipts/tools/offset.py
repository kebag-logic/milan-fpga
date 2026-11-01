#!/usr/bin/env python3
"""The Arty's time against the grandmaster, from one tap clock: each Pdelay_Resp_Follow_Up's t3 from the Arty, less the grandmaster time at that response's capture, interpolated from the bracketing Sync captures and their Follow_Ups' preciseOriginTimestamp + correctionField.
usage: offset.py <pcap> [extra_egress_ns] : prints the raw difference and, with the extra egress removed, the offset of the Arty's PHC."""
import statistics, struct, sys
ARTY = "02:00:00:00:00:02"
ts = lambda b: int.from_bytes(b[:6], "big") * 10**9 + int.from_bytes(b[6:10], "big")
data = open(sys.argv[1], "rb").read(); o = 24
extra = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0
sync_t, fu_g, resp_t, t3 = {}, {}, {}, {}
while o + 16 <= len(data):
    _, _, cap, _ = struct.unpack("<IIII", data[o:o+16]); r = data[o+16:o+16+cap]; o += 16 + cap
    if len(r) < 42: continue
    hi, lo = struct.unpack("<II", r[12:20]); t = (hi << 32) | lo; e = r[28:]
    if struct.unpack(">H", e[12:14])[0] != 0x88F7: continue
    src, p = e[6:12].hex(":"), e[14:]; mt, seq = p[0] & 0xF, struct.unpack(">H", p[30:32])[0]
    corr = int.from_bytes(p[8:16], "big", signed=True) / 65536.0
    if src != ARTY and mt == 0: sync_t[seq] = t
    if src != ARTY and mt == 8: fu_g[seq] = ts(p[34:44]) + corr
    if src == ARTY and mt == 3: resp_t[seq] = t
    if src == ARTY and mt == 10: t3[seq] = ts(p[34:44])
pts = sorted((sync_t[s], fu_g[s]) for s in sync_t if s in fu_g)
res = []
import bisect
xs = [a for a, _ in pts]
for s in sorted(t3):
    if s not in resp_t: continue
    T = resp_t[s]; i = bisect.bisect_right(xs, T)
    if i == 0 or i >= len(xs): continue
    (a0, g0), (a1, g1) = pts[i-1], pts[i]
    if a1 - a0 > 300_000_000: continue
    g = g0 + (g1 - g0) * (T - a0) / (a1 - a0)
    res.append((T, t3[s] - g))
v = [x for _, x in res]
if v:
    print(f"n={len(v)} raw t3-GM mean {statistics.mean(v):.1f} ns sd {statistics.pstdev(v):.1f} min {min(v):.0f} max {max(v):.0f}; extra egress {extra:.0f} -> PHC offset from GM mean {statistics.mean(v)-extra:.1f} ns")
    n = len(v) // 6 or 1
    for k in range(0, len(v), n):
        w = v[k:k+n]
        print(f"  block {k}: n={len(w)} mean {statistics.mean(w):.1f} sd {statistics.pstdev(w):.1f}")
else:
    print("no matched response")
