#!/usr/bin/env python3
"""Spot checks of four page statements. usage: spot_checks.py <archive root>"""
import glob
import os
import re
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pcap_census import records, split_envelope  # noqa: E402
from rederive_step3 import console, offsets, ptp_records  # noqa: E402

root = sys.argv[1]
print("1. host (no-envelope) records per tap capture:")
for p in sorted(glob.glob(os.path.join(root, "**", "*.pcap"), recursive=True)):
    n = h = 0
    for lt, pkt in records(p):
        n += 1
        if split_envelope(pkt)[0] == "host":
            h += 1
    print(f"   {os.path.relpath(p, root)}: records {n}, host {h}")
logs = sorted(glob.glob(os.path.join(root, "**", "tcpdump*.log"), recursive=True))
drops = []
for lg in logs:
    m = re.findall(r"(\d+) packets? dropped by kernel", open(lg, errors="replace").read())
    drops.append((os.path.relpath(lg, root), m))
print(f"2. tcpdump logs: {len(logs)}; dropped-by-kernel values: {sorted({x for _, m in drops for x in m})}; logs without a drop line: {[l for l, m in drops if not m]}")
print("3. asCapable return vs the DUT's completed Pdelay exchanges after the link returns, and ACMP CONNECT_TX to the DUT:")
a202 = os.path.join(root, "bench-a202", "bench")
for c in range(1, 7):
    d = os.path.join(a202, f"cycle{c}")
    off = offsets(os.path.join(d, "clock-before.jsonl"))
    t0 = float(re.search(r"T_OFF_CMD (\S+)", open(os.path.join(d, "powerstrip.txt")).read()).group(1)) - off["pi"]
    srv = [v for k, v in off.items() if k.startswith("ubuntu")][0]
    S, _ = console(os.path.join(d, "console.txt"))
    asc = [(s["t"] - t0, (int(s["CLKV_STAT"], 16) >> 16) & 1) for s in S]
    i1 = next(i for i, (t, a) in enumerate(asc) if t > 30 and a)
    req, done, acmp = {}, [], []
    fu = set()
    rsp = {}
    for t, port, fr in ptp_records(os.path.join(d, f"tap-c{c}.pcap")):
        t = t - srv - t0
        et = struct.unpack(">H", fr[12:14])[0]
        o = 14
        if et == 0x8100:
            et = struct.unpack(">H", fr[16:18])[0]
            o = 18
        p = fr[o:]
        if et == 0x88F7 and t > 30:
            mt, seq = p[0] & 0xF, struct.unpack(">H", p[30:32])[0]
            if mt == 2 and port == 3:
                req[seq] = t
            elif mt == 3 and port == 2 and seq in req:
                rsp[seq] = t
            elif mt == 0xA and port == 2 and seq in rsp:
                done.append(t)
        elif et == 0x22F0 and p and (p[0] & 0x7F) == 0x7C and port == 2:
            msg = p[1] & 0x0F
            if msg == 0 and p[20:28].hex() == "020000fffe000001":
                acmp.append(round(t, 2))
    print(f"   cycle {c}: asCapable 0->1 between samples {asc[i1-1][0]:.2f} and {asc[i1][0]:.2f}; completed exchanges after return at {[round(x, 2) for x in done[:3]]}; "
          f"CONNECT_TX to the DUT in 0.5..38 s: {[x for x in acmp if 0.5 < x < 38]}, first after 38 s: {next((x for x in acmp if x > 38), None)}")
