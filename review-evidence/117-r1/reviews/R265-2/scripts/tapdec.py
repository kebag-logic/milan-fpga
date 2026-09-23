#!/usr/bin/env python3
"""Independent stdlib decoder for the issue 117 tap and port captures.

Tap records carry a 28-octet envelope ahead of the Ethernet frame: a tag
word 6, a length word, the tap port (3 = sent by the DUT, 2 = sent by the
far end), a spare word, then the tap's nanosecond counter modulo 2^32.
The counter is unwrapped against the pcap host timestamp. A record whose
first word is not 6 or whose port is not 2/3 is counted as host traffic.
Port captures (no envelope) are decoded as plain Ethernet.
"""
import struct

WRAP = 1 << 32
SWITCH = "3cc0c6fffefe0210"
DUT = "020000fffe000001"


def pcap_records(path):
    raw = open(path, "rb").read()
    magic = struct.unpack("<I", raw[:4])[0]
    if magic not in (0xA1B2C3D4, 0xA1B23C4D):
        raise SystemExit(f"{path}: not a little-endian pcap")
    nano = magic == 0xA1B23C4D
    off = 24
    while off + 16 <= len(raw):
        s, f, incl, _orig = struct.unpack("<IIII", raw[off:off + 16])
        off += 16
        yield s * 10**9 + (f if nano else f * 1000), raw[off:off + incl]
        off += incl


def tap_records(path):
    """Yield dicts with host_ns, tap_ns, port, frame; count host records."""
    out, host = [], 0
    first = None
    for host_ns, pkt in pcap_records(path):
        if len(pkt) < 42:
            host += 1
            continue
        tag, _l, port = struct.unpack("<III", pkt[:12])
        if tag != 6 or port not in (2, 3):
            host += 1
            continue
        lo = struct.unpack("<I", pkt[16:20])[0]
        if first is None:
            first = (host_ns, lo)
        k = round(((host_ns - first[0]) - (lo - first[1])) / WRAP)
        out.append(dict(host_ns=host_ns, tap_ns=lo - first[1] + k * WRAP,
                        port=port, frame=pkt[28:]))
    return out, host


def plain_records(path):
    return [dict(host_ns=h, tap_ns=h, port=None, frame=p) for h, p in pcap_records(path)]


def ts10(b):
    return int.from_bytes(b[0:6], "big") * 10**9 + int.from_bytes(b[6:10], "big")


def decode(fr):
    d = {"src": fr[6:12].hex(), "dst": fr[0:6].hex()}
    et = struct.unpack(">H", fr[12:14])[0]
    p = fr[14:]
    d["vlan"] = None
    if et == 0x8100:
        tci = struct.unpack(">H", fr[14:16])[0]
        d["vlan"] = (tci >> 13, tci & 0xFFF)
        et = struct.unpack(">H", fr[16:18])[0]
        p = fr[18:]
    d["et"] = et
    if et == 0x88F7 and len(p) >= 34:
        d["mt"] = p[0] & 0xF
        d["domain"] = p[4]
        d["corr"] = int.from_bytes(p[8:16], "big", signed=True)
        d["sport"] = p[20:28].hex() + ":" + p[28:30].hex()
        d["seq"] = struct.unpack(">H", p[30:32])[0]
        d["logint"] = struct.unpack("b", p[33:34])[0]
        if d["mt"] == 0xB and len(p) >= 64:
            d["prio1"] = p[47]
            d["gm"] = p[53:61].hex()
            d["steps"] = struct.unpack(">H", p[61:63])[0]
            path, o = [], 64
            while o + 4 <= len(p):
                t, ln = struct.unpack(">HH", p[o:o + 4])
                if t == 0x0008:
                    path = [p[o + 4 + 8 * i:o + 12 + 8 * i].hex() for i in range(ln // 8)]
                o += 4 + ln
            d["path"] = path
        if d["mt"] in (0x3, 0xA) and len(p) >= 54:
            d["ts"] = ts10(p[34:44])
            d["reqport"] = p[44:52].hex() + ":" + p[52:54].hex()
    if et == 0x22F0 and len(p) >= 20:
        d["subtype"] = p[0]
        if p[0] == 0x04:
            d["tu"] = p[1] & 1
            d["avtp_seq"] = p[2]
            d["stream"] = p[4:12].hex()
    return d


def host_fit(recs):
    """Least-squares line through per-5 s minima of host_ns - tap_ns."""
    buckets = {}
    for r in recs:
        b = r["tap_ns"] // 5_000_000_000
        v = r["host_ns"] - r["tap_ns"]
        if b not in buckets or v < buckets[b][1]:
            buckets[b] = (r["tap_ns"], v)
    pts = sorted(buckets.values())
    n = len(pts)
    mx = sum(x for x, _ in pts) / n
    my = sum(y for _, y in pts) / n
    sxx = sum((x - mx) ** 2 for x, _ in pts) or 1
    a = sum((x - mx) * (y - my) for x, y in pts) / sxx
    b = my - a * mx
    resid = max(abs(y - (a * x + b)) for x, y in pts)
    return (lambda t: t + a * t + b), resid
