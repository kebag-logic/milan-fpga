#!/usr/bin/env python3
"""Arm x one-word corruption at d = -4..+4, each channel, eight masks, F = 8192 and 16384; one case per capture.

Usage: python3 -I arm_d4.py <tools dir> [jobs]
Captures from the planner's own synthesizer; arms are drop 3 at 300 and F-700, repeat 2 at 500 and
F-450, flip 0x100 on channel 1 at 700 and F-200, tolerance 2. Prints each case that is not exact:
FAIL, every arm found, and the DUT events exactly the one bit-flip at its sample, channel and mask.
"""
import json, sys
from multiprocessing import get_context
sys.path.insert(0, sys.argv[1])
JOBS = int(sys.argv[2]) if len(sys.argv) > 2 else 8
import torture_campaign as t

MASKS = (0x100, 0x200, 0x1E00, 0x40000, 0x80000, 0x80100, 0x100000, 0x01000000)

def arms(F):
    return [("dropped", 300, 3, None), ("repeated", 500, 2, None), ("bit-flip", 700, 0x100, 1),
            ("dropped", F - 700, 3, None), ("repeated", F - 450, 2, None), ("bit-flip", F - 200, 0x100, 1)]

def grade(F, extra):
    ev, log = [], []
    for cls, at, size, ch in arms(F):
        if cls == "bit-flip":
            ev.append(dict(kind="flip", index=at, channel=ch, mask=size)); log.append({"class": cls, "index": at, "mask": size, "channel": ch})
        else:
            ev.append(dict(kind="drop" if cls == "dropped" else "repeat", index=at, n=size)); log.append({"class": cls, "index": at, "n": size})
    cap = t.synthesize_counter_capture(F, 4, events=ev + extra)
    return t.grade_audio_counter_capture(cap, t.CounterCapture(4, "big", 48000, 0.0, 0.0), t.CounterRunLog(log, [], 2),
                                         required_s=(F - 126) / 48000)

def case(args):
    F, ai, d, ch, mask = args
    cls, at, size, armch = arms(F)[ai]
    v, det = grade(F, [dict(kind="flip", index=at + d, channel=ch, mask=mask)])
    dut = [(e["channel"], e["capture_index"], e["class"], e["n"], e.get("mask"), e.get("located_within")) for e in det["events"] if e["attribution"] == "dut"]
    exact = v == "FAIL" and not det["planted_missed"] and [x[:5] for x in dut] == [(ch, at + d, "bit-flip", 1, f"0x{mask:08X}")]
    return args, v, [a["index"] for a in det["planted_missed"]], dut, exact

if __name__ == "__main__":
    cases = [(F, ai, d, ch, m) for F in (8192, 16384) for ai in range(6) for d in range(-4, 5) for ch in range(4) for m in MASKS]
    with get_context("fork").Pool(JOBS) as pool:
        res = pool.map(case, cases, chunksize=16)
    bad = 0
    for args, v, missed, dut, exact in res:
        if not exact:
            bad += 1
            F, ai, d, ch, m = args
            print("NOT-EXACT", json.dumps({"F": F, "arm": arms(F)[ai][:2], "d": d, "ch": ch, "mask": f"0x{m:X}", "v": v, "missed": missed, "dut": dut[:5]}))
    print("SUMMARY", len(res), "not exact", bad)
