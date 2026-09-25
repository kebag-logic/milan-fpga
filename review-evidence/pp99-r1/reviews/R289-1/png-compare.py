#!/usr/bin/env python3
"""Compare two PNGs pixel by pixel (8-bit gray/RGB/RGBA, non-interlaced), with
alpha composited over white. Prints size, differing-pixel count and max channel
delta, plus a bounding box of the differences.
Usage: png-compare.py <a.png> <b.png>"""
import struct, sys, zlib

def decode(path):
    data = open(path, "rb").read()
    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    pos, idat, hdr = 8, b"", None
    while pos < len(data):
        n, typ = struct.unpack(">I4s", data[pos:pos + 8]); body = data[pos + 8:pos + 8 + n]; pos += 12 + n
        if typ == b"IHDR": hdr = struct.unpack(">IIBBBBB", body)
        elif typ == b"IDAT": idat += body
    w, h, depth, ctype, _, _, inter = hdr
    assert depth == 8 and inter == 0 and ctype in (0, 2, 6), hdr
    ch = {0: 1, 2: 3, 6: 4}[ctype]; raw = zlib.decompress(idat); stride = w * ch
    out, prev, i = [], bytearray(stride), 0
    for _ in range(h):
        f = raw[i]; line = bytearray(raw[i + 1:i + 1 + stride]); i += 1 + stride
        for x in range(stride):
            a = line[x - ch] if x >= ch else 0; b = prev[x]; c = prev[x - ch] if x >= ch else 0
            if f == 1: line[x] = (line[x] + a) & 255
            elif f == 2: line[x] = (line[x] + b) & 255
            elif f == 3: line[x] = (line[x] + (a + b) // 2) & 255
            elif f == 4:
                p = a + b - c; pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                line[x] = (line[x] + (a if pa <= pb and pa <= pc else b if pb <= pc else c)) & 255
        out.append(bytes(line)); prev = line
    def px(y, x):
        s = out[y][x * ch:(x + 1) * ch]
        if ch == 1: return (s[0],) * 3
        if ch == 3: return tuple(s)
        al = s[3]; return tuple((v * al + 255 * (255 - al) + 127) // 255 for v in s[:3])
    return w, h, px

wa, ha, pa = decode(sys.argv[1]); wb, hb, pb = decode(sys.argv[2])
print(f"a {wa}x{ha}  b {wb}x{hb}")
if (wa, ha) != (wb, hb): sys.exit("size differs")
diff, mx, box = 0, 0, [wa, ha, -1, -1]
for y in range(ha):
    for x in range(wa):
        d = max(abs(u - v) for u, v in zip(pa(y, x), pb(y, x)))
        if d > 8:
            diff += 1; box = [min(box[0], x), min(box[1], y), max(box[2], x), max(box[3], y)]
        mx = max(mx, d)
print(f"pixels differing by >8: {diff} of {wa * ha}; max channel delta {mx}; bbox {box if diff else '-'}")
