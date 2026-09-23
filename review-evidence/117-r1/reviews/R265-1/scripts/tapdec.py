#!/usr/bin/env python3
"""Reviewer-owned, independent decoder for the #117 inline-tap captures.

Written from the frame formats (IEEE 802.1AS / 1588 common header, IEEE
1722 CRF header, IEEE 1722.1 ADP) and from the byte layout observed in the
published captures, not from the author's decoder. The tap prepends an
envelope to each Ethernet frame; this module locates it by its observed
shape: a little-endian tag word 6, a port word 2 or 3, a 32-bit nanosecond
counter at offset 16, and the frame from offset 28 (checked against the
Ethernet destination/ethertype of every frame it accepts).

Tap time is unwrapped incrementally: each step adds the modulo-2^32
difference of the counter plus the number of whole wraps that the pcap host
time says elapsed between the two records. Records with no envelope are
counted and excluded.
"""
import struct

WRAP = 1 << 32


def pcap_records(path):
    raw = open(path, "rb").read()
    magic = struct.unpack("<I", raw[:4])[0]
    if magic == 0xA1B2C3D4:
        nano = False
    elif magic == 0xA1B23C4D:
        nano = True
    else:
        raise SystemExit(f"{path}: unsupported pcap magic {magic:#x}")
    linktype = struct.unpack("<I", raw[20:24])[0]
    off = 24
    while off + 16 <= len(raw):
        s, f, incl, orig = struct.unpack("<IIII", raw[off:off + 16])
        off += 16
        pkt = raw[off:off + incl]
        off += incl
        yield (s * 10**9 + (f if nano else f * 1000)), pkt, linktype


def tap_frames(path):
    """Yield dicts: host_ns, tap_ns, port, frame. Plus a final stats dict."""
    prev = None
    host_only = 0
    n = 0
    for host_ns, pkt, _lt in pcap_records(path):
        if len(pkt) >= 42:
            tag, _l, port = struct.unpack("<III", pkt[:12])
        else:
            tag = port = None
        if tag != 6 or port not in (2, 3):
            host_only += 1
            continue
        lo = struct.unpack("<I", pkt[16:20])[0]
        if prev is None:
            tap = lo
        else:
            phost, plo, ptap = prev
            d = (lo - plo) % WRAP
            k = round(((host_ns - phost) - d) / WRAP)
            tap = ptap + d + k * WRAP
        prev = (host_ns, lo, tap)
        n += 1
        yield dict(host_ns=host_ns, tap_ns=tap, port=port, frame=pkt[28:])
    yield dict(stats=True, tapped=n, host_only=host_only)


def ts80(b):
    return int.from_bytes(b[0:6], "big") * 10**9 + int.from_bytes(b[6:10], "big")


def decode(fr):
    d = dict(dst=fr[0:6].hex(), src=fr[6:12].hex())
    et = struct.unpack(">H", fr[12:14])[0]
    p = fr[14:]
    d["vlan"] = None
    if et == 0x8100:
        tci = struct.unpack(">H", fr[14:16])[0]
        d["vlan"] = (tci >> 13, tci & 0xFFF)
        et = struct.unpack(">H", fr[16:18])[0]
        p = fr[18:]
    d["et"] = et
    d["kind"] = f"et{et:04x}"
    if et == 0x88F7 and len(p) >= 34:
        mt = p[0] & 0x0F
        d["kind"] = "ptp"
        d["mt"] = mt
        d["domain"] = p[4]
        d["corr"] = int.from_bytes(p[8:16], "big", signed=True)  # scaled ns (2^-16)
        d["spid"] = p[20:30].hex()
        d["seq"] = struct.unpack(">H", p[30:32])[0]
        d["logi"] = struct.unpack("b", p[33:34])[0]
        d["msglen"] = struct.unpack(">H", p[2:4])[0]
        if mt in (0, 2, 3, 8, 0xA, 0xB) and len(p) >= 44:
            d["ts"] = ts80(p[34:44])
        if mt in (3, 0xA) and len(p) >= 54:
            d["reqpid"] = p[44:54].hex()
        if mt == 0xB and len(p) >= 64:
            d["p1"] = p[47]
            d["cls"] = p[48]
            d["acc"] = p[49]
            d["var"] = struct.unpack(">H", p[50:52])[0]
            d["p2"] = p[52]
            d["gm"] = p[53:61].hex()
            d["steps"] = struct.unpack(">H", p[61:63])[0]
            d["tsrc"] = p[63]
            o, end, path = 64, min(d["msglen"], len(p)), None
            while o + 4 <= end:
                t, ln = struct.unpack(">HH", p[o:o + 4])
                if t == 0x0008:
                    body = p[o + 4:o + 4 + ln]
                    path = [body[i:i + 8].hex() for i in range(0, len(body), 8)]
                o += 4 + ln
                if ln == 0:
                    break
            d["path"] = path
    elif et == 0x22F0 and len(p) >= 12:
        sub = p[0]
        if sub == 0x04:
            d["kind"] = "crf"
            d["tu"] = p[1] & 1
            d["seq"] = p[2]
            d["sid"] = p[4:12].hex()
        elif sub == 0x02:
            d["kind"] = "aaf"
            d["tu"] = p[3] & 1
            d["seq"] = p[2]
            d["sid"] = p[4:12].hex()
        elif sub == 0xFA and len(p) >= 58:
            d["kind"] = "adp"
            d["adpmsg"] = p[1] & 0x0F
            d["eid"] = p[4:12].hex()
            d["avail"] = struct.unpack(">I", p[36:40])[0]
            d["gm"] = p[40:48].hex()
        elif sub == 0xFB:
            d["kind"] = "aecp"
        elif sub == 0xFC:
            d["kind"] = "acmp"
            d["acmpmsg"] = p[1] & 0x0F
            d["status"] = p[2] >> 3
        elif sub == 0xFE:
            d["kind"] = "maap"
        else:
            d["kind"] = f"avtp{sub:02x}"
    elif et == 0x22EA:
        d["kind"] = "msrp"
    return d


def load(path):
    """Return (list of decoded records sorted by tap time, stats)."""
    out, stats = [], None
    for r in tap_frames(path):
        if r.get("stats"):
            stats = r
            continue
        d = decode(r["frame"])
        d.update(host_ns=r["host_ns"], tap_ns=r["tap_ns"], port=r["port"])
        out.append(d)
    out.sort(key=lambda x: x["tap_ns"])
    return out, stats
