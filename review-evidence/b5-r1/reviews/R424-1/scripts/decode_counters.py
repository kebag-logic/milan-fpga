#!/usr/bin/env python3
"""Decode every GET_COUNTERS response in each run's ctl.jsonl (IEEE 1722.1 STREAM_INPUT
and STREAM_OUTPUT counter order). usage: decode_counters.py <author dir>"""
import json, sys
from pathlib import Path
IN = ["MEDIA_LOCKED", "MEDIA_UNLOCKED", "STREAM_INTERRUPTED", "SEQ_NUM_MISMATCH", "MEDIA_RESET",
      "TIMESTAMP_UNCERTAIN", "TIMESTAMP_VALID", "TIMESTAMP_NOT_VALID", "UNSUPPORTED_FORMAT",
      "LATE_TIMESTAMP", "EARLY_TIMESTAMP", "FRAMES_RX"]
OUT = ["STREAM_START", "STREAM_STOP", "MEDIA_RESET", "TIMESTAMP_UNCERTAIN", "FRAMES_TX"]
A = Path(sys.argv[1])
for run in ["a-try1", "diag1", "a-long", "cap-test1"]:
    print("==", run)
    for l in open(A / "runs" / run / "ctl.jsonl"):
        x = json.loads(l).get("line", {})
        if x.get("cmd") != "GET_COUNTERS": continue
        pl = bytes.fromhex(x["payload"])
        dtype = int.from_bytes(pl[0:2], "big"); valid = int.from_bytes(pl[4:8], "big")
        vals = [int.from_bytes(pl[8 + 4 * i:12 + 4 * i], "big") for i in range(32)]
        names = IN if dtype == 5 else OUT if dtype == 6 else []
        nz = {(names[i] if i < len(names) else i): v for i, v in enumerate(vals) if v}
        print(f"  {x['role']} dtype {dtype} valid {valid:#x} t {x['t_rx']:.1f}: {nz}")
