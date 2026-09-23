#!/usr/bin/env python3
"""Step 2 cadence counts and DUT Pdelay turnaround from the A200 tap captures (Run A, B, C, final).

Usage: step2_rederive.py <evidence-root>
Intervals use tap time (unwrapped hardware nanoseconds) within each capture.
"""
import os
import struct
import sys

WRAP = 1 << 32
root = sys.argv[1]
caps = ["runA/tap-runA.pcap", "runB/tap-runB.pcap", "runC/tap-runC.pcap", "final/tap-final.pcap"]
tot = {}
turn = []
exch = {"sw_req": [0, 0], "dut_req": [0, 0]}
maxint = {}
for cp in caps:
    raw = open(os.path.join(root, "bench-a200", "bench", cp), "rb").read()
    off = 24
    first = None
    last = {}
    pend_sw = {}
    pend_dut = {}
    while off + 16 <= len(raw):
        s, us, incl, _ = struct.unpack("<IIII", raw[off:off + 16])
        off += 16
        pkt = raw[off:off + incl]
        off += incl
        if len(pkt) < 42:
            continue
        tag, _, port = struct.unpack("<III", pkt[:12])
        if tag != 6 or port not in (2, 3):
            continue
        host = s * 10**9 + us * 1000
        lo = struct.unpack("<I", pkt[16:20])[0]
        if first is None:
            first = (host, lo)
        k = round(((host - first[0]) - (lo - first[1])) / WRAP)
        t = lo - first[1] + k * WRAP
        fr = pkt[28:]
        et = struct.unpack(">H", fr[12:14])[0]
        if et != 0x88F7:
            continue
        p = fr[14:]
        mt = p[0] & 0xF
        seq = struct.unpack(">H", p[30:32])[0]
        key = (mt, port)
        if key in last:
            tot.setdefault(key, []).append(t - last[key])
        last[key] = t
        if mt == 2 and port == 2:
            pend_sw[seq] = t
            exch["sw_req"][0] += 1
        elif mt == 3 and port == 3 and seq in pend_sw:
            turn.append(t - pend_sw.pop(seq))
            exch["sw_req"][1] += 1
        elif mt == 2 and port == 3:
            pend_dut[seq] = t
            exch["dut_req"][0] += 1
        elif mt == 3 and port == 2 and seq in pend_dut:
            pend_dut.pop(seq)
            exch["dut_req"][1] += 1
names = {(0, 2): "Sync switch->DUT", (0xB, 2): "Announce switch->DUT", (2, 2): "Pdelay_Req switch->DUT", (2, 3): "Pdelay_Req DUT->switch"}
for k, n in names.items():
    iv = tot.get(k, [])
    nom = 125e6 if k[0] == 0 else 1e9
    within = sum(1 for x in iv if abs(x - nom) <= 0.3 * nom)
    print(f"{n:26s} intervals {len(iv):5d}  min {min(iv)/1e6:.1f} ms  max {max(iv)/1e6:.1f} ms  within 30%: {within}")
print(f"exchanges switch-requested: requests {exch['sw_req'][0]} answered {exch['sw_req'][1]}; DUT-requested: requests {exch['dut_req'][0]} answered {exch['dut_req'][1]}")
print(f"DUT turnaround (tap, request to response): min {min(turn)} ns max {max(turn)} ns over {len(turn)}")
