#!/usr/bin/env python3
"""List distinct printable strings hidden in captures and hex/base64 payloads.

Usage: printable_strings_census.py <archive-root> > strings.txt

1. Every frame of every classic pcap under the root (tap envelope removed):
   distinct printable ASCII runs of >= 4 octets per EtherType, excluding
   runs made only of the mask octet `#`.
2. Every text file: every run of >= 16 hex digits (even length) and every
   base64-looking run of >= 24 characters is decoded; printable runs of
   >= 4 octets inside the decoded bytes are listed.
3. UTF-16LE printable runs of >= 4 characters anywhere in any file.
Output lines: source-class, count, string. Review by eye; the script
decides nothing.
"""
import base64
import binascii
import collections
import re
import struct
import sys
from pathlib import Path

PRINT = re.compile(rb"[\x20-\x7e]{4,}")
U16 = re.compile(rb"(?:[\x20-\x7e]\x00){4,}")
HEXRUN = re.compile(rb"(?<![0-9A-Fa-f])(?:[0-9A-Fa-f]{2}){8,}(?![0-9A-Fa-f])")
B64RUN = re.compile(rb"(?<![A-Za-z0-9+/=])[A-Za-z0-9+/]{24,}={0,2}")
out = collections.Counter()


def keep(s):
    return s.strip(b"#").strip() != b"" and set(s) - set(b"# .-_")


def frames(path):
    data = path.read_bytes()
    endian = "<" if data[:4] == b"\xd4\xc3\xb2\xa1" else ">"
    off = 24
    while off + 16 <= len(data):
        _s, _u, incl, _o = struct.unpack(endian + "IIII", data[off:off + 16])
        off += 16
        fr = data[off:off + incl]
        off += incl
        if incl >= 42 and fr[:4] == b"\x06\x00\x00\x00":
            w5, w6 = struct.unpack("<II", fr[20:28])
            if w5 == w6 == incl - 28:
                fr = fr[28:]
        yield fr


def main():
    root = Path(sys.argv[1])
    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        data = p.read_bytes()
        if p.suffix == ".pcap":
            for fr in frames(p):
                et = fr[12:14].hex() if len(fr) >= 14 else "short"
                if et == "8100" and len(fr) >= 18:
                    et = fr[16:18].hex()
                for m in PRINT.findall(fr[14:]):
                    if keep(m):
                        out[(f"pcap.et{et}", m[:120])] += 1
            continue
        for m in U16.findall(data):
            s = m.decode("utf-16-le").encode()
            if keep(s):
                out[("utf16le", s[:120])] += 1
        for m in HEXRUN.findall(data):
            try:
                raw = binascii.unhexlify(m)
            except binascii.Error:
                continue
            for s in PRINT.findall(raw):
                if keep(s):
                    out[("hexdecoded", s[:120])] += 1
        for m in B64RUN.findall(data):
            if HEXRUN.fullmatch(m):
                continue
            try:
                raw = base64.b64decode(m + b"=" * (-len(m) % 4))
            except (binascii.Error, ValueError):
                continue
            for s in PRINT.findall(raw):
                if keep(s) and len(s) >= 5:
                    out[("b64decoded", s[:120])] += 1
    for (cls, s), n in sorted(out.items()):
        print(f"{cls}\t{n}\t{s!r}")


if __name__ == "__main__":
    main()
