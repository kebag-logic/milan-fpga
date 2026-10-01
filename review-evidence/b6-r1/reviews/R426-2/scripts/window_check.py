#!/usr/bin/env python3
"""Each graded case's window start against its last bind or clock-source set, and
B CRF's servo lock and in-window servo reads, from the archived run logs.
Prints times, kinds and status words only (no stream or descriptor labels).
Usage: window_check.py <author/runs dir>"""
import json, os, sys
R = sys.argv[1]
for c in ("a0", "a1", "a2", "bint", "bcrf"):
    ev = [json.loads(l) for l in open(os.path.join(R, c, "events.jsonl"))]
    ws = next(e for e in ev if e["kind"] == "window-start")
    last = [e for e in ev if e["kind"] in ("bind", "set-clock") and e["t"] <= ws["t"]][-1]
    print(f"{c}: window opened {ws['t'] - last['t']:.3f} s after the last {last['kind']}"
          + (f" (set {last.get('status')}, read back {'equal' if last.get('ok') else 'NOT equal'})" if last["kind"] == "set-clock" else ""))
    if c == "bcrf":
        st = next(e for e in ev if e["kind"] == "set-clock" and e.get("tag") == "case")
        lk = next(e for e in ev if e["kind"] == "servo-lock")
        print(f"   servo-lock {lk['t'] - st['t']:.3f} s after the set; window {ws['t'] - lk['t']:.3f} s after the lock")
        for e in ev:
            if e["kind"] == "dut" and (str(e.get("tag", "")).startswith("window") or e.get("tag") == "servo-wait"):
                w = int(e["words"]["0x8f8"], 16)
                print(f"   {e['tag']:10s} t-set {e['t'] - st['t']:+8.2f} s  MCSRV_STAT 0x{w:08x} state {w & 0xF} bit4 {(w >> 4) & 1}  SLIP_TDM 0x{int(e['words']['0x8d8'], 16) & 0xFFFF:04x}")
