#!/usr/bin/env python3
"""Distinct grandmaster Announce field tuples in the A200 Run A tap capture.

usage: announce_fields.py <bench-a200 dir>
"""
import collections
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import tapdec as T  # noqa: E402

recs, _h = T.tap_records(Path(sys.argv[1]) / "bench/runA/tap-runA.pcap")
seen = collections.Counter()
for r in recs:
    fr = r["frame"]
    et = struct.unpack(">H", fr[12:14])[0]
    p = fr[14:] if et != 0x8100 else fr[18:]
    if r["port"] == 2 and struct.unpack(">H", fr[12:14])[0] == 0x88F7 and p[0] & 0xF == 0xB:
        seen[(p[47], p[48], hex(p[49]), hex(struct.unpack(">H", p[50:52])[0]), p[52],
              p[53:61].hex(), struct.unpack(">H", p[61:63])[0], hex(p[63]))] += 1
for k, v in seen.items():
    print(f"{v} Announces: priority1 {k[0]}, clockClass {k[1]}, clockAccuracy {k[2]}, "
          f"offsetScaledLogVariance {k[3]}, priority2 {k[4]}, grandmasterIdentity {k[5]}, "
          f"stepsRemoved {k[6]}, timeSource {k[7]}")
