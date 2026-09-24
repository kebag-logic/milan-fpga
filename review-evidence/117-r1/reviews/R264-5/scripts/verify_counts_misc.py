#!/usr/bin/env python3
"""Step 2 console-sample health and per-capture host/CRF counts for the Step 3 captures.

Usage: verify_counts_misc.py <117-r1-root>
"""
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verify_step3_cycles import console  # noqa: E402

pk = sys.argv[1]
tot = 0
for rel in ["bench-a200/bench/runA/console.txt", "bench-a200/bench/runB/console.txt", "bench-a200/identity/console-identity.txt", "bench-a200/bench/final/console-final.txt"]:
    s = console(os.path.join(pk, rel))
    tot += len(s)
    bad = [x for x in s if not (x["SYNC"] == "1" and x["ASCAPABLE"] == "1" and x["TU"] == "0" and x["GPTP_GM"] == "3cc0c6fffefe0210")]
    print(rel, "milan_status samples", len(s), "not SYNC=1 ASCAPABLE=1 TU=0 GM=switch:", len(bad))
print("A200 milan_status samples total", tot)


def recs(path):
    raw = open(path, "rb").read()
    off, host, out = 24, 0, []
    while off + 16 <= len(raw):
        _, _, incl, _ = struct.unpack("<IIII", raw[off:off + 16])
        off += 16
        pkt = raw[off:off + incl]
        off += incl
        if len(pkt) >= 42 and struct.unpack("<I", pkt[:4])[0] == 6 and struct.unpack("<I", pkt[8:12])[0] in (2, 3):
            out.append(pkt[28:])
        else:
            host += 1
    return host, out


for c in ["attempt1-aborted/tap-c1.pcap"] + [f"cycle{i}/tap-c{i}.pcap" for i in range(1, 7)] + ["final/tap-final.pcap"]:
    host, out = recs(os.path.join(pk, "bench-a202/bench", c))
    crf = []
    for fr in out:
        et, o = struct.unpack(">H", fr[12:14])[0], 14
        while et == 0x8100:
            et, o = struct.unpack(">H", fr[o + 2:o + 4])[0], o + 4
        if et == 0x22F0 and fr[o] == 0x04:
            crf.append(fr[o + 1] & 1)
    print(c, "host records", host, "CRF PDUs", len(crf), "tu=1", sum(crf))
