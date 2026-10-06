#!/usr/bin/env python3
"""Independently compare the four observed notification frames to explicit bytes."""
import hashlib
import json
from pathlib import Path
import re
import struct

packet = Path(__file__).resolve().parents[1]
text = (packet / "receipts/timing-probe.log").read_text()
frames = []
for tag, time, wire in re.findall(r"R503_TX tag=(\w+) t=(\d+) bytes=([0-9a-f]+)", text):
    got = bytes.fromhex(wire)
    seq = len(frames)
    expected = (bytes.fromhex("0202deadbeef0a0b0c0d0e0f22f0fb010028123456789abcdef07777000000000042")
                + struct.pack(">H", seq)
                + bytes.fromhex("802700090000a1a2a3a4a5a6a7a800001234000700020603000205020002"))
    assert got == expected, tag
    frames.append({"tag": tag, "tx_last": int(time), "bytes": len(got), "sequence_id": seq,
                   "u": got[36] >> 7, "command": hex(int.from_bytes(got[36:38], "big") & 0x7fff),
                   "cdl": int.from_bytes(got[16:18], "big") & 2047,
                   "descriptor_type": int.from_bytes(got[38:40], "big"),
                   "descriptor_index": int.from_bytes(got[40:42], "big"),
                   "sha256": hashlib.sha256(got).hexdigest()})
assert len(frames) == 4
result = {"frames": frames, "independent_byte_comparison": "PASS",
          "minimum_frame_spacing": min(b["tx_last"] - a["tx_last"] for a, b in zip(frames, frames[1:]))}
print(json.dumps(result, indent=2))
