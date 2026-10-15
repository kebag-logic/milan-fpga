#!/usr/bin/env python3
"""Decode each cycle's GET_COUNTERS payloads (start and end) from the raw cycle events and list every
valid counter that moved, by entity, descriptor and counter slot (IEEE 1722.1 7.4.42 layout:
descriptor_type, descriptor_index, counters_valid, 32 x 32-bit counters).

usage: python3 -I decode_counters.py <b18_author_dir>
"""
import json, sys
from pathlib import Path

# IEEE 1722.1-2021 Table 7.152 (STREAM_INPUT) and 7.149 (AVB_INTERFACE) slot names, valid-bit order
SI = {0: "MEDIA_LOCKED", 1: "MEDIA_UNLOCKED", 2: "STREAM_INTERRUPTED", 3: "SEQ_NUM_MISMATCH", 4: "MEDIA_RESET",
      5: "TIMESTAMP_UNCERTAIN", 6: "TIMESTAMP_VALID", 7: "TIMESTAMP_NOT_VALID", 8: "UNSUPPORTED_FORMAT",
      9: "LATE_TIMESTAMP", 10: "EARLY_TIMESTAMP", 11: "FRAMES_RX"}
SO = {0: "STREAM_START", 1: "STREAM_STOP", 2: "MEDIA_RESET", 3: "TIMESTAMP_UNCERTAIN", 4: "FRAMES_TX"}


def dec(h):
    b = bytes.fromhex(h)
    dt, di, valid = int.from_bytes(b[0:2], "big"), int.from_bytes(b[2:4], "big"), int.from_bytes(b[4:8], "big")
    cnt = [int.from_bytes(b[8 + 4 * i:12 + 4 * i], "big") for i in range(32)]
    return dt, di, valid, cnt


root = Path(sys.argv[1])
for cdir in sorted((root / "cycles").glob("c[0-9][0-9]")):
    ev = [json.loads(l) for l in open(cdir / "events.jsonl")]
    cs = {e["when"]: e["payloads"] for e in ev if e["kind"] == "counters"}
    for key in sorted(cs["start"]):
        dt, di, va, a = dec(cs["start"][key])
        _, _, vb, b = dec(cs["end"][key])
        names = SO if key.startswith("peer") else (SI if dt == 5 else {})
        bits = [i for i in range(32) if (va >> i) & 1]
        moved = {names.get(i, f"slot{i}"): (a[i], b[i]) for i in bits if a[i] != b[i]}
        nonzero_static = {names.get(i, f"slot{i}"): a[i] for i in bits if a[i] == b[i] and a[i]}
        print(cdir.name, key, f"valid=0x{va:08x}", "moved", moved, "static_nonzero", nonzero_static)
