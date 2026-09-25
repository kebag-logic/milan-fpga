#!/usr/bin/env python3
"""Compare two non-interlaced 8-bit PNGs pixel by pixel (stdlib only).

Usage: png_diff.py a.png b.png
RGBA inputs are compared on RGB after compositing onto white. Prints size,
count of differing pixels, max channel delta and the bounding box of
differences; exits 0 when every pixel differs by at most 8 per channel.
"""
import struct
import sys
import zlib


def decode(path):
    data = open(path, "rb").read()
    assert data[:8] == b"\x89PNG\r\n\x1a\n", path
    pos, idat, w = 8, b"", None
    while pos < len(data):
        ln, typ = struct.unpack(">I4s", data[pos:pos + 8])
        chunk = data[pos + 8:pos + 8 + ln]
        if typ == b"IHDR":
            w, h, depth, ctype, _, _, inter = struct.unpack(">IIBBBBB", chunk)
            assert depth == 8 and inter == 0 and ctype in (2, 6), (path, depth, ctype, inter)
            bpp = 3 if ctype == 2 else 4
        elif typ == b"IDAT":
            idat += chunk
        pos += 12 + ln
    raw = zlib.decompress(idat)
    stride = w * bpp
    out, prev = [], bytearray(stride)
    for y in range(h):
        f = raw[y * (stride + 1)]
        line = bytearray(raw[y * (stride + 1) + 1:(y + 1) * (stride + 1)])
        for i in range(stride):
            a = line[i - bpp] if i >= bpp else 0
            b = prev[i]
            c = prev[i - bpp] if i >= bpp else 0
            if f == 1:
                line[i] = (line[i] + a) & 255
            elif f == 2:
                line[i] = (line[i] + b) & 255
            elif f == 3:
                line[i] = (line[i] + (a + b) // 2) & 255
            elif f == 4:
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                line[i] = (line[i] + (a if pa <= pb and pa <= pc else b if pb <= pc else c)) & 255
        prev = line
        row = []
        for x in range(w):
            px = line[x * bpp:(x + 1) * bpp]
            if bpp == 4:
                al = px[3]
                px = [(px[k] * al + 255 * (255 - al)) // 255 for k in range(3)]
            row.append(tuple(px[:3]))
        out.append(row)
    return w, h, out


def main():
    wa, ha, a = decode(sys.argv[1])
    wb, hb, b = decode(sys.argv[2])
    print(f"a {wa}x{ha}  b {wb}x{hb}")
    if (wa, ha) != (wb, hb):
        print("SIZE MISMATCH")
        return 1
    n, mx, box = 0, 0, [wa, ha, -1, -1]
    for y in range(ha):
        for x in range(wa):
            d = max(abs(p - q) for p, q in zip(a[y][x], b[y][x]))
            if d:
                n += 1
                mx = max(mx, d)
                box = [min(box[0], x), min(box[1], y), max(box[2], x), max(box[3], y)]
    print(f"differing pixels {n} of {wa * ha}, max channel delta {mx}, bbox {box if n else None}")
    return 0 if mx <= 8 else 1


if __name__ == "__main__":
    sys.exit(main())
