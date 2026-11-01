"""Scratch: the gap between consecutive frames from the Arty on round 1's tap captures, read as offset.py reads them."""
import struct, sys
ARTY = bytes.fromhex("020000000002")
print("capture | frames | Arty frames | smallest start-to-start less frame time, ns | pairs under 10 us | Arty ethertypes")
for p in sys.argv[1:]:
    d = open(p, "rb").read(); o = 24; n = 0; rows = []; types = {}
    while o + 16 <= len(d):
        _, _, cap, _ = struct.unpack("<IIII", d[o:o+16]); r = d[o+16:o+16+cap]; o += 16 + cap
        if len(r) < 42: continue
        n += 1
        hi, lo = struct.unpack("<II", r[12:20]); t = (hi << 32) | lo
        inner = struct.unpack("<I", r[20:24])[0]
        e = r[28:]
        if e[6:12] != ARTY: continue
        et = e[12:14].hex(); types[et] = types.get(et, 0) + 1
        rows.append((t, inner, et))
    gaps = sorted((b[0] - a[0] - (8 + a[1] + 4) * 80, a[1], b[1], a[2], b[2]) for a, b in zip(rows, rows[1:]))
    close = [g for g in gaps if g[0] < 10_000]
    print(p.split("/")[-2], "|", n, "|", len(rows), "|", gaps[0] if gaps else None, "|", len(close), "|", types)
    for g in gaps[:4]: print("   ", g)
