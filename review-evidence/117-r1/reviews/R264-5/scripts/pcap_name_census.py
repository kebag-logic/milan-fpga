#!/usr/bin/env python3
"""Census of every name-bearing field in the pinned captures (pure Python).

Usage:
  pcap_name_census.py <root> [--allow allowlist.txt] [--private out.txt]

Walks every *.pcap under <root> and decodes Ethernet (with 802.1Q), IPv4/IPv6,
UDP, and collects the name-bearing fields:
  DHCPv4 options 12 (host name), 15 (domain), 60 (vendor class), 77 (user
  class), 81 (client FQDN); DHCPv6 option 39 (FQDN); DNS/mDNS/LLMNR question and
  record owner names, PTR/CNAME/SRV targets and TXT strings; NBNS names; SSDP
  headers; LLDP chassis/port/system TLVs; IEEE 1722.1 AECP/ADP printable runs;
  plus every other printable ASCII run of 6+ octets in any frame.

A value counts as MASKED when it contains '#', and as PUBLIC when it matches
the allowlist (regexes, one per line; reviewed by hand). Every other value is
UNREVIEWED and printed only as SHA-256 prefix and length, so the public
receipt cannot leak what the census is looking for; --private writes the raw
unreviewed values to a file that is never published.
"""
import hashlib
import os
import re
import struct
import sys
from collections import defaultdict


def read_pcap(path):
    data = open(path, "rb").read()
    magic = data[:4]
    if magic in (b"\xd4\xc3\xb2\xa1", b"\x4d\x3c\xb2\xa1"):
        e = "<"
    elif magic in (b"\xa1\xb2\xc3\xd4", b"\xa1\xb2\x3c\x4d"):
        e = ">"
    else:
        raise ValueError(f"{path}: not a classic pcap")
    linktype = struct.unpack(e + "I", data[20:24])[0]
    off = 24
    while off + 16 <= len(data):
        _, _, incl, _ = struct.unpack(e + "IIII", data[off:off + 16])
        off += 16
        yield linktype, data[off:off + incl]
        off += incl


def dns_name(buf, off, depth=0):
    labels, jumped, end = [], False, None
    while off < len(buf) and depth < 20:
        ln = buf[off]
        if ln == 0:
            off += 1
            break
        if ln & 0xC0 == 0xC0:
            if off + 1 >= len(buf):
                break
            ptr = ((ln & 0x3F) << 8) | buf[off + 1]
            if not jumped:
                end = off + 2
            jumped = True
            off = ptr
            depth += 1
            continue
        labels.append(buf[off + 1:off + 1 + ln])
        off += 1 + ln
    return b".".join(labels), (end if jumped else off)


def parse_dns(p, out):
    if len(p) < 12:
        return
    qd, an, ns, ar = struct.unpack(">HHHH", p[4:12])
    off = 12
    try:
        for _ in range(qd):
            n, off = dns_name(p, off)
            out["dns-qname"].add(n)
            off += 4
        for _ in range(an + ns + ar):
            n, off = dns_name(p, off)
            out["dns-owner"].add(n)
            typ, _, _, rdl = struct.unpack(">HHIH", p[off:off + 10])
            off += 10
            rd = p[off:off + rdl]
            if typ in (12, 5, 2):
                out["dns-target"].add(dns_name(p, off)[0])
            elif typ == 33:
                out["dns-target"].add(dns_name(p, off + 6)[0])
            elif typ == 16:
                i = 0
                while i < len(rd):
                    ln = rd[i]
                    out["dns-txt"].add(rd[i + 1:i + 1 + ln])
                    i += 1 + ln
            elif typ == 13:
                out["dns-hinfo"].add(rd)
            off += rdl
    except (struct.error, IndexError):
        out["parse-errors"].add(b"dns")


def parse_dhcp(p, out):
    if len(p) < 240 or p[236:240] != b"\x63\x82\x53\x63":
        return
    out["dhcp-sname"].add(p[44:108].rstrip(b"\0"))
    out["dhcp-file"].add(p[108:236].rstrip(b"\0"))
    i = 240
    while i < len(p):
        code = p[i]
        if code == 0:
            i += 1
            continue
        if code == 255 or i + 1 >= len(p):
            break
        ln = p[i + 1]
        v = p[i + 2:i + 2 + ln]
        if code in (12, 15, 60, 77, 81):
            out[f"dhcp-opt{code}"].add(v[3:] if code == 81 else v)
        i += 2 + ln


def nbns_name(enc):
    try:
        s = bytes(((enc[i] - 0x41) << 4) | (enc[i + 1] - 0x41) for i in range(0, 32, 2))
        return s.rstrip(b" \0")
    except (ValueError, IndexError):
        return b"?"


def census(root):
    out = defaultdict(set)
    counts = defaultdict(int)
    files = sorted(os.path.join(d, f) for d, _, fs in os.walk(root) for f in fs if f.endswith(".pcap"))
    for path in files:
        for lt, fr in read_pcap(path):
            counts["frames"] += 1
            # tap records carry a 28-octet envelope (tag 6, port 2 or 3) in
            # front of the Ethernet frame; the capture host's own records do not
            if len(fr) >= 42 and fr[:4] == b"\x06\0\0\0" and fr[8:12] in (b"\x02\0\0\0", b"\x03\0\0\0"):
                counts["tap-enveloped"] += 1
                fr = fr[28:]
            if lt != 1 or len(fr) < 14:
                continue
            et = struct.unpack(">H", fr[12:14])[0]
            off = 14
            while et in (0x8100, 0x88A8) and off + 4 <= len(fr):
                et = struct.unpack(">H", fr[off + 2:off + 4])[0]
                off += 4
            pl = fr[off:]
            for run in re.findall(rb"[\x20-\x7e]{6,}", fr):
                out["any-ascii6"].add(run)
            if et == 0x88CC:
                i = 0
                while i + 2 <= len(pl):
                    h = struct.unpack(">H", pl[i:i + 2])[0]
                    t, ln = h >> 9, h & 0x1FF
                    if t == 0:
                        break
                    out[f"lldp-tlv{t}"].add(pl[i + 2:i + 2 + ln])
                    i += 2 + ln
            elif et == 0x22F0 and pl:
                for run in re.findall(rb"[\x20-\x7e]{5,}", pl):
                    out[f"avtp-subtype-{pl[0]:02x}"].add(run)
                for run in re.findall(rb"#{3,}", pl):
                    counts[f"hash-run3-avtp-{pl[0]:02x}"] += 1
            elif et in (0x0800, 0x86DD):
                if et == 0x0800 and len(pl) >= 20:
                    ihl = (pl[0] & 0xF) * 4
                    proto, l4 = pl[9], pl[ihl:]
                elif et == 0x86DD and len(pl) >= 40:
                    proto, l4 = pl[6], pl[40:]
                else:
                    continue
                if proto != 17 or len(l4) < 8:
                    if proto == 6:
                        counts["tcp"] += 1
                    continue
                sp, dp = struct.unpack(">HH", l4[:4])
                u = l4[8:]
                ports = {sp, dp}
                counts[f"udp-{min(ports)}"] += 1
                if ports & {67, 68}:
                    parse_dhcp(u, out)
                elif ports & {53, 5353, 5355}:
                    parse_dns(u, out)
                elif ports & {137}:
                    if len(u) > 13 + 32:
                        out["nbns-name"].add(nbns_name(u[13:45]))
                elif ports & {1900}:
                    for line in u.split(b"\r\n"):
                        if b":" in line:
                            out["ssdp-hdr"].add(line)
                elif ports & {546, 547}:
                    i = 4
                    while i + 4 <= len(u):
                        code, ln = struct.unpack(">HH", u[i:i + 4])
                        if code == 39:
                            out["dhcpv6-fqdn"].add(u[i + 5:i + 4 + ln])
                        i += 4 + ln
    return files, out, counts


def main():
    root = sys.argv[1]
    allow, private = [], None
    if "--allow" in sys.argv:
        allow = [re.compile(l.rstrip("\n").encode()) for l in open(sys.argv[sys.argv.index("--allow") + 1]) if l.strip() and not l.startswith("#")]
    if "--private" in sys.argv:
        private = open(sys.argv[sys.argv.index("--private") + 1], "wb")
    files, out, counts = census(root)
    print(f"captures: {len(files)}; frames: {counts['frames']}")
    print("udp/tcp frame counts:", {k: v for k, v in sorted(counts.items()) if k != "frames"})
    unreviewed_total = 0
    for field in sorted(out):
        vals = out[field]
        masked = [v for v in vals if b"#" in v]
        public = [v for v in vals if b"#" not in v and any(a.fullmatch(v) for a in allow)]
        rest = [v for v in vals if b"#" not in v and not any(a.fullmatch(v) for a in allow)]
        print(f"{field}: {len(vals)} distinct; masked {len(masked)}; allowlisted {len(public)}; unreviewed {len(rest)}")
        if field != "any-ascii6":
            for v in sorted(public):
                shown = "<ipv6 link-local reverse-lookup name>" if v.endswith(b".ip6.arpa") else v.decode("latin-1")
                print(f"   public: {shown!r}")
        for v in sorted(rest):
            unreviewed_total += 1
            print(f"   UNREVIEWED sha256={hashlib.sha256(v).hexdigest()[:16]} len={len(v)}")
            if private:
                private.write(field.encode() + b"\t" + v + b"\n")
    print(f"UNREVIEWED total: {unreviewed_total}")
    return 0 if unreviewed_total == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
