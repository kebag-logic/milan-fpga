#!/usr/bin/env python3
"""One table row from a measure.sh directory: the method of docs/integration/BOARD_PORTING_AX7101.md section 6, wire turnaround at the tap less the responder's claimed t3-t2, per responder.
PDELAY_NS, GPTP_LAT, ASCAPABLE, SYNC come from the console poll taken during the same capture."""
import json, re, statistics, struct, sys
d = sys.argv[1]
ARTY = "02:00:00:00:00:02"
ts = lambda b: int.from_bytes(b[:6], "big") * 10**9 + int.from_bytes(b[6:10], "big")
def frames(path):
    data = open(path, "rb").read(); o = 24
    while o + 16 <= len(data):
        _, _, cap, _ = struct.unpack("<IIII", data[o:o+16]); r = data[o+16:o+16+cap]; o += 16 + cap
        if len(r) < 42: continue
        hi, lo = struct.unpack("<II", r[12:20]); yield (hi << 32) | lo, r[28:]
req, resp, fu = {}, {}, {}
counts = {}
for t, e in frames(d + "/cap.pcap"):
    if struct.unpack(">H", e[12:14])[0] != 0x88F7: continue
    src, p = e[6:12].hex(":"), e[14:]; mt, seq = p[0] & 0xF, struct.unpack(">H", p[30:32])[0]
    counts[f"{'arty' if src == ARTY else 'partner'}:{mt}"] = counts.get(f"{'arty' if src == ARTY else 'partner'}:{mt}", 0) + 1
    if mt == 2: req[(src, seq)] = t
    if mt == 3: resp[(src, seq)] = (t, ts(p[34:44]))
    if mt == 10: fu[(src, seq)] = ts(p[34:44])
res = {}
for (rs, seq), (t, t2) in resp.items():
    if (rs, seq) not in fu: continue
    q = [v for (qs, qseq), v in req.items() if qseq == seq and qs != rs]
    if not q: continue
    res.setdefault(rs, []).append(t - q[0] - (fu[(rs, seq)] - t2))
arty = res.get(ARTY, []); others = [v for k, v in res.items() if k != ARTY]; zero = others[0] if others else []
poll = open(d + "/poll.txt", errors="replace").read()
pd = [int(x) for x in re.findall(r"PDELAY_NS=(\d+)", poll)]
pd = [x if x < 2**31 else x - 2**32 for x in pd]
# the first two polls may still carry an exchange from before the write
pd = pd[2:] if len(pd) > 4 else pd
st = re.findall(r"SYNC=(\d) ASCAPABLE=(\d) TU=(\d) GPTP_LAT=([0-9a-f]{8})", poll)
gm = re.findall(r"GPTP_GM=([0-9a-f]{16})", poll)
row = {"dir": d.rstrip("/").split("/")[-1], "n_arty": len(arty), "n_zero": len(zero),
       "arty": round(statistics.mean(arty), 1) if arty else None, "arty_sd": round(statistics.pstdev(arty), 1) if arty else None,
       "zero": round(statistics.mean(zero), 1) if zero else None, "zero_sd": round(statistics.pstdev(zero), 1) if zero else None}
row["residual"] = round(row["arty"] - row["zero"], 1) if arty and zero else None
lat = int(st[-1][3], 16) if st else 0
row.update(ingress=lat >> 16, egress=lat & 0xffff, gptp_lat=st[-1][3] if st else None)
row["sum"] = round(row["residual"] + row["ingress"] + row["egress"], 1) if row["residual"] is not None else None
row.update(pdelay_mean=round(statistics.mean(pd), 1) if pd else None, pdelay_min=min(pd) if pd else None, pdelay_max=max(pd) if pd else None, pdelay_n=len(pd),
           predicted_pdelay=round((row["arty"] + row["zero"]) / 2, 1) if arty and zero else None,
           ascapable=sorted(set(s[1] for s in st)), sync=sorted(set(s[0] for s in st)), tu=sorted(set(s[2] for s in st)), gm=sorted(set(gm)), wire=counts)
print(json.dumps(row))
