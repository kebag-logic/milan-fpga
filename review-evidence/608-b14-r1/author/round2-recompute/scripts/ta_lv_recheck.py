#!/usr/bin/env python3
"""Recompute the DUT Talker Advertise withdrawal times in item 3 from raw tap bytes.

Independent of the lane analyser: walks the pcap, strips the 28-byte tap record,
times every frame by the tap's own 32-bit nanosecond counter (modular difference,
exact for intervals under 4.29 s), decodes ACMP and MSRP from the frame bytes and
prints, per capture, the DISCONNECT_RX_RESPONSE, the bridge's Listener Lv and the
DUT's Talker Advertise Lv for the DUT's CRF stream, with both intervals.

usage: ta_lv_recheck.py <stream_id_hex> <tap.pcap>...
"""
import struct
import sys

ACMP_DISCONNECT_RX_RESPONSE = 9
EVENTS = ("New", "JoinIn", "In", "JoinMt", "Mt", "Lv")
ATTR = {1: "TalkerAdvertise", 2: "TalkerFailed", 3: "Listener", 4: "Domain"}


def frames(path):
    raw = open(path, "rb").read()
    magic = struct.unpack("<I", raw[:4])[0]
    assert magic in (0xA1B2C3D4, 0xA1B23C4D), hex(magic)
    off = 24
    while off + 16 <= len(raw):
        _s, _f, incl, _o = struct.unpack("<IIII", raw[off:off + 16])
        off += 16
        pkt = raw[off:off + incl]
        off += incl
        if len(pkt) < 42:
            continue
        tag, _l, port = struct.unpack("<III", pkt[:12])
        if tag != 6 or port not in (2, 3):
            continue
        yield struct.unpack("<I", pkt[16:20])[0], port, pkt[28:]


def payload(fr):
    et = struct.unpack(">H", fr[12:14])[0]
    p = fr[14:]
    if et == 0x8100:
        et = struct.unpack(">H", p[2:4])[0]
        p = p[4:]
    return et, p


def msrp_events(p):
    """Yield (attr, event, first_value_bytes, index, leaveall) for every value."""
    assert p[0] == 0
    i = 1
    while i + 4 <= len(p):
        atype, alen = p[i], p[i + 1]
        if atype == 0:
            break
        llen = struct.unpack(">H", p[i + 2:i + 4])[0]
        j = i + 4
        end = j + llen
        while j + 2 <= end:
            hdr = struct.unpack(">H", p[j:j + 2])[0]
            if hdr == 0:
                j += 2
                break
            leaveall = bool(hdr & 0xE000)
            n = hdr & 0x1FFF
            j += 2
            fv = p[j:j + alen]
            j += alen
            nb = (n + 2) // 3
            packed = p[j:j + nb]
            j += nb
            if atype == 3:
                j += (n + 3) // 4
            if n == 0 and leaveall:
                yield ATTR.get(atype), "LeaveAll", fv, 0, True
            for k in range(n):
                b = packed[k // 3]
                ev = (b // 36, (b // 6) % 6, b % 6)[k % 3]
                yield ATTR.get(atype), EVENTS[ev], fv, k, leaveall
        i = end


def main():
    sid = int(sys.argv[1], 16)
    for path in sys.argv[2:]:
        resp = bridge_lv = dut_lv = None
        for tap, port, fr in frames(path):
            et, p = payload(fr)
            if et == 0x22F0 and p[0] == 0xFC and resp is None:
                if p[1] & 0x0F == ACMP_DISCONNECT_RX_RESPONSE:
                    resp = (tap, port, struct.unpack(">H", p[38:40])[0])
            elif et == 0x22EA:
                for attr, ev, fv, k, _la in msrp_events(p):
                    if ev != "Lv" or len(fv) < 8:
                        continue
                    if int.from_bytes(fv[:8], "big") + k != sid:
                        continue
                    if attr == "Listener" and port == 2 and bridge_lv is None:
                        bridge_lv = tap
                    if attr == "TalkerAdvertise" and port == 3 and dut_lv is None:
                        dut_lv = tap

        def d(a, b):
            return ((b - a) & 0xFFFFFFFF) / 1e9

        print(path)
        print(f"  DISCONNECT_RX_RESPONSE port {resp[1]} listener_unique_id {resp[2]}")
        print(f"  bridge Listener Lv after the response      {d(resp[0], bridge_lv):.6f} s")
        if dut_lv is None:
            print("  DUT Talker Advertise Lv: none in the capture")
            continue
        print(f"  DUT Talker Advertise Lv after bridge Lv    {d(bridge_lv, dut_lv):.6f} s")
        print(f"  DUT Talker Advertise Lv after the response {d(resp[0], dut_lv):.6f} s")


if __name__ == "__main__":
    main()
