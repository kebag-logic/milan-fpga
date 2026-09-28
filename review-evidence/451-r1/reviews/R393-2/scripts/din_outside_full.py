#!/usr/bin/env python3
"""Full word census of a DIN AAF recording outside its playback region.

Selects AVTP AAF PDUs (ethertype 0x22f0, optional 802.1Q tag, subtype 0x02),
requires a single stream_id, unpacks big-endian 32-bit words into frames of
8 channels, locates the playback region (first..last frame in which channel c
carries tag c+1 in bits 31:24 for every c), and reports, for everything
outside it: frame count, word-value census, the maximal all-ffffff00 spans,
and the exact words of every frame that is not all ffffff00.
Usage: din_outside_full.py <recording.pcap>
"""
import collections
import json
import struct
import sys

import numpy as np

data = open(sys.argv[1], "rb").read()
off, pl, sids = 24, [], collections.Counter()
while off + 16 <= len(data):
    incl = struct.unpack_from("<I", data, off + 8)[0]
    off += 16
    pkt = data[off:off + incl]
    off += incl
    p = 18 if pkt[12:14] == b"\x81\x00" else 14
    if pkt[p - 2:p] != b"\x22\xf0" or pkt[p] != 2:
        continue
    sids[pkt[p + 4:p + 12].hex()] += 1
    sdl = struct.unpack_from(">H", pkt, p + 20)[0]
    pl.append(pkt[p + 24:p + 24 + sdl])
assert len(sids) == 1, sids
w = np.frombuffer(b"".join(pl), dtype=">u4").astype(np.uint32).reshape(-1, 8)
n = w.shape[0]
own = np.all((w >> 24) == np.arange(1, 9, dtype=np.uint32), axis=1)
idx = np.nonzero(own)[0]
a, b = int(idx[0]), int(idx[-1])
inside_ok = bool(np.all(own[a:b + 1]))
outside = np.ones(n, bool)
outside[a:b + 1] = False
ow = w[outside]
cen = collections.Counter("%08x" % x for x in ow.ravel().tolist())
idle_frame = np.all(w == 0xFFFFFF00, axis=1)
non_idle_out = [int(i) for i in np.nonzero(outside & ~idle_frame)[0]]


def spans(ix):
    if not ix:
        return []
    r, s, p = [], ix[0], ix[0]
    for i in ix[1:]:
        if i != p + 1:
            r.append([s, p])
            s = i
        p = i
    r.append([s, p])
    return r


idle_out = [int(i) for i in np.nonzero(outside & idle_frame)[0]]
zero_frames = [int(i) for i in np.nonzero(outside & np.all(w == 0, axis=1))[0]]
detail = {str(i): ["%08x" % x for x in w[i]] for i in non_idle_out
          if not np.all(w[i] == 0)}
print(json.dumps({
    "stream_id": list(sids)[0], "pdus": sum(sids.values()), "frames": n,
    "seconds": round(n / 48000, 4),
    "region": [a, b], "region_frames": b - a + 1,
    "region_seconds": round((b - a + 1) / 48000, 4),
    "every_frame_in_region_own_tag": inside_ok,
    "outside_frames": int(outside.sum()), "outside_words": int(ow.size),
    "outside_word_census": dict(cen.most_common()),
    "outside_all_ffffff00_frame_spans": spans(idle_out),
    "outside_non_idle_frame_spans": spans(non_idle_out),
    "outside_all_zero_frame_spans": spans(zero_frames),
    "outside_all_zero_frames": len(zero_frames),
    "outside_partial_frames_words": detail,
}, indent=1))
