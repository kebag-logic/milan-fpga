#!/usr/bin/env python3
"""Decode lane B8's raw GET_COUNTERS payloads independently of the lane's tools.

usage: decode_counters.py <events.jsonl>...

Layout (IEEE 1722.1 GET_COUNTERS response body): descriptor_type u16,
descriptor_index u16, counters_valid u32, then 32 u32 counters; counter i is
valid when bit i of counters_valid is set. Names follow Milan v1.2's counter
tables for CLOCK_DOMAIN (0x0024), STREAM_INPUT (0x0005), STREAM_OUTPUT (0x0006).
"""
import datetime
import json
import sys

NAMES = {
    0x0024: {0: "LOCKED", 1: "UNLOCKED"},
    0x0005: {0: "MEDIA_LOCKED", 1: "MEDIA_UNLOCKED", 2: "STREAM_INTERRUPTED",
             3: "SEQ_NUM_MISMATCH", 4: "MEDIA_RESET", 5: "TIMESTAMP_UNCERTAIN",
             8: "UNSUPPORTED_FORMAT", 9: "LATE_TIMESTAMP", 10: "EARLY_TIMESTAMP",
             11: "FRAMES_RX"},
    0x0006: {0: "STREAM_START", 1: "STREAM_STOP", 2: "MEDIA_RESET",
             3: "TIMESTAMP_UNCERTAIN", 4: "FRAMES_TX"},
}
SHORT = {"LOCKED": "L", "UNLOCKED": "U", "MEDIA_LOCKED": "ML", "MEDIA_UNLOCKED": "MU",
         "STREAM_INTERRUPTED": "SI", "SEQ_NUM_MISMATCH": "SQ", "MEDIA_RESET": "MR",
         "TIMESTAMP_UNCERTAIN": "TU", "UNSUPPORTED_FORMAT": "UF", "LATE_TIMESTAMP": "LT",
         "EARLY_TIMESTAMP": "ET", "STREAM_START": "START", "STREAM_STOP": "STOP"}
CEST = datetime.timezone(datetime.timedelta(hours=2))


def decode(hexs):
    b = bytes.fromhex(hexs)
    dtype = int.from_bytes(b[0:2], "big")
    valid = int.from_bytes(b[4:8], "big")
    out = {}
    for i, name in NAMES.get(dtype, {}).items():
        if valid >> i & 1:
            out[name] = int.from_bytes(b[8 + 4 * i:12 + 4 * i], "big")
    return out


for path in sys.argv[1:]:
    print(f"== {path}")
    for line in open(path):
        d = json.loads(line)
        if d.get("kind") != "counters" or "payloads" not in d:
            continue
        t = datetime.datetime.fromtimestamp(d["t"], CEST).strftime("%H:%M:%S")
        cells = []
        for who, hexs in sorted(d["payloads"].items()):
            if not isinstance(hexs, str) or not hexs:
                cells.append(f"{who}=<none>")
                continue
            c = decode(hexs)
            keep = {SHORT.get(k, k): v for k, v in c.items()
                    if k not in ("FRAMES_TX", "FRAMES_RX") and (v or k in ("LOCKED", "UNLOCKED", "MEDIA_RESET", "MEDIA_UNLOCKED"))}
            cells.append(f"{who}={keep}")
        print(t, d.get("tag"), " | ".join(cells))
