#!/usr/bin/env python3
"""Locate non-idle words outside the DIN playback region of an AAF recording.
Usage: din_outside_census.py <recording.pcap> <stream_id_hex> <first_frame> <last_frame>"""
import struct, sys, json
import numpy as np
path, sid = sys.argv[1], bytes.fromhex(sys.argv[2]); a, b = int(sys.argv[3]), int(sys.argv[4])
data = open(path, "rb").read(); off = 24; pl = []
while off + 16 <= len(data):
    incl = struct.unpack_from("<I", data, off + 8)[0]; off += 16; pkt = data[off:off + incl]; off += incl
    p = 18 if pkt[12:14] == b"\x81\x00" else 14
    if pkt[p - 2:p] != b"\x22\xf0" or pkt[p] != 2 or pkt[p + 4:p + 12] != sid: continue
    sdl = struct.unpack_from(">H", pkt, p + 20)[0]; pl.append(pkt[p + 24:p + 24 + sdl])
w = np.frombuffer(b"".join(pl), dtype=">u4").reshape(-1, 8)
def runs(mask):
    idx = np.nonzero(mask)[0]
    if idx.size == 0: return []
    br = np.nonzero(np.diff(idx) != 1)[0]
    st = np.concatenate([[idx[0]], idx[br + 1]]); en = np.concatenate([idx[br], [idx[-1]]])
    return [[int(s), int(e)] for s, e in zip(st, en)]
zero_any = np.any(w == 0, axis=1)
odd = ~np.all((w == 0xFFFFFF00) | (w == 0), axis=1)
out = {"frames": int(w.shape[0]), "region": [a, b],
       "frame_runs_with_any_zero_word": runs(zero_any)[:20],
       "frame_runs_not_idle_or_zero_outside_region": [r for r in runs(odd) if r[1] < a or r[0] > b][:20],
       "frames_around_region_start": [[("%08x" % x) for x in row] for row in w[a - 3:a + 2]],
       "frames_around_region_end": [[("%08x" % x) for x in row] for row in w[b - 1:b + 4]],
       "first_frames": [[("%08x" % x) for x in row] for row in w[:2]]}
print(json.dumps(out, indent=1))
