#!/usr/bin/env python3
"""Locate zero and non-idle words outside the DIN own-tag region (reviewer probe)."""
import json, sys
import numpy as np
sys.path.insert(0, __import__("os").path.dirname(__file__))
from r392_decode import pcap_records
import struct
path, sid = sys.argv[1], bytes.fromhex(sys.argv[2])
chunks = []
for pkt in pcap_records(path):
    off = 12
    et = struct.unpack(">H", pkt[off:off+2])[0]
    while et in (0x8100, 0x88A8):
        off += 4; et = struct.unpack(">H", pkt[off:off+2])[0]
    a = pkt[off+2:]
    if et != 0x22F0 or a[0] != 2 or a[4:12] != sid: continue
    sdl = struct.unpack(">H", a[20:22])[0]
    chunks.append(a[24:24+sdl])
w = np.frombuffer(b"".join(chunks), dtype=">u4").reshape(-1, 8)
own = np.arange(1, 9, dtype=np.uint32)[None, :]
allown = np.all(((w & 0xff) == 0) & ((w >> 24) == own), axis=1)
idx = np.nonzero(allown)[0]; a, b = int(idx[0]), int(idx[-1])
zf = np.nonzero(np.any(w == 0, axis=1))[0]
odd = np.nonzero(np.any((w != 0) & (w != 0xffffff00), axis=1) & ~allown)[0]
def runs(ix):
    if ix.size == 0: return []
    br = np.nonzero(np.diff(ix) != 1)[0]
    s = np.concatenate([[ix[0]], ix[br+1]]); e = np.concatenate([ix[br], [ix[-1]]])
    return [[int(x), int(y)] for x, y in zip(s, e)]
out = {"frames": int(w.shape[0]), "region": [a, b],
       "zero_word_frame_runs": runs(zf),
       "non_idle_non_region_frame_runs": runs(odd),
       "frames_around_region_start": [[f"{x:08x}" for x in w[i]] for i in range(max(0,a-3), a+2)],
       "frames_around_region_end": [[f"{x:08x}" for x in w[i]] for i in range(b-1, min(w.shape[0], b+4))],
       "first_frames": [[f"{x:08x}" for x in w[i]] for i in range(0, 3)],
       }
zr = runs(zf)
if zr:
    s0 = zr[0][0]
    out["frames_around_first_zero_run"] = [[f"{x:08x}" for x in w[i]] for i in range(max(0, s0-2), min(w.shape[0], zr[0][1]+3)) if i < s0+3 or i > zr[0][1]-3]
json.dump(out, sys.stdout, indent=1); print()
