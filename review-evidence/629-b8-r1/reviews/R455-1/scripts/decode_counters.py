#!/usr/bin/env python3
"""Independent decode of the GET_COUNTERS payloads in runs/{sw,crfll}/events.jsonl,
compared with the lane's decoded summaries (summary/sw/switches.json,
summary/crfll/lockloss.json). Layout: descriptor_type u16, descriptor_index u16,
counters_valid u32, then 32 x u32 (IEEE 1722.1 7.4.42; Milan v1.2 counter tables).

usage: decode_counters.py <author-dir> <out.txt>
"""
import json
import sys
from pathlib import Path

A, out = Path(sys.argv[1]), Path(sys.argv[2])
NAMES = {
    0x0024: {0: "LOCKED", 1: "UNLOCKED"},
    0x0006: {0: "STREAM_START", 1: "STREAM_STOP", 2: "MEDIA_RESET"},
    0x0005: {0: "MEDIA_LOCKED", 1: "MEDIA_UNLOCKED", 2: "STREAM_INTERRUPTED", 3: "SEQ_NUM_MISMATCH",
             4: "MEDIA_RESET", 5: "TIMESTAMP_UNCERTAIN", 9: "LATE_TIMESTAMP", 10: "EARLY_TIMESTAMP"},
}


def dec(h):
    b = bytes.fromhex(h)
    dt = int.from_bytes(b[0:2], "big")
    vals = [int.from_bytes(b[8 + 4 * i:12 + 4 * i], "big") for i in range(32)]
    return dt, {n: vals[i] for i, n in NAMES.get(dt, {}).items()}


L, bad, n = [], 0, 0
for run, summ in (("sw", "summary/sw/switches.json"), ("crfll", "summary/crfll/lockloss.json")):
    S = json.loads((A / summ).read_text())["counters"]
    for line in (A / "runs" / run / "events.jsonl").read_text().splitlines():
        e = json.loads(line)
        if e.get("kind") != "counters":
            continue
        for key, h in e["payloads"].items():
            if not h:
                continue
            dt, mine = dec(h)
            theirs = S.get(e["tag"], {}).get(key)
            n += 1
            if theirs is None:
                L.append(f"{run} {e['tag']} {key}: not in summary"); bad += 1; continue
            diff = {k: (v, theirs.get(k)) for k, v in mine.items() if k in theirs and theirs[k] != v}
            if diff:
                L.append(f"{run} {e['tag']} {key}: MISMATCH {diff}"); bad += 1
L.append(f"payloads decoded {n}; mismatches {bad}")
out.write_text("\n".join(L) + "\n")
print("\n".join(L))
