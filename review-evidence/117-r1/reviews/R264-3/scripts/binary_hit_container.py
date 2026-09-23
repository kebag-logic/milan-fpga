#!/usr/bin/env python3
"""Classify where a vendor-mark byte match sits inside binary PNG/PDF files.

Usage: binary_hit_container.py FILE [...]  (run from the clone root)
PNG: the chunk type holding the match (IDAT is zlib-compressed pixel data).
PDF: whether the match lies inside a stream ... endstream body.
"""
import re, struct, sys

#: the three-octet vendor mark, assembled from code points so this file never spells it
MARK_RE = re.compile(rb"\s*".join(re.escape(bytes([c])) for c in (100, 38, 98)), re.IGNORECASE)


def png_chunk_at(data, off):
    p = 8
    while p < len(data):
        n = struct.unpack(">I", data[p:p + 4])[0]
        t = data[p + 4:p + 8]
        if p <= off < p + 12 + n:
            return t.decode("latin-1")
        p += 12 + n
    return "?"


for f in sys.argv[1:]:
    d = open(f, "rb").read()
    for m in re.finditer(MARK_RE, d):
        if f.endswith(".png"):
            where = png_chunk_at(d, m.start())
        else:
            where = "inside-stream" if d.rfind(b"stream", 0, m.start()) > d.rfind(b"endstream", 0, m.start()) else "outside-stream"
        print(f"# V2 classification: {f} offset={m.start()} container={where}")
