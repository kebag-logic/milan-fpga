#!/usr/bin/env python3
"""Independent box 3 probe on the tap clock, with its own pcap and console parsing.
Usage: probe_box3.py RAW_ROOT
Per cycle: the grandmaster-loss and grandmaster-return brackets re-placed
through the DUT PHC (nearest Pdelay response within 3 s in PHC time, from
unrounded tap times) and their margins at d = 0 and at d_lo = 10.938 ms
(u = 0.075 ms). PHC continuity is in probe_phc_steps.py."""
import json, re, struct, sys
from pathlib import Path
SW, DUT = "3cc0c6fffefe0210", "020000fffe000001"
D_LO, U = 0.010938, 0.000075
def recs(path):
    raw = open(path, "rb").read(); off = 24; first = None
    while off + 16 <= len(raw):
        s, f, incl, _ = struct.unpack("<IIII", raw[off:off + 16]); off += 16
        pkt = raw[off:off + incl]; off += incl
        host = s * 10**9 + f * 1000
        if len(pkt) < 42: continue
        tag, _, port = struct.unpack("<III", pkt[:12])
        if tag != 6 or port not in (2, 3): continue
        lo = struct.unpack("<I", pkt[16:20])[0]
        if first is None: first = (host, lo)
        k = round(((host - first[0]) - (lo - first[1])) / 2**32)
        fr = pkt[28:]
        et = struct.unpack(">H", fr[12:14])[0]; p = fr[14:]
        if et == 0x8100: et = struct.unpack(">H", fr[16:18])[0]; p = fr[18:]
        if et != 0x88F7 or len(p) < 44: continue
        yield dict(port=port, tap=lo - first[1] + k * 2**32, mt=p[0] & 0xF, seq=struct.unpack(">H", p[30:32])[0],
                   corr=int.from_bytes(p[8:16], "big", signed=True) / 65536.0,
                   ts=int.from_bytes(p[34:40], "big") * 10**9 + int.from_bytes(p[40:44], "big"),
                   gm=p[53:61].hex() if (p[0] & 0xF) == 0xB and len(p) >= 61 else None)
root = Path(sys.argv[1])
for i in range(1, 7):
    d = root / f"cycle{i:02d}"
    R = list(recs(d / "tap.pcap"))
    resp = {r["seq"]: r["tap"] for r in R if r["port"] == 3 and r["mt"] == 0x3}
    pairs = sorted((r["ts"] + r["corr"], resp[r["seq"]]) for r in R if r["port"] == 3 and r["mt"] == 0xA and r["seq"] in resp and 0 <= r["tap"] - resp[r["seq"]] < 1e8)
    # console samples placed through the nearest pair within 3 s
    S = []
    for l in open(d / "console.jsonl"):
        if not l.strip(): continue
        r = json.loads(l)
        if r["cmd"] != "milan_status": continue
        kv = dict(re.findall(r"(\w+)=([0-9A-Za-z]+)", r["raw"]))
        if "TAI_NS" not in kv: continue
        phc = int(kv["TAI_NS"], 16)
        best = min(pairs, key=lambda p: abs(p[0] - phc))
        S.append(dict(gm=kv["GPTP_GM"], tap=(best[1] + phc - best[0]) if abs(best[0] - phc) <= 3e9 else None))
    ann = [r for r in R if r["port"] == 2 and r["mt"] == 0xB and r["gm"] == SW]
    # grandmaster loss: first sample naming the DUT after one naming the switch
    k = next(k for k in range(1, len(S)) if S[k]["gm"] == DUT and S[k - 1]["gm"] == SW)
    a = S[k - 1]["tap"]
    lastann = max(r["tap"] for r in ann if r["tap"] < a)
    c = lastann + 3e9
    out = f"cycle{i} pairs={len(pairs)}"
    if a is not None:
        out += f" | GM loss lower margin: d=0 {(c - a)/1e6:.2f} ms, d_lo {(c - (a - D_LO*1e9 + U*1e9))/1e6:.2f} ms"
    # grandmaster return: last sample naming DUT before the first naming the switch again (after the loss)
    k2 = next(j for j in range(k + 1, len(S)) if S[j]["gm"] == SW and S[j - 1]["gm"] == DUT)
    a2, b2 = S[k2 - 1]["tap"], S[k2]["tap"]
    if a2 is not None and b2 is not None:
        cand = [r["tap"] for r in ann if r["tap"] <= b2 - D_LO * 1e9 + U * 1e9]
        c2 = max(cand)
        out += f" | GM return: announce-to-old-read at d=0 {(c2 - a2)/1e6:.2f} ms, at d_lo {(c2 - (a2 - D_LO*1e9 + U*1e9))/1e6:.2f} ms; new-read lead {(b2 - c2)/1e6:.2f} ms at d=0"
    print(out)
