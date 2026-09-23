#!/usr/bin/env python3
"""Cycles 4 to 6 CRF stream phases from the console (CRFT_CTRL 0x750,
CLKV_STAT) and the DUT side of the tap (AVTP CRF subtype 0x04, tu bit).
usage: rederive_stream.py <bench-a202 root>"""
import os
import re
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rederive_step3 import console, offsets, ptp_records  # noqa: E402

root = sys.argv[1]
for c in (4, 5, 6):
    d = os.path.join(root, "bench", f"cycle{c}")
    off = offsets(os.path.join(d, "clock-before.jsonl"))
    pi = off["pi"]
    srv = [v for k, v in off.items() if k.startswith("ubuntu")][0]
    t_off = float(re.search(r"T_OFF_CMD (\S+)", open(os.path.join(d, "powerstrip.txt")).read()).group(1))
    t0 = t_off - pi
    S, _ = console(os.path.join(d, "console.txt"))
    S = [{"t": s["t"] - t0, "st": int(s["CLKV_STAT"], 16), "ctrl": s.get("0x750"), "gm": s["GPTP_GM"]} for s in S]
    tu_rise = next(i for i, s in enumerate(S) if s["t"] > 0 and s["st"] & 1)
    lic_drop = next(s["t"] for s in S if s["t"] > 0 and s["ctrl"] == 0x3)
    relic = next(s["t"] for s in S if s["t"] > 30 and s["ctrl"] not in (None, 0x3))
    good = lambda s: s["gm"] == "3cc0c6fffefe0210" and (s["st"] & 0x10003) == 0x10002
    i = len(S)
    while i > 0 and good(S[i - 1]):
        i -= 1
    ag = S[i]["t"]
    ctrl_before = sorted({hex(s["ctrl"]) for s in S if s["t"] < 0 and s["ctrl"] is not None})
    crf = []
    for t, port, fr in ptp_records(os.path.join(d, f"tap-c{c}.pcap")):
        if port == 3 and struct.unpack(">H", fr[12:14])[0] == 0x8100 and struct.unpack(">H", fr[16:18])[0] == 0x22F0 and fr[18] & 0x7F == 0x04:
            crf.append((t - srv - t0, fr[19] & 1, struct.unpack(">H", fr[14:16])[0]))
    first_tu1 = next(x[0] for x in crf if x[0] > 0 and x[1])
    n_tu1 = sum(1 for x in crf if 0 < x[0] < 20 and x[1])
    end = max(x[0] for x in crf if x[0] < 20)
    after = [x for x in crf if x[0] > 30]
    tci = sorted({hex(x[2]) for x in crf})
    print(f"cycle {c}: CRFT_CTRL before {ctrl_before}; CLKV_STAT[0] rose between {S[tu_rise-1]['t']:.2f} and {S[tu_rise]['t']:.2f}; "
          f"first tu=1 PDU {first_tu1:.2f}; tu=1 PDUs until link end {n_tu1}; emission end {end:.2f}; licence drop {lic_drop:.2f}; "
          f"relicensed {relic:.2f} = all-good {ag:.2f} + {relic - ag:.2f}; first PDU after return {after[0][0]:.2f} tu={after[0][1]}; "
          f"PDUs after return {len(after)} with tu=1 {sum(x[1] for x in after)}; VLAN TCI {tci}")
