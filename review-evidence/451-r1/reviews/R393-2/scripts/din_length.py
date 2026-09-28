#!/usr/bin/env python3
"""Frame count, duration and word-value census of DIN AAF recordings.
Usage: din_length.py <recording.pcap> [...]"""
import collections
import json
import struct
import sys

import numpy as np

out = {}
for path in sys.argv[1:]:
    data = open(path, "rb").read()
    off, pl = 24, []
    while off + 16 <= len(data):
        incl = struct.unpack_from("<I", data, off + 8)[0]
        off += 16
        pkt = data[off:off + incl]
        off += incl
        p = 18 if pkt[12:14] == b"\x81\x00" else 14
        if pkt[p - 2:p] != b"\x22\xf0" or pkt[p] != 2:
            continue
        sdl = struct.unpack_from(">H", pkt, p + 20)[0]
        pl.append(pkt[p + 24:p + 24 + sdl])
    w = np.frombuffer(b"".join(pl), dtype=">u4").reshape(-1, 8)
    vals = collections.Counter("%08x" % x for x in np.unique(w).tolist())
    out[path.split("/")[-1]] = {"frames": int(w.shape[0]),
                                "seconds": round(w.shape[0] / 48000, 4),
                                "distinct_word_values": sorted(vals)}
print(json.dumps(out, indent=1))
