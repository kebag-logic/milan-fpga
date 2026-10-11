#!/usr/bin/env python3
"""R607-1: the exported rom bank .init files, concatenated, equal the ELF's load image.

    check_rom_init.py <gateware-dir> <elf>
Reads each <top>_rom_bank<N>.init (one hex word per line, LiteX's format) in
bank order and compares it word for word with the ELF's PT_LOAD bytes at their
physical addresses (zero-filled between segments), read independently here.
"""
import struct
import sys
from pathlib import Path

gw, elf = Path(sys.argv[1]), Path(sys.argv[2])
data = elf.read_bytes()
phoff, = struct.unpack_from("<I", data, 28)
phentsize, phnum = struct.unpack_from("<HH", data, 42)
img = bytearray()
for i in range(phnum):
    t, off, _v, pa, fsz, _m, _f, _a = struct.unpack_from("<8I", data, phoff + i * phentsize)
    if t == 1 and fsz:
        img.extend(bytes(max(0, pa + fsz - len(img))))
        img[pa:pa + fsz] = data[off:off + fsz]
img.extend(bytes(-len(img) % 4))
want = list(struct.unpack(f"<{len(img) // 4}I", img))
banks = sorted(gw.glob("*_rom_bank*.init"), key=lambda p: int(p.stem.rsplit("bank", 1)[1]))
got = []
for p in banks:
    words = [int(x, 16) for x in p.read_text().split()]
    print(f"{p.name}: {len(words)} words")
    got += words
tail = got[len(want):]
ok = got[:len(want)] == want and not any(tail)
print(f"image {len(want)} words, banks {len(got)} words, tail beyond image all zero: {not any(tail)}")
print("ROM INIT:", "MATCH" if ok else "MISMATCH")
sys.exit(0 if ok else 1)
