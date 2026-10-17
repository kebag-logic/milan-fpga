#!/usr/bin/env python3
"""Lane B21: decode the AAF packets of an inline tap capture (offline, read-only).

Record layout as lane B19's wire_summary.py documents it: tcpdump LINKTYPE_ETHERNET with a 28-byte
tap envelope in front of each frame ([8:12] tap port: 3 = sent by the station on the tapped port's
near side, 2 = sent by the far end; [16:20] tap hardware time, ns modulo 2^32), then the Ethernet
frame without FCS. The tap time is unwrapped against the pcap host time, as there.

AAF (IEEE 1722-2016 7): subtype 0x02 at the AVTPDU's byte 0; sv/version/mr/tv byte 1; sequence_num
byte 2; tu byte 3; stream_id bytes 4-11; avtp_timestamp 12-15; format 16, nsr/channels_per_frame
17-18, bit_depth 19; stream_data_length 20-21; sp/evt 22; reserved 23; samples from 24.

usage:
  b21_aaf.py summary <pcap>                       streams, ports, counts, lengths, rates
  b21_aaf.py extract <pcap> <stream_id> <port> <out_prefix>
      writes <out_prefix>.pkts (per packet <q tap_ns, H seq, I avtp_ts, B tv, B mr, H sdl>) and
      <out_prefix>.samples (the payload words, big-endian on the wire, as uint32 host order)
"""
import struct
import sys
from collections import defaultdict

import numpy as np

WRAP = 1 << 32
PKT = struct.Struct("<qHIBBH")


def records(path):
    with open(path, "rb") as f:
        hdr = f.read(24)
        magic = struct.unpack("<I", hdr[:4])[0]
        if magic not in (0xA1B2C3D4, 0xA1B23C4D):
            raise SystemExit(f"not a little-endian pcap: {magic:#x}")
        nano = magic == 0xA1B23C4D
        first = None
        rh = struct.Struct("<IIII")
        while True:
            h = f.read(16)
            if len(h) < 16:
                break
            ts_s, ts_f, incl, _orig = rh.unpack(h)
            pkt = f.read(incl)
            if len(pkt) < incl:
                break
            host_ns = ts_s * 10**9 + (ts_f if nano else ts_f * 1000)
            if len(pkt) < 28 + 14:
                continue
            tag, _envlen, port = struct.unpack("<III", pkt[:12])
            if tag != 6 or port not in (2, 3):
                continue
            tap_lo = struct.unpack("<I", pkt[16:20])[0]
            if first is None:
                first = (host_ns, tap_lo)
            k = round(((host_ns - first[0]) - (tap_lo - first[1])) / WRAP)
            yield tap_lo - first[1] + k * WRAP, port, pkt[28:], host_ns


def avtp(fr):
    et = struct.unpack(">H", fr[12:14])[0]
    p = 14
    if et == 0x8100:
        et = struct.unpack(">H", fr[16:18])[0]
        p = 18
    if et != 0x22F0:
        return None
    return fr[p:]


def summary(path):
    st = defaultdict(lambda: dict(n=0, lens=defaultdict(int), t0=None, t1=None, seq_gaps=0, last=None))
    other = defaultdict(int)
    for tap_ns, port, fr, _h in records(path):
        a = avtp(fr)
        if a is None or len(a) < 24:
            et = struct.unpack(">H", fr[12:14])[0]
            other[(port, hex(et))] += 1
            continue
        sub = a[0]
        sid = a[4:12].hex()
        k = (sid, port, sub)
        s = st[k]
        s["n"] += 1
        s["lens"][len(a)] += 1
        s["t0"] = tap_ns if s["t0"] is None else s["t0"]
        s["t1"] = tap_ns
        seq = a[2]
        if s["last"] is not None and (seq - s["last"]) & 0xFF != 1:
            s["seq_gaps"] += 1
        s["last"] = seq
        if s["n"] == 1:
            s["first"] = dict(fmt=a[16], nsr_cpf=a[17:19].hex(), depth=a[19], sdl=struct.unpack(">H", a[20:22])[0],
                              head=a[24:56].hex())
    for (sid, port, sub), s in sorted(st.items()):
        dur = (s["t1"] - s["t0"]) / 1e9 if s["n"] > 1 else 0
        print(dict(stream=sid, port=port, subtype=hex(sub), packets=s["n"], seconds=round(dur, 3),
                   rate=round((s["n"] - 1) / dur, 1) if dur else None, avtp_lengths=dict(s["lens"]),
                   seq_gaps=s["seq_gaps"], first=s.get("first")))
    for k, v in sorted(other.items()):
        print(dict(port=k[0], ethertype=k[1], frames=v))


def extract(path, sid, port, prefix):
    sidb = bytes.fromhex(sid)
    port = int(port)
    pk = open(prefix + ".pkts", "wb")
    sm = open(prefix + ".samples", "wb")
    n = 0
    for tap_ns, p, fr, _h in records(path):
        if p != port:
            continue
        a = avtp(fr)
        if a is None or len(a) < 24 or a[0] != 0x02 or a[4:12] != sidb:
            continue
        sdl = struct.unpack(">H", a[20:22])[0]
        pk.write(PKT.pack(tap_ns, a[2], struct.unpack(">I", a[12:16])[0], a[1] & 1, (a[1] >> 3) & 1, sdl))
        body = a[24:24 + sdl]
        sm.write(np.frombuffer(body[: len(body) // 4 * 4], dtype=">u4").astype("<u4").tobytes())
        n += 1
    pk.close()
    sm.close()
    print(dict(stream=sid, port=port, packets=n))


if __name__ == "__main__":
    if sys.argv[1] == "summary":
        summary(sys.argv[2])
    elif sys.argv[1] == "extract":
        extract(*sys.argv[2:6])
    else:
        raise SystemExit(__doc__)
