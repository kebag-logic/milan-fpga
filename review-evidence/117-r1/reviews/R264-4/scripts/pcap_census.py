#!/usr/bin/env python3
"""Protocol and name-field census of the classic-pcap captures of an evidence
archive, for a bench-identity review.

usage: pcap_census.py <root> <public-out.txt> <private-out.txt>

The public output carries only counts, protocol names, service types, field
KEYS and whether each value is masked; the private output (keep in scratch)
also carries the decoded name and string VALUES for the reviewer to inspect.
Tap records open with a 28-octet envelope (u32 type 6, u32 block length,
u32 port, two u32 time words, u32 captured and u32 original length); a record
without one is the capture host's own frame and is decoded as plain Ethernet.
"""
import collections
import os
import re
import struct
import sys

MASK_RE = re.compile(rb"^[#*xX_.\- 0<>]*$|<[^>]*>")


def records(path):
    d = open(path, "rb").read()
    magic = struct.unpack("<I", d[:4])[0]
    end = "<" if magic in (0xA1B2C3D4, 0xA1B23C4D) else ">"
    lt = struct.unpack(end + "I", d[20:24])[0]
    off = 24
    while off + 16 <= len(d):
        _, _, incl, _ = struct.unpack(end + "IIII", d[off:off + 16])
        off += 16
        yield lt, d[off:off + incl]
        off += incl


def split_envelope(pkt):
    if len(pkt) >= 28:
        typ, _blk, port, _t1, _t2, cap, orig = struct.unpack("<7I", pkt[:28])
        if typ == 6 and cap == orig and 28 + cap <= len(pkt) and cap >= 14:
            return f"tap-port{port}", pkt[28:28 + cap]
    return "host", pkt


def dns_name(buf, off, depth=0):
    labels = []
    jumped = False
    ret = off
    while off < len(buf) and depth < 20:
        n = buf[off]
        if n == 0:
            off += 1
            break
        if n & 0xC0 == 0xC0:
            ptr = ((n & 0x3F) << 8) | buf[off + 1]
            if not jumped:
                ret = off + 2
            jumped = True
            off = ptr
            depth += 1
            continue
        labels.append(buf[off + 1:off + 1 + n])
        off += 1 + n
    return b".".join(labels), (ret if jumped else off)


def parse_dns(p, pub, priv, tag):
    if len(p) < 12:
        return
    qd, an, ns, ar = struct.unpack(">HHHH", p[4:12])
    off = 12
    for _ in range(qd):
        name, off = dns_name(p, off)
        off += 4
        priv[tag].add(b"Q " + name)
        pub[tag + " question name label-count"][name.count(b".") + 1] += 1
    for _ in range(an + ns + ar):
        if off >= len(p):
            break
        name, off = dns_name(p, off)
        if off + 10 > len(p):
            break
        typ, _cls, _ttl, rdl = struct.unpack(">HHIH", p[off:off + 10])
        off += 10
        rd = p[off:off + rdl]
        off += rdl
        priv[tag].add(b"RR%d " % typ + name)
        pub[tag + " rr-type"][typ] += 1
        if typ == 16:  # TXT
            i = 0
            while i < len(rd):
                n = rd[i]
                s = rd[i + 1:i + 1 + n]
                i += 1 + n
                key = s.split(b"=", 1)[0]
                val = s.split(b"=", 1)[1] if b"=" in s else b""
                priv[tag].add(b"TXT " + s)
                masked = bool(MASK_RE.search(val)) or not val
                pub[tag + " TXT key (value masked?)"][(key_shape(key), masked)] += 1
        elif typ in (12, 33):
            tgt, _ = dns_name(p, off - rdl + (6 if typ == 33 else 0))
            priv[tag].add(b"RDATA%d " % typ + tgt)
        elif typ in (1, 28):
            pub[tag + " address record"][typ] += 1


def key_shape(k):
    """Publishable form of a TXT key: its shape, not its text."""
    return re.sub(rb"[a-z]", b"a", re.sub(rb"[A-Z]", b"A", re.sub(rb"[0-9]", b"9", k))).decode("latin-1")


def ipv4_class(a):
    if a[0] == 169 and a[1] == 254:
        return "link-local"
    if a[0] == 10 or (a[0] == 172 and 16 <= a[1] < 32) or (a[0] == 192 and a[1] == 168):
        return "private"
    if 224 <= a[0] < 240:
        return "multicast"
    if a == b"\0\0\0\0":
        return "unspecified"
    if a == b"\xff\xff\xff\xff":
        return "broadcast"
    return "other"


def strings(b, n=5):
    return re.findall(rb"[\x20-\x7e]{%d,}" % n, b)


def main():
    root, pubf, privf = sys.argv[1:4]
    pub = collections.defaultdict(collections.Counter)
    priv = collections.defaultdict(set)
    nfiles = 0
    for dp, _, fns in os.walk(root):
        for fn in sorted(fns):
            if not fn.endswith(".pcap"):
                continue
            nfiles += 1
            path = os.path.join(dp, fn)
            rel = os.path.relpath(path, root)
            for lt, pkt in records(path):
                where, fr = split_envelope(pkt)
                pub["records by origin"][where] += 1
                if lt != 1 or len(fr) < 14:
                    pub["non-ethernet"][lt] += 1
                    continue
                et = struct.unpack(">H", fr[12:14])[0]
                off = 14
                while et in (0x8100, 0x88A8) and len(fr) >= off + 4:
                    et = struct.unpack(">H", fr[off + 2:off + 4])[0]
                    off += 4
                p = fr[off:]
                pub["ethertype"][hex(et)] += 1
                if et == 0x0800 and len(p) >= 20:
                    ihl = (p[0] & 15) * 4
                    proto = p[9]
                    for a in (p[12:16], p[16:20]):
                        pub["ipv4 address class"][ipv4_class(a)] += 1
                        priv["ipv4"].add(".".join(str(x) for x in a).encode())
                    l4 = p[ihl:]
                    pub["ipv4 proto"][proto] += 1
                    if proto == 17 and len(l4) >= 8:
                        sp, dpt = struct.unpack(">HH", l4[:4])
                        port = min(sp, dpt)
                        pub["udp port"][port] += 1
                        body = l4[8:]
                        if 5353 in (sp, dpt) or 5355 in (sp, dpt) or 53 in (sp, dpt):
                            parse_dns(body, pub, priv, "dns-family")
                        elif port in (67, 68):
                            i = 240
                            while i + 2 <= len(body) and body[i] != 255:
                                if body[i] == 0:
                                    i += 1
                                    continue
                                o, ln = body[i], body[i + 1]
                                val = body[i + 2:i + 2 + ln]
                                pub["dhcp option"][o] += 1
                                if o in (12, 15, 43, 60, 61, 81):
                                    priv["dhcp"].add(b"opt%d " % o + val)
                                i += 2 + ln
                        else:
                            for s in strings(body):
                                priv[f"udp{port}-strings"].add(s)
                    elif proto == 6:
                        pub["tcp"]["segments"] += 1
                    elif proto == 2:
                        pub["igmp"]["messages"] += 1
                elif et == 0x86DD and len(p) >= 40:
                    nh = p[6]
                    pub["ipv6 next header"][nh] += 1
                    if nh == 17 and len(p) >= 48:
                        sp, dpt = struct.unpack(">HH", p[40:44])
                        pub["udp6 port"][min(sp, dpt)] += 1
                        if 5353 in (sp, dpt) or 5355 in (sp, dpt):
                            parse_dns(p[48:], pub, priv, "dns-family")
                elif et == 0x0806 and len(p) >= 28:
                    for a in (p[14:18], p[24:28]):
                        pub["arp address class"][ipv4_class(a)] += 1
                        priv["ipv4"].add(".".join(str(x) for x in a).encode())
                elif et == 0x88CC:
                    i = 0
                    while i + 2 <= len(p):
                        t = p[i] >> 1
                        ln = ((p[i] & 1) << 8) | p[i + 1]
                        if t == 0:
                            break
                        pub["lldp tlv"][t] += 1
                        priv["lldp"].add(b"tlv%d " % t + p[i + 2:i + 2 + ln])
                        i += 2 + ln
                elif et == 0x22F0 and len(p) >= 1:
                    sub = p[0] & 0x7F
                    pub["avtp subtype"][hex(sub)] += 1
                    if sub in (0x7A, 0x7B, 0x7C, 0xFA, 0xFB, 0xFC):
                        for s in strings(p, 4):
                            priv[f"avdecc-strings-{rel.split('/')[0]}"].add(s)
                elif et not in (0x88F7, 0x22EA, 0x88F5, 0x22F0):
                    for s in strings(p):
                        priv[f"ethertype{hex(et)}-strings"].add(s)
    with open(pubf, "w") as f:
        f.write(f"pcap files: {nfiles}\n")
        for k in sorted(pub):
            f.write(f"{k}: " + ", ".join(f"{a}={b}" for a, b in sorted(pub[k].items(), key=lambda x: str(x[0]))) + "\n")
    with open(privf, "wb") as f:
        for k in sorted(priv):
            f.write(f"## {k} ({len(priv[k])})\n".encode())
            for s in sorted(priv[k]):
                f.write(s + b"\n")
    print(f"pcap files: {nfiles}")


if __name__ == "__main__":
    main()
