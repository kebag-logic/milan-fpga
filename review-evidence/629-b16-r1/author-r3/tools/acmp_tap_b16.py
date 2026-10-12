#!/usr/bin/env python3
"""Lane B16 (new, offline): list the ACMP messages (IEEE 1722.1 clause 8, AVTP subtype 0xFC) in a tap capture
with the tap's 28-byte record header (direction port at header bytes 8-11, little-endian), and count the AVTP
stream PDUs per stream ID and port. Read-only.

usage: acmp_tap_b16.py <pcap> <out.json>
"""
import json
import struct
import sys

TAPHDR = 28
MT = {0: "CONNECT_TX_COMMAND", 1: "CONNECT_TX_RESPONSE", 2: "DISCONNECT_TX_COMMAND", 3: "DISCONNECT_TX_RESPONSE",
      4: "GET_TX_STATE_COMMAND", 5: "GET_TX_STATE_RESPONSE", 6: "CONNECT_RX_COMMAND", 7: "CONNECT_RX_RESPONSE",
      8: "DISCONNECT_RX_COMMAND", 9: "DISCONNECT_RX_RESPONSE", 10: "GET_RX_STATE_COMMAND", 11: "GET_RX_STATE_RESPONSE",
      12: "GET_TX_CONNECTION_COMMAND", 13: "GET_TX_CONNECTION_RESPONSE"}


def records(d):
    magic = struct.unpack("<I", d[:4])[0]
    off = 24
    while off + 16 <= len(d):
        ts, tu, incl, orig = struct.unpack("<IIII", d[off:off + 16])
        yield ts + tu * (1e-9 if magic == 0xA1B23C4D else 1e-6), d[off + 16:off + 16 + incl]
        off += 16 + incl


def main():
    d = open(sys.argv[1], "rb").read()
    acmp, streams, t0 = [], {}, None
    for t, p in records(d):
        if len(p) < TAPHDR + 18:
            continue
        t0 = t if t0 is None else t0
        port = struct.unpack("<I", p[8:12])[0]
        f = p[TAPHDR:]
        et, b = f[12:14], 14
        if et == b"\x81\x00":
            et, b = f[16:18], 18
        if et != b"\x22\xf0":
            continue
        a = f[b:]
        sub = a[0]
        if sub == 0xFC and len(a) >= 56:
            mt = a[1] & 0x0F
            st = a[2] >> 3
            rec = dict(t=round(t - t0, 6), port=port, src=f[6:12].hex(), dst=f[0:6].hex(), msg=MT.get(mt, mt), status=st,
                       stream_id=a[4:12].hex(), controller=a[12:20].hex(), talker=a[20:28].hex(), listener=a[28:36].hex(),
                       talker_uid=struct.unpack(">H", a[36:38])[0], listener_uid=struct.unpack(">H", a[38:40])[0],
                       dmac=a[40:46].hex(), conn_count=struct.unpack(">H", a[46:48])[0], seq=struct.unpack(">H", a[48:50])[0],
                       flags=f"0x{struct.unpack('>H', a[50:52])[0]:04x}")
            if mt not in (10, 11, 4, 5):
                acmp.append(rec)
            else:
                acmp.append(dict(t=rec["t"], port=port, msg=rec["msg"], talker=rec["talker"], listener=rec["listener"],
                                 listener_uid=rec["listener_uid"], talker_uid=rec["talker_uid"], status=st))
        elif sub in (0x02, 0x04) and len(a) >= 12:
            k = f"{a[4:12].hex()} subtype={sub:#04x} port={port}"
            streams[k] = streams.get(k, 0) + 1
    out = dict(file=sys.argv[1].split("/")[-1], acmp=acmp, stream_pdus=streams)
    json.dump(out, open(sys.argv[2], "w"), indent=1)
    for r in acmp:
        print(json.dumps(r))
    print(json.dumps(streams))


if __name__ == "__main__":
    main()
