#!/usr/bin/env python3
"""DUT Pdelay turnaround on the tap clock in integer nanoseconds (the tap's
32-bit nanosecond word, differenced modulo 2^32), for the four A200 Step 2
captures. usage: turnaround_int.py <bench-a200 root>"""
import os
import statistics
import struct
import sys

RUNS = ["runA/tap-runA.pcap", "runB/tap-runB.pcap", "runC/tap-runC.pcap", "final/tap-final.pcap"]


def recs(path):
    d = open(path, "rb").read()
    off = 24
    while off + 16 <= len(d):
        _, _, incl, _ = struct.unpack("<IIII", d[off:off + 16])
        off += 16
        pkt = d[off:off + incl]
        off += incl
        if len(pkt) < 28:
            continue
        typ, _b, port, _hi, lo, cap, orig = struct.unpack("<7I", pkt[:28])
        if typ == 6 and cap == orig and 28 + cap <= len(pkt):
            yield lo, port, pkt[28:28 + cap]


allv, med = [], []
claimed = []
for r in RUNS:
    req, rsp, rfu = {}, {}, {}
    for lo, port, fr in recs(os.path.join(sys.argv[1], "bench", r)):
        if struct.unpack(">H", fr[12:14])[0] != 0x88F7:
            continue
        p = fr[14:]
        mt, seq = p[0] & 0xF, struct.unpack(">H", p[30:32])[0]
        if mt == 2 and port == 2:
            req[seq] = lo
        elif mt == 3 and port == 3:
            rsp[seq] = (lo, p)
        elif mt == 0xA and port == 3:
            rfu[seq] = p
    v = []
    for s, t in req.items():
        if s in rsp:
            v.append((rsp[s][0] - t) % 2**32)
            # claimed t3 - t2: t2 = requestReceiptTimestamp in the Resp body, t3 = responseOriginTimestamp in the Resp_FU
            if s in rfu:
                def tsf(b):
                    return (int.from_bytes(b[0:6], "big") * 10**9 + int.from_bytes(b[6:10], "big"))
                t2 = tsf(rsp[s][1][34:44])
                t3 = tsf(rfu[s][34:44])
                cf = lambda b: int.from_bytes(b[8:16], "big", signed=True) / 65536
                claimed.append((t3 - t2) + cf(rfu[s]) - cf(rsp[s][1]))
    allv += v
    med.append(statistics.median(v))
print(f"switch requests, DUT responds: {len(allv)} exchanges; tap request-to-response ns min {min(allv)} max {max(allv)}; per-run medians {med}")
print(f"claimed t3-t2 (correction fields included) ns min {min(claimed):.0f} max {max(claimed):.0f} over {len(claimed)}")
