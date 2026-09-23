#!/usr/bin/env python3
"""Count tap-envelope and non-envelope records in every pcap under a root, and
report every tcpdump log's drop line.

Usage: pcap_envelope_census.py ARCHIVE_ROOT

Independent of the packet's own decoder. A record has a valid tap envelope
when it is at least 28 octets long, its first little-endian word is 6 and its
third word (tap port) is 2 or 3. Every other record is counted as
non-envelope, split into short (< 28 octets) and other. The pcap record walk
also proves each file parses to its last octet.
"""
import os, re, struct, sys


def census(path):
    raw = open(path, "rb").read()
    magic = struct.unpack("<I", raw[:4])[0]
    if magic not in (0xA1B2C3D4, 0xA1B23C4D):
        return None
    off, total, env, short, other = 24, 0, 0, 0, 0
    while off + 16 <= len(raw):
        _s, _f, incl, _o = struct.unpack("<IIII", raw[off:off + 16])
        off += 16
        pkt = raw[off:off + incl]
        off += incl
        total += 1
        if len(pkt) < 28:
            short += 1
            continue
        tag, _l, port = struct.unpack("<III", pkt[:12])
        if tag == 6 and port in (2, 3):
            env += 1
        else:
            other += 1
    return dict(total=total, env=env, nonenv=short + other, short=short,
                clean_end=(off == len(raw)))


def main():
    root = sys.argv[1]
    pcaps, logs = [], []
    for dp, dn, fn in os.walk(root):
        for f in fn:
            p = os.path.join(dp, f)
            if f.endswith(".pcap"):
                pcaps.append(p)
            elif f.startswith("tcpdump") and f.endswith(".log"):
                logs.append(p)
    for p in sorted(pcaps):
        c = census(p)
        print(f"PCAP {os.path.relpath(p, root)} {c}")
    for p in sorted(logs):
        t = open(p, encoding="utf-8", errors="replace").read()
        m = re.search(r"(\d+) packets? dropped by kernel", t)
        print(f"LOG {os.path.relpath(p, root)} dropped_by_kernel={m.group(1) if m else 'NO-LINE'}")
    print(f"TOTALS pcaps={len(pcaps)} tcpdump_logs={len(logs)}")


if __name__ == "__main__":
    main()
