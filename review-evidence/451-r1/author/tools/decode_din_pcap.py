#!/usr/bin/env python3
"""Decode the DUT talker's AAF stream from a pcap (offline, no bench access).

usage: decode_din_pcap.py <pcap> <stream_id_hex> [<json_out>]

Accepts VLAN-tagged or untagged frames. For the named stream it checks the
AAF header (INT32, 48 kHz, 8 channels, 32 bits, 192 bytes), the 8-bit AVTP
sequence (lost PDUs), and decodes the 32-bit big-endian words with the same
pattern rule as the capture decoder: stream channel k is expected to carry a
tag of 1..8 in bits 31:24 and a 16-bit ordinal in bits 23:8. Reports per
stream channel the tag histogram, zero and non-pattern words, torn frames,
and ordinal steps between consecutive non-silent frames.
"""
import collections
import hashlib
import json
import struct
import sys


def main():
    path, sid = sys.argv[1], bytes.fromhex(sys.argv[2])
    raw = open(path, "rb").read()
    magic = raw[:4]
    endian = "<" if magic in (b"\xd4\xc3\xb2\xa1", b"\x4d\x3c\xb2\xa1") else ">"
    nano = magic in (b"\x4d\x3c\xb2\xa1", b"\xa1\xb2\x3c\x4d")
    pos = 24
    pdus = seq_err = hdr_err = vlan_tagged = 0
    other_frames = 0
    prev_seq = None
    tags = [collections.Counter() for _ in range(8)]
    zero = [0] * 8
    bad = [0] * 8
    torn = silent = 0
    steps = collections.Counter()
    prev = None
    first_t = last_t = None
    tu_set = 0
    events = []
    frame_idx = 0
    while pos + 16 <= len(raw):
        sec, frac, incl, orig = struct.unpack(endian + "4I", raw[pos:pos + 16])
        fr = raw[pos + 16:pos + 16 + incl]
        pos += 16 + incl
        t = sec + frac / (1e9 if nano else 1e6)
        off = 12
        et = struct.unpack(">H", fr[off:off + 2])[0]
        tagged = False
        if et == 0x8100:
            tagged = True
            off += 4
            et = struct.unpack(">H", fr[off:off + 2])[0]
        p = fr[off + 2:]
        if et != 0x22F0 or len(p) < 24 or p[0] != 0x02 or p[4:12] != sid:
            other_frames += 1
            continue
        vlan_tagged += tagged
        pdus += 1
        first_t = t if first_t is None else first_t
        last_t = t
        tu_set += p[3] & 1
        if prev_seq is not None and ((p[2] - prev_seq) & 0xFF) != 1:
            seq_err += 1
        prev_seq = p[2]
        if p[16] != 0x02 or (p[17] >> 4) != 5 or (((p[17] & 3) << 8) | p[18]) != 8 or p[19] != 32 \
                or struct.unpack(">H", p[20:22])[0] != 192:
            hdr_err += 1
            continue
        words = struct.unpack(">48I", p[24:216])
        for k in range(6):
            fw = words[k * 8:(k + 1) * 8]
            frame_idx += 1
            if not any(fw):
                silent += 1
                for c in range(8):
                    zero[c] += 1
                continue
            ords = set()
            for c in range(8):
                v = fw[c]
                if v == 0:
                    zero[c] += 1
                    continue
                tg, lo = v >> 24, v & 0xFF
                if lo or not 1 <= tg <= 8:
                    bad[c] += 1
                    continue
                tags[c][tg] += 1
                ords.add((v >> 8) & 0xFFFF)
            if len(ords) != 1:
                torn += 1
                continue
            o = ords.pop()
            if prev is not None:
                d = (o - prev) & 0xFFFF
                key = "+1" if d == 1 else "0 (repeat)" if d == 0 else "+2 (one skipped)" if d == 2 else (
                    "backward" if d > 0x8000 else "forward>2")
                steps[key] += 1
                if d != 1:
                    events.append((frame_idx, t, d if d < 0x8000 else d - 0x10000))
            prev = o
    starts = [e[0] for e in events]
    out = dict(file=path.split("/")[-1], bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest(),
               stream_id=sid.hex(), pdus=pdus, frames=pdus * 6, vlan_tagged_pdus=vlan_tagged,
               span_s=(last_t - first_t) if pdus > 1 else 0, sequence_gaps=seq_err, header_mismatch=hdr_err,
               tu_set_pdus=tu_set, other_frames=other_frames, silent_frames=silent, torn_frames=torn,
               per_stream_channel=[dict(stream_channel=c, tags=dict(sorted(tags[c].items())),
                                        zero_words=zero[c], non_pattern_words=bad[c]) for c in range(8)],
               ordinal_steps=dict(steps), discontinuities=[dict(frame=f, t=round(t, 6), step=d) for f, t, d in events][:400],
               discontinuity_gaps_frames=[b - a for a, b in zip(starts, starts[1:])][:400])
    s = json.dumps(out, indent=1)
    print(s)
    if len(sys.argv) > 3:
        open(sys.argv[3], "w").write(s + "\n")


if __name__ == "__main__":
    main()
