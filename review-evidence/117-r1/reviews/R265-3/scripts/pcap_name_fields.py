#!/usr/bin/env python3
"""Census of name-bearing protocol fields in classic pcap files.

Usage: pcap_name_fields.py [--show] <pcap>...

For DHCP (UDP 67/68) options 12, 15, 43, 60, 61, 77, 81 and LLDP TLVs 1, 2, 4,
5, 6, 127, and for any mDNS/SSDP/NetBIOS/CDP frame, reports per field the count
and the byte-class composition of the values: masked octets ('#'), printable,
other. Values are printed only with --show (for a private terminal, never for a
published receipt).
"""
import struct
import sys
from collections import defaultdict


def packets(path):
    with open(path, "rb") as f:
        hdr = f.read(24)
        magic = struct.unpack("<I", hdr[:4])[0]
        if magic in (0xA1B2C3D4, 0xA1B23C4D):
            e = "<"
        elif magic in (0xD4C3B2A1, 0x4D3CB2A1):
            e = ">"
        else:
            raise SystemExit(f"{path}: not classic pcap")
        while True:
            ph = f.read(16)
            if len(ph) < 16:
                return
            _, _, incl, _ = struct.unpack(e + "IIII", ph)
            pkt = f.read(incl)
            # strip the capture tap's 28-octet envelope when present
            if len(pkt) >= 42:
                tag, _, port = struct.unpack("<III", pkt[:12])
                if tag == 6 and port in (2, 3):
                    pkt = pkt[28:]
            yield pkt


def classify(v):
    masked = sum(1 for c in v if c == 0x23)
    printable = sum(1 for c in v if 0x20 <= c < 0x7F and c != 0x23)
    other = len(v) - masked - printable
    return masked, printable, other


def main():
    show = "--show" in sys.argv
    files = [a for a in sys.argv[1:] if a != "--show"]
    census = defaultdict(lambda: [0, 0, 0, 0, set()])
    other_proto = defaultdict(int)
    nframes = 0
    for p in files:
        for fr in packets(p):
            nframes += 1
            if len(fr) < 14:
                continue
            et = struct.unpack(">H", fr[12:14])[0]
            off = 14
            if et == 0x8100 and len(fr) >= 18:
                et = struct.unpack(">H", fr[16:18])[0]
                off = 18
            if et == 0x88CC:
                i = off
                while i + 2 <= len(fr):
                    th = struct.unpack(">H", fr[i:i + 2])[0]
                    t, ln = th >> 9, th & 0x1FF
                    if t == 0:
                        break
                    v = fr[i + 2:i + 2 + ln]
                    if t in (1, 2, 4, 5, 6, 8, 127):
                        k = f"LLDP TLV {t}"
                        m, pr, ot = classify(v)
                        c = census[k]
                        c[0] += 1; c[1] += m; c[2] += pr; c[3] += ot
                        if show:
                            c[4].add(v)
                    i += 2 + ln
                continue
            if et == 0x0800 and len(fr) >= off + 20:
                ihl = (fr[off] & 0xF) * 4
                proto = fr[off + 9]
                if proto != 17:
                    continue
                u = off + ihl
                sp, dp = struct.unpack(">HH", fr[u:u + 4])
                if {sp, dp} & {67, 68}:
                    b = u + 8
                    opts = b + 240
                    if fr[b + 236:b + 240] != b"\x63\x82\x53\x63":
                        continue
                    sname = fr[b + 44:b + 108].rstrip(b"\0")
                    if sname:
                        k = "DHCP sname"
                        m, pr, ot = classify(sname)
                        c = census[k]; c[0] += 1; c[1] += m; c[2] += pr; c[3] += ot
                    i = opts
                    while i < len(fr):
                        o = fr[i]
                        if o == 255:
                            break
                        if o == 0:
                            i += 1
                            continue
                        ln = fr[i + 1]
                        v = fr[i + 2:i + 2 + ln]
                        if o in (12, 15, 43, 60, 61, 77, 81):
                            k = f"DHCP option {o}"
                            m, pr, ot = classify(v)
                            c = census[k]; c[0] += 1; c[1] += m; c[2] += pr; c[3] += ot
                            if show:
                                c[4].add(v)
                        i += 2 + ln
                elif {sp, dp} & {5353, 1900, 137, 138, 5355}:
                    other_proto[f"UDP {min(sp, dp) if min(sp,dp) in (137,138) else (sp if sp in (5353,1900,5355) else dp)}"] += 1
            elif et in (0x2000,) or (len(fr) >= 22 and fr[14:17] == b"\xaa\xaa\x03" and fr[20:22] == b"\x20\x00"):
                other_proto["CDP"] += 1
    print(f"files {len(files)}, frames {nframes}")
    for k in sorted(census):
        n, m, pr, ot, vals = census[k]
        print(f"  {k:16s} occurrences {n:6d}  masked-octets {m:7d}  printable {pr:7d}  other {ot:7d}  distinct-values {len(vals) if show else '-'}")
        if show:
            for v in sorted(vals):
                print("      ", v)
    for k in sorted(other_proto):
        print(f"  other name-bearing protocol {k}: {other_proto[k]} frames")


if __name__ == "__main__":
    main()
