#!/usr/bin/env python3
"""Census of IPv4/ARP/mDNS frames sourced by the bench switch MAC in every capture.

Usage: switch_addressing.py <evidence-root> <switch-mac-hex, 12 digits>

Handles the tap's 28-octet envelope. Prints, per capture: frames by kind and
source-address class, and for mDNS the DNS record types and whether an SRV record
(a service with a port) is advertised. Never prints names, TXT values or
literal addresses.
"""
import collections
import glob
import os
import struct
import sys

root, mac = sys.argv[1], bytes.fromhex(sys.argv[2])


def frames(path):
    raw = open(path, "rb").read()
    off = 24
    while off + 16 <= len(raw):
        _, _, incl, _ = struct.unpack("<IIII", raw[off:off + 16])
        off += 16
        pkt = raw[off:off + incl]
        off += incl
        if len(pkt) >= 42:
            tag, _, port = struct.unpack("<III", pkt[:12])
            if tag == 6 and port in (2, 3):
                pkt = pkt[28:]
        yield pkt


def aclass(b):
    if b == bytes(4):
        return "unspecified 0.0.0.0"
    if b[0] == 169 and b[1] == 254:
        return "IPv4 link-local"
    return "IPv4 non-link-local"


for p in sorted(glob.glob(os.path.join(root, "**", "*.pcap"), recursive=True)):
    c = collections.Counter()
    for fr in frames(p):
        if len(fr) < 14 or fr[6:12] != mac:
            continue
        et = struct.unpack(">H", fr[12:14])[0]
        if et == 0x0806 and len(fr) >= 42:
            c[("ARP", "sender " + aclass(fr[28:32]))] += 1
        elif et == 0x0800 and len(fr) >= 34:
            src = aclass(fr[26:30])
            proto = fr[23]
            ihl = (fr[14] & 0xF) * 4
            u = 14 + ihl
            kind = {1: "ICMP", 2: "IGMP", 6: "TCP", 17: "UDP"}.get(proto, str(proto))
            if proto == 17 and len(fr) >= u + 8:
                sp, dp = struct.unpack(">HH", fr[u:u + 4])
                kind = f"UDP {sp}->{dp}"
                if 5353 in (sp, dp):
                    d = fr[u + 8:]
                    an, ns, ar = struct.unpack(">HHH", d[6:12])
                    types = collections.Counter()
                    i = 12
                    qd = struct.unpack(">H", d[4:6])[0]

                    def skip(i):
                        while True:
                            ln = d[i]
                            if ln == 0:
                                return i + 1
                            if ln & 0xC0 == 0xC0:
                                return i + 2
                            i += 1 + ln
                    for _ in range(qd):
                        i = skip(i) + 4
                    txt_desc = ""
                    for _ in range(an + ns + ar):
                        i = skip(i)
                        t, _, _, rl = struct.unpack(">HHIH", d[i:i + 10])
                        types[{1: "A", 12: "PTR", 16: "TXT", 33: "SRV", 47: "NSEC", 28: "AAAA"}.get(t, str(t))] += 1
                        if t == 16:
                            rd = d[i + 10:i + 10 + rl]
                            j = 0
                            strs = []
                            while j < len(rd):
                                ln = rd[j]
                                strs.append(rd[j + 1:j + 1 + ln])
                                j += 1 + ln
                            keys = [x.split(b"=", 1)[0] for x in strs]
                            ns_keys = sum(1 for k in keys if b"_" in k)
                            masked_vals = sum(1 for x in strs if b"#" in x)
                            txt_desc = (f"; TXT strings {len(strs)}, keys with a namespace prefix {ns_keys}, "
                                        f"values containing mask octets {masked_vals}")
                        i += 10 + rl
                    kind += " mDNS records " + ",".join(f"{k}x{v}" for k, v in sorted(types.items())) + txt_desc
            c[(kind, "src " + src)] += 1
        else:
            c[(f"ethertype {et:#06x}", "")] += 1
    if c:
        print(os.path.relpath(p, root))
        for k, v in sorted(c.items()):
            print(f"   {v:5d}  {k[0]}  {k[1]}")
