#!/usr/bin/env python3
"""Decode the STREAM_INPUT GET_COUNTERS payloads recorded in a lane B15 run events.jsonl
(IEEE 1722.1-2021 GET_COUNTERS response: descriptor_type, descriptor_index, counters_valid,
then 32 big-endian 32-bit counters; STREAM_INPUT counter order per the standard's table).
usage: decode_counters.py <events.jsonl> [...]"""
import json
import sys

NAMES = ["MEDIA_LOCKED", "MEDIA_UNLOCKED", "STREAM_INTERRUPTED", "SEQ_NUM_MISMATCH", "MEDIA_RESET",
         "TIMESTAMP_UNCERTAIN", "TIMESTAMP_VALID", "TIMESTAMP_NOT_VALID", "UNSUPPORTED_FORMAT",
         "LATE_TIMESTAMP", "EARLY_TIMESTAMP", "FRAMES_RX"]

for path in sys.argv[1:]:
    rows = {}
    for line in open(path):
        d = json.loads(line)
        if d.get("kind") != "counters":
            continue
        b = bytes.fromhex(d["payload"])
        valid = int.from_bytes(b[4:8], "big")
        c = [int.from_bytes(b[8 + 4 * i:12 + 4 * i], "big") for i in range(32)]
        rows[(d["who"], d["tag"])] = (d["t"], valid, c)
        print(path, d["who"], d["tag"], f"t={d['t']:.3f}", f"valid={valid:#x}",
              {n: c[i] for i, n in enumerate(NAMES)})
    for who in ("dut", "peer"):
        if (who, "before") in rows and (who, "after") in rows:
            t0, _, a = rows[(who, "before")]
            t1, _, b = rows[(who, "after")]
            print(path, who, "delta", {n: b[i] - a[i] for i, n in enumerate(NAMES) if b[i] != a[i]},
                  f"dt={t1 - t0:.3f}s", f"FRAMES_RX/dt={(b[11] - a[11]) / (t1 - t0):.1f}/s")
