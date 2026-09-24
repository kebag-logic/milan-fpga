#!/usr/bin/env python3
"""The bench switch's DHCP cadence on the DUT link (Run A, B, C tap captures).

Usage: verify_switch_dhcp.py <a200-packet-dir>
Groups the switch-side DHCP frames by whether their source OUI is the
switch's clock-identity OUI (3c:c0:c6), by the option-12 length and whether
it is masked. Other sources are printed only as "other" (no address).
"""
import collections
import glob
import os
import struct
import sys


def recs(path):
    raw = open(path, "rb").read()
    off, out = 24, []
    while off + 16 <= len(raw):
        _, _, incl, _ = struct.unpack("<IIII", raw[off:off + 16])
        off += 16
        pkt = raw[off:off + incl]
        off += incl
        if len(pkt) >= 42 and struct.unpack("<I", pkt[:4])[0] == 6 and struct.unpack("<I", pkt[8:12])[0] in (2, 3):
            out.append((struct.unpack("<I", pkt[16:20])[0], struct.unpack("<I", pkt[8:12])[0], pkt[28:]))
    # unwrap the tap ns counter
    res, prev, base = [], None, 0
    for lo, p, fr in out:
        if prev is not None and lo < prev:
            base += 1 << 32
        prev = lo
        res.append(((base + lo) / 1e9, p, fr))
    return res


def opt12(u):
    i = 240
    while i < len(u):
        c = u[i]
        if c == 0:
            i += 1
            continue
        if c == 255:
            break
        ln = u[i + 1]
        if c == 12:
            return u[i + 2:i + 2 + ln]
        i += 2 + ln
    return b""


for path in sorted(glob.glob(os.path.join(sys.argv[1], "bench/run*/tap-run*.pcap"))):
    by = collections.defaultdict(list)
    for t, p, fr in recs(path):
        if p == 2 and struct.unpack(">H", fr[12:14])[0] == 0x0800 and fr[23] == 17 and struct.unpack(">H", fr[36:38])[0] == 67:
            h = opt12(fr[42:])
            src = "switch OUI" if fr[6:9] == bytes.fromhex("3cc0c6") else "other"
            by[(src, len(h), b"#" in h)].append(t)
    for (src, hl, masked), ts in by.items():
        iv = sorted(set(round(b - a, 2) for a, b in zip(ts, ts[1:])))
        print(f"{os.path.basename(path)}: source {src}; option-12 length {hl}, masked {masked}: {len(ts)} frames, intervals {iv[:4]}{'...' if len(iv) > 4 else ''}")
