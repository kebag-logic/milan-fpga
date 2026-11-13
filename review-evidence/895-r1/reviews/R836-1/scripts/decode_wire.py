#!/usr/bin/env python3
"""Reviewer's independent decoder of a CPU-budget-harness log's WIRE lines (frames the DUT's mailbox sent).

usage: decode_wire.py LOG [--cpu-hz 100000000]

Each `WIRE <cycle> <interface> <channel> <hex frame>` line is decoded from the bytes alone (no repository code):
- EtherType 0x22EA (MSRP): an MRPDU per IEEE 802.1Q-2018 10.8 (ProtocolVersion, Messages of AttributeType,
  AttributeLength, AttributeListLength, VectorAttributes of a VectorHeader with LeaveAllEvent and NumberOfValues,
  FirstValue, ThreePackedEvents and for the Listener FourPackedEvents, EndMarks). Talker Advertise (type 1, 25 octets)
  and Talker Failed (type 2, 34 octets) FirstValues give StreamID, destination_address, VID, TSpec and, for Failed,
  the FailureInformation (35.2.2.8). Values past the first are FirstValue + k on StreamID and destination_address.
- EtherType 0x22F0, subtype 0xFE (MAAP, IEEE 1722-2016 Annex B): message_type, requested_start_address and count.
- Anything else: EtherType only.
`MARK` lines (the stimulus script's marks) are printed with their time. Times are cycle / cpu_hz in ms.
"""
from __future__ import annotations

import argparse
import sys

EVENTS = ("New", "JoinIn", "In", "JoinMt", "Mt", "Lv")
TYPES = {1: ("TalkerAdvertise", 25), 2: ("TalkerFailed", 34), 3: ("Listener", 8), 4: ("Domain", 4)}


def mrpdu(p: bytes):
    """Yield (attrtype, leaveall, value_bytes, event, listener_subevent) for every value in an MSRP MRPDU."""
    if not p:
        return
    pos = 1  # ProtocolVersion
    while pos + 1 < len(p):
        if p[pos] == 0 and p[pos + 1] == 0:  # the MRPDU's EndMark
            return
        atype, alen = p[pos], p[pos + 1]
        llen = int.from_bytes(p[pos + 2:pos + 4], "big")
        end = pos + 4 + llen
        q = pos + 4
        while q + 1 < end:
            hdr = int.from_bytes(p[q:q + 2], "big")
            if hdr == 0:  # the message's EndMark
                break
            leaveall = hdr >> 13
            n = hdr & 0x1FFF
            q += 2
            first = p[q:q + alen]
            q += alen
            three = p[q:q + (n + 2) // 3]
            q += (n + 2) // 3
            four = b""
            if atype == 3:
                four = p[q:q + (n + 3) // 4]
                q += (n + 3) // 4
            evs = []
            for b in three:
                evs += [b // 36, (b // 6) % 6, b % 6]
            subs = []
            for b in four:
                subs += [(b >> 6) & 3, (b >> 4) & 3, (b >> 2) & 3, b & 3]
            for k in range(n):
                v = bytearray(first)
                if atype in (1, 2, 3):
                    sid = (int.from_bytes(first[0:8], "big") + k) & ((1 << 64) - 1)
                    v[0:8] = sid.to_bytes(8, "big")
                if atype in (1, 2) and k:
                    da = (int.from_bytes(first[8:14], "big") + k) & ((1 << 48) - 1)
                    v[8:14] = da.to_bytes(6, "big")
                yield atype, leaveall, bytes(v), evs[k], (subs[k] if subs else None)
            if n == 0:
                yield atype, leaveall, b"", None, None
        pos = end


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("log")
    ap.add_argument("--cpu-hz", type=int, default=100_000_000)
    a = ap.parse_args()
    per_ms = a.cpu_hz / 1000.0
    counts = {}
    with open(a.log, errors="replace") as fh:
        for line in fh:
            if line.startswith("MARK "):
                parts = line.split()
                # MARK <cycle> <name>, the stimulus script's mark
                print(f"{int(parts[1]) / per_ms:12.3f} MARK {' '.join(parts[2:])}")
                continue
            if not line.startswith("WIRE "):
                continue
            _, cyc, ifc, ch, hexs = line.split()[:5]
            t = int(cyc) / per_ms
            fr = bytes.fromhex(hexs)
            et = int.from_bytes(fr[12:14], "big")
            if et == 0x22EA:
                for atype, la, v, ev, sub in mrpdu(fr[14:]):
                    name = TYPES.get(atype, (f"type{atype}", 0))[0]
                    lat = " LeaveAll" if la else ""
                    evn = EVENTS[ev] if ev is not None and ev < 6 else str(ev)
                    if atype in (1, 2) and v:
                        sid = v[0:8].hex()
                        da = v[8:14].hex()
                        vid = int.from_bytes(v[14:16], "big")
                        mfs = int.from_bytes(v[16:18], "big")
                        mif = int.from_bytes(v[18:20], "big")
                        extra = ""
                        if atype == 2:
                            extra = f" failure bridge {v[25:33].hex()} code {v[33]}"
                        print(f"{t:12.3f} if{ifc} MSRP {name} sid {sid} DA {da} vid {vid} tspec {mfs}/{mif} {evn}{lat}{extra}")
                        counts[(name, evn)] = counts.get((name, evn), 0) + 1
                    elif atype == 4:
                        print(f"{t:12.3f} if{ifc} MSRP Domain {v.hex()} {evn}{lat}")
                    elif atype == 3:
                        print(f"{t:12.3f} if{ifc} MSRP Listener sid {v[0:8].hex()} {evn} sub {sub}{lat}")
                    else:
                        print(f"{t:12.3f} if{ifc} MSRP {name} (no values){lat}")
            elif et == 0x22F0 and fr[14] == 0xFE:
                mt = fr[15] & 0x0F
                start = int.from_bytes(fr[26:32], "big")
                cnt = int.from_bytes(fr[32:34], "big")
                kind = {1: "PROBE", 2: "DEFEND", 3: "ANNOUNCE"}.get(mt, str(mt))
                print(f"{t:12.3f} if{ifc} MAAP {kind} start {start:012x} count {cnt}")
            elif et == 0x22F0:
                print(f"{t:12.3f} if{ifc} AVTP subtype {fr[14]:02x} msg {fr[15] & 0x0F}")
            else:
                print(f"{t:12.3f} if{ifc} ethertype {et:04x}")
    print("COUNTS", sorted(counts.items()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
