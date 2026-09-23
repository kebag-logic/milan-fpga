#!/usr/bin/env python3
"""Check the page's B1/B3 statements about the bench switch against every
published capture: ADP (no AVDECC entity), ARP probe/announcement of a
link-local address, IGMP sources, DNS-SD control service and TXT record per
A202 cycle, DHCP cadence and whether anything answers, and TCP use.

usage: check_b1_b3.py <archive root review-evidence/117-r1>
Prints counts and address CLASSES only (no host names, no TXT contents).
"""
import collections
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pcap_census import dns_name, ipv4_class, records, split_envelope  # noqa: E402

SW_MAC = bytes.fromhex("3cc0c6fe0210")


def frames(path):
    d = open(path, "rb").read()
    off = 24
    while off + 16 <= len(d):
        s, us, incl, _ = struct.unpack("<IIII", d[off:off + 16])
        off += 16
        pkt = d[off:off + incl]
        off += incl
        where, fr = split_envelope(pkt)
        yield s + us * 1e-6, where, fr


def l3(fr):
    et = struct.unpack(">H", fr[12:14])[0]
    off = 14
    if et == 0x8100:
        et = struct.unpack(">H", fr[16:18])[0]
        off = 18
    return et, fr[off:]


def main():
    root = sys.argv[1]
    per = {}
    for dp, _, fns in os.walk(root):
        for fn in sorted(fns):
            if not fn.endswith(".pcap"):
                continue
            rel = os.path.relpath(os.path.join(dp, fn), root)
            c = collections.Counter()
            dhcp_t = []
            igmp_src = collections.Counter()
            arp = []
            for t, where, fr in frames(os.path.join(dp, fn)):
                if len(fr) < 14:
                    continue
                src = fr[6:12]
                et, p = l3(fr)
                if et == 0x22F0 and p and (p[0] & 0x7F) == 0x7A and len(p) >= 12:
                    c["adp from switch MAC" if src == SW_MAC else "adp other"] += 1
                if src != SW_MAC:
                    if et == 0x0800 and len(p) >= 28 and p[9] == 17:
                        ihl = (p[0] & 15) * 4
                        sp, dpt = struct.unpack(">HH", p[ihl:ihl + 4])
                        if sp == 67:
                            c["DHCP server reply (any source)"] += 1
                        if 67 in (sp, dpt) and sp == 68:
                            c["DHCP request from another host"] += 1
                    continue
                c["frames from switch MAC"] += 1
                if et == 0x0806 and len(p) >= 28:
                    spa, tpa = p[14:18], p[24:28]
                    if spa == b"\0\0\0\0":
                        arp.append(("probe", ipv4_class(tpa)))
                    elif spa == tpa:
                        arp.append(("announce", ipv4_class(tpa)))
                    else:
                        arp.append(("other", ipv4_class(spa)))
                elif et == 0x0800 and len(p) >= 20:
                    ihl = (p[0] & 15) * 4
                    proto = p[9]
                    if proto == 2:
                        igmp_src[ipv4_class(p[12:16])] += 1
                        c["igmp from switch"] += 1
                    elif proto == 6:
                        c["tcp from switch"] += 1
                    elif proto == 17:
                        sp, dpt = struct.unpack(">HH", p[ihl:ihl + 4])
                        body = p[ihl + 8:]
                        if dpt == 67:
                            dhcp_t.append(t)
                            c["dhcp from switch"] += 1
                        elif 5353 in (sp, dpt):
                            c["mdns from switch"] += 1
                            qd, an, ns, ar = struct.unpack(">HHHH", body[4:12])
                            off = 12
                            for _ in range(qd):
                                _n, off = dns_name(body, off)
                                off += 4
                            for _ in range(an + ns + ar):
                                name, off = dns_name(body, off)
                                typ, _cl, _ttl, rdl = struct.unpack(">HHIH", body[off:off + 10])
                                off += 10 + rdl
                                if typ == 33 and name.endswith(b"._tcp.local"):
                                    c["dns-sd SRV for a _tcp service"] += 1
                                if typ == 16:
                                    c["dns-sd TXT record"] += 1
                elif et == 0x86DD and len(p) >= 48:
                    if p[6] == 17 and 5353 in struct.unpack(">HH", p[40:44]):
                        c["mdns6 from switch"] += 1
            c.update(collections.Counter(f"arp {k}:{v}" for k, v in arp))
            c.update(collections.Counter(f"igmp source class {k}" for k in igmp_src.elements()))
            if len(dhcp_t) > 1:
                iv = [b - a for a, b in zip(dhcp_t, dhcp_t[1:])]
                c[f"dhcp interval s min/max {min(iv):.2f}/{max(iv):.2f}"] = len(iv)
            per[rel] = c
    for rel in sorted(per):
        c = per[rel]
        keys = [k for k in c if c[k]]
        print(rel)
        for k in sorted(keys):
            print(f"    {k}: {c[k]}")
    # igmp source distinct addresses per class, across all captures
    srcs = collections.defaultdict(set)
    for dp, _, fns in os.walk(root):
        for fn in fns:
            if fn.endswith(".pcap"):
                for t, where, fr in frames(os.path.join(dp, fn)):
                    if len(fr) >= 14 and fr[6:12] == SW_MAC:
                        et, p = l3(fr)
                        if et == 0x0800 and len(p) >= 20 and p[9] == 2:
                            srcs[ipv4_class(p[12:16])].add(p[12:16])
    print("distinct IGMP source addresses from the switch, by class:", {k: len(v) for k, v in srcs.items()})


if __name__ == "__main__":
    main()
