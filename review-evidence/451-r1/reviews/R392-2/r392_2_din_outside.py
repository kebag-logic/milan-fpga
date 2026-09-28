#!/usr/bin/env python3
"""Reviewer probe (R392-2): what a DIN talker-stream recording holds outside
the playback region, word by word.

Independent of any author tool. Reads a classic pcap, keeps AAF PDUs of the
given stream ID, and rebuilds the 8-channel frame sequence. The playback
region is the first to the last frame in which all eight channels carry their
own tag (bits 31:24 = channel + 1, bits 7:0 zero), the page's definition.
Prints the outside-region frame and word census, the zero-word runs, the
boundary frames, and the capture's first and last packet times.

Usage: r392_2_din_outside.py recording.pcap <stream-id-hex>
"""
import json, struct, sys
import numpy as np

path, sid = sys.argv[1], bytes.fromhex(sys.argv[2])
chunks, t_first, t_last, pdus = [], None, None, 0
with open(path, "rb") as f:
    gh = f.read(24)
    e = "<" if struct.unpack("<I", gh[:4])[0] in (0xA1B2C3D4, 0xA1B23C4D) else ">"
    nano = struct.unpack(e + "I", gh[:4])[0] == 0xA1B23C4D
    while True:
        h = f.read(16)
        if len(h) < 16:
            break
        ts, tf, incl, _ = struct.unpack(e + "IIII", h)
        pkt = f.read(incl)
        off = 12
        et = struct.unpack(">H", pkt[off:off + 2])[0]
        while et in (0x8100, 0x88A8):
            off += 4
            et = struct.unpack(">H", pkt[off:off + 2])[0]
        a = pkt[off + 2:]
        if et != 0x22F0 or a[0] != 2 or a[4:12] != sid:
            continue
        t = ts + tf / (1e9 if nano else 1e6)
        t_first = t if t_first is None else t_first
        t_last = t
        pdus += 1
        sdl = struct.unpack(">H", a[20:22])[0]
        chunks.append(a[24:24 + sdl])
w = np.frombuffer(b"".join(chunks), dtype=">u4").reshape(-1, 8)
n = w.shape[0]
own = np.arange(1, 9, dtype=np.uint32)[None, :]
allown = np.all(((w & 0xFF) == 0) & ((w >> 24) == own), axis=1)
idx = np.nonzero(allown)[0]
out = {"pdus": pdus, "frames": int(n), "seconds_at_48k": round(n / 48000, 4),
       "first_packet_epoch": t_first, "last_packet_epoch": t_last,
       "packet_span_s": None if t_first is None else round(t_last - t_first, 3)}


def runs(ix):
    if ix.size == 0:
        return []
    br = np.nonzero(np.diff(ix) != 1)[0]
    s = np.concatenate([[ix[0]], ix[br + 1]]); e2 = np.concatenate([ix[br], [ix[-1]]])
    return [[int(x), int(y)] for x, y in zip(s, e2)]


def hexf(i):
    return [f"{x:08x}" for x in w[i]]


if idx.size == 0:
    vals, cnts = np.unique(w, return_counts=True)
    out["region"] = None
    out["word_census"] = {f"{v:08x}": int(c) for v, c in zip(vals, cnts)}
else:
    a0, b0 = int(idx[0]), int(idx[-1])
    mask = np.ones(n, bool); mask[a0:b0 + 1] = False
    ow = w[mask]
    vals, cnts = np.unique(ow, return_counts=True)
    census = {f"{v:08x}": int(c) for v, c in zip(vals, cnts)}
    others = {k: v for k, v in census.items() if k not in ("00000000", "ffffff00")}
    idle = np.all(w == 0xFFFFFF00, axis=1)
    zero_any = np.any(w == 0, axis=1)
    all_zero = np.all(w == 0, axis=1)
    tail = runs(np.nonzero(zero_any & mask)[0])
    out.update({
        "region": [a0, b0], "region_frames": b0 - a0 + 1,
        "region_not_all_own_frames": int(np.sum(~allown[a0:b0 + 1])),
        "outside_frames": int(mask.sum()), "outside_words": int(ow.size),
        "outside_word_census_idle_zero": {k: census.get(k, 0) for k in ("ffffff00", "00000000")},
        "outside_other_words": others, "outside_other_word_count": int(sum(others.values())),
        "outside_all_idle_frame_runs": runs(np.nonzero(idle & mask)[0]),
        "outside_frames_with_zero_word_runs": tail,
        "outside_all_zero_frame_runs": runs(np.nonzero(all_zero & mask)[0]),
        "frame_before_region": {str(a0 - 1): hexf(a0 - 1)},
        "last_region_frame": {str(b0): hexf(b0)},
        "tail_first_frames": {str(i): hexf(i) for i in range(b0 + 1, b0 + 3)},
        "tail_last_frames": {str(i): hexf(i) for i in range(tail[-1][1] - 1, tail[-1][1] + 2)} if tail else {},
    })
    if tail:
        s, e3 = tail[-1]
        out["stop_tail"] = {"first": s, "last": e3, "frames": e3 - s + 1,
                            "ms": round((e3 - s + 1) / 48.0, 2),
                            "zero_words": int(np.sum(w[s:e3 + 1] == 0)),
                            "all_zero_frames": int(np.sum(all_zero[s:e3 + 1]))}
json.dump(out, sys.stdout, indent=1); print()
