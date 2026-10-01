#!/usr/bin/env python3
"""Window start of each lane B6 case against its last bind or clock-source set (read-only).

usage: window_check.py <lane_packet_dir>

Reads runs/<case>/events.jsonl. Prints, per case, the seconds from the last bind or
set-clock event before the window to window-start, from servo-lock (B CRF) to
window-start, and each in-window DUT read: its offset into the window, MCSRV_STAT
(0x8F8; state = bits 2:0, 4 = LOCKED) and SLIP_TDM (0x8D8 [15:0]).
"""
import json
import sys
from pathlib import Path

pk = Path(sys.argv[1])
for c in ["a0", "a1", "a2", "bint", "bcrf"]:
    ev = [json.loads(line) for line in open(pk / "runs" / c / "events.jsonl")]
    last = ws = lock = st = None
    for e in ev:
        if e["kind"] in ("bind", "set-clock") and ws is None:
            last = e
            if e["kind"] == "set-clock":
                st = e["t"]
        if e["kind"] == "servo-lock":
            lock = e
        if e["kind"] == "window-start":
            ws = e["t"]
    line = f"{c}: last before the window {last['kind']}, window-start {ws - last['t']:.3f} s after it"
    if lock:
        line += (f"; servo-lock event {lock['t'] - st:.3f} s after the set (tool's count {lock['seconds']:.3f} s), "
                 f"window-start {ws - lock['t']:.3f} s after it")
    print(line)
    for e in ev:
        if e["kind"] == "dut" and e.get("tag", "").startswith("window"):
            s = int(e["words"]["0x8f8"], 16)
            print(f"    {e['tag']} at {e['t'] - ws:6.1f} s: MCSRV_STAT {e['words']['0x8f8']} state {s & 7}"
                  f"{' LOCKED' if s & 7 == 4 else ''}, SLIP_TDM {int(e['words']['0x8d8'], 16) & 0xFFFF:#06x}")
