#!/usr/bin/env python3
"""List every name-carrying protocol field in classic pcap files.

Usage: pcap_identity_fields.py <file.pcap>... > fields.txt

Pure standard library. Walks Ethernet (with 802.1Q), IPv4/IPv6, UDP and
reports, per distinct value: DHCP options 12/15/60/61/81/119, DNS/mDNS/LLMNR
names (questions and records, including TXT, SRV targets, PTR, HINFO),
NetBIOS name service names (first-level decoded), SSDP/HTTP header lines,
LLDP TLVs, IPv4 and IPv6 addresses, EtherTypes and UDP ports seen. Prints
the value and a count; masked bytes (0x23 '#') are shown as-is.
"""
import collections
import struct
import sys

seen = collections.Counter()


def add(kind, value):
    seen[(kind, value)] += 1


def dns_name(buf, off, depth=0):
    labels = []
    jumped = False
    end = off
    while off < len(buf) and depth < 20:
        n = buf[off]
        if n == 0:
            off += 1
            break
        if n & 0xC0 == 0xC0:
            if off + 1 >= len(buf):
                break
            ptr = ((n & 0x3F) << 8) | buf[off + 1]
            if not jumped:
                end = off + 2
            jumped = True
            off = ptr
            depth += 1
            continue
        labels.append(buf[off + 1:off + 1 + n])
        off += 1 + n
    if not jumped:
        end = off
    return b".".join(labels), end


def parse_dns(kind, buf):
    if len(buf) < 12:
        return
    qd, an, ns, ar = struct.unpack("!HHHH", buf[4:12])
    off = 12
    try:
        for _ in range(qd):
            name, off = dns_name(buf, off)
            add(kind + ".qname", name)
            off += 4
        for _ in range(an + ns + ar):
            name, off = dns_name(buf, off)
            add(kind + ".rrname", name)
            rtype, _c, _t, rdlen = struct.unpack("!HHIH", buf[off:off + 10])
            off += 10
            rdata = buf[off:off + rdlen]
            if rtype in (12, 5, 2):  # PTR CNAME NS
                add(kind + f".rdata{rtype}", dns_name(buf, off)[0])
            elif rtype == 33:  # SRV
                add(kind + ".srv", dns_name(buf, off + 6)[0])
            elif rtype == 16:  # TXT
                i = 0
                while i < len(rdata):
                    n = rdata[i]
                    add(kind + ".txt", rdata[i + 1:i + 1 + n])
                    i += 1 + n
            elif rtype == 13:  # HINFO
                add(kind + ".hinfo", rdata)
            elif rtype == 1:
                add(kind + ".A", ".".join(map(str, rdata)).encode())
            elif rtype == 47:
                add(kind + ".nsec", dns_name(buf, off)[0])
            off += rdlen
    except (struct.error, IndexError):
        add(kind + ".parse_error", b"")


def nbns_decode(label):
    if len(label) != 32:
        return label
    try:
        return bytes(
            ((label[i] - 0x41) << 4) | (label[i + 1] - 0x41) for i in range(0, 32, 2)
        )
    except ValueError:
        return label


def parse_udp(src, dst, sport, dport, pl):
    add("udp.ports", f"{min(sport, dport)}".encode())
    if 67 in (sport, dport) or 68 in (sport, dport):
        if len(pl) > 240 and pl[236:240] == b"\x63\x82\x53\x63":
            i = 240
            while i < len(pl):
                code = pl[i]
                if code == 0:
                    i += 1
                    continue
                if code == 255 or i + 1 >= len(pl):
                    break
                n = pl[i + 1]
                val = pl[i + 2:i + 2 + n]
                if code in (12, 15, 60, 61, 81, 119, 43, 77, 124, 125):
                    add(f"dhcp.opt{code}", val)
                i += 2 + n
    if 5353 in (sport, dport):
        parse_dns("mdns", pl)
    elif 5355 in (sport, dport):
        parse_dns("llmnr", pl)
    elif 53 in (sport, dport):
        parse_dns("dns", pl)
    elif 137 in (sport, dport):
        if len(pl) > 13:
            n = pl[12]
            add("nbns.name", nbns_decode(pl[13:13 + n]))
    elif 138 in (sport, dport):
        add("nbdgm.raw", pl[:80])
    elif 1900 in (sport, dport) or 3702 in (sport, dport):
        for line in pl.split(b"\r\n"):
            if line:
                add("ssdp.line", line[:160])
    elif 546 in (sport, dport) or 547 in (sport, dport):
        i = 4
        while i + 4 <= len(pl):
            code, n = struct.unpack("!HH", pl[i:i + 4])
            if code in (1, 16, 39, 17):
                add(f"dhcp6.opt{code}", pl[i + 4:i + 4 + n])
            i += 4 + n
    elif 17754 in (sport, dport) or 17755 in (sport, dport):
        pass
    else:
        add(f"udp.other.{min(sport, dport)}", b"")


def parse_frame(fr):
    if len(fr) < 14:
        return
    et = struct.unpack("!H", fr[12:14])[0]
    off = 14
    while et in (0x8100, 0x88A8) and len(fr) >= off + 4:
        et = struct.unpack("!H", fr[off + 2:off + 4])[0]
        off += 4
    add("ethertype", f"{et:04x}".encode())
    if et == 0x88CC:
        i = off
        while i + 2 <= len(fr):
            hdr = struct.unpack("!H", fr[i:i + 2])[0]
            t, n = hdr >> 9, hdr & 0x1FF
            if t == 0:
                break
            add(f"lldp.tlv{t}", fr[i + 2:i + 2 + n])
            i += 2 + n
    elif et == 0x0800:
        ip = fr[off:]
        if len(ip) < 20:
            return
        ihl = (ip[0] & 0x0F) * 4
        proto = ip[9]
        src = ".".join(map(str, ip[12:16]))
        dst = ".".join(map(str, ip[16:20]))
        add("ipv4.addr", src.encode())
        add("ipv4.addr", dst.encode())
        if proto == 17 and len(ip) >= ihl + 8:
            sport, dport = struct.unpack("!HH", ip[ihl:ihl + 4])
            parse_udp(src, dst, sport, dport, ip[ihl + 8:])
        elif proto == 6:
            add("ipv4.tcp", b"")
        elif proto == 2:
            add("ipv4.igmp", dst.encode())
    elif et == 0x86DD:
        ip = fr[off:]
        if len(ip) < 40:
            return
        add("ipv6.addr", ip[8:24].hex().encode())
        add("ipv6.addr", ip[24:40].hex().encode())
        if ip[6] == 17:
            sport, dport = struct.unpack("!HH", ip[40:44])
            parse_udp("", "", sport, dport, ip[48:])
    elif et == 0x0806:
        add("arp.spa", ".".join(map(str, fr[off + 14:off + 18])).encode())


def walk(path):
    data = open(path, "rb").read()
    magic = data[:4]
    endian = "<" if magic == b"\xd4\xc3\xb2\xa1" else ">"
    off = 24
    while off + 16 <= len(data):
        _s, _u, incl, _orig = struct.unpack(endian + "IIII", data[off:off + 16])
        off += 16
        fr = data[off:off + incl]
        # Tap records carry a 28-octet envelope ahead of the Ethernet frame
        # (word 0 = 6, words 5 and 6 = frame length); the capture host's own
        # records carry none.
        if incl >= 42 and fr[:4] == b"\x06\x00\x00\x00":
            w5, w6 = struct.unpack("<II", fr[20:28])
            if w5 == w6 == incl - 28:
                add("tap.envelope", b"")
                fr = fr[28:]
        parse_frame(fr)
        off += incl


def main():
    for p in sys.argv[1:]:
        walk(p)
    for (kind, value), n in sorted(seen.items()):
        print(f"{kind}\t{n}\t{value!r}")


if __name__ == "__main__":
    main()
