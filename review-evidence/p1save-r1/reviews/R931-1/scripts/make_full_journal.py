#!/usr/bin/env python3
"""R931-1 probe: a journal whose two slots hold a minor 1 container and delta frames of nothing filling the room.
Usage: make_full_journal.py <checkout> <stem> <frames per slot> <out>. The containers are the recorded 2509db68 store's."""
import struct, sys, zlib
from pathlib import Path
root, stem, n, out = Path(sys.argv[1]), sys.argv[2], int(sys.argv[3]), Path(sys.argv[4])
PAGE, HALF = 256, 640 * 1024 // 2
j = bytearray()
def seal(b):
    b[-4:] = struct.pack('<I', zlib.crc32(bytes(b[:-4])))
for k, s in enumerate('ab'):
    blob = bytearray(bytes.fromhex((root / f'sw/firmware/ctrl_nvm/test/data/2509db68/{stem}-{s}.hex').read_text()))
    struct.pack_into('<I', blob, 4, 0x00030001)
    seq = 5 + k
    struct.pack_into('<I', blob, 8, seq); seal(blob)
    slot = blob + b'\xff' * (-len(blob) % PAGE)
    for _ in range(n):
        new = bytearray(blob); struct.pack_into('<I', new, 8, seq + 2); seal(new)
        f = struct.pack('<7I', 0x33444C4B, 0x00010000, seq + 2, seq, 40, 0, struct.unpack_from('<I', new, len(new) - 4)[0])
        f += struct.pack('<I', zlib.crc32(f))
        slot += f + b'\xff' * (PAGE - len(f)); seq += 2
    j += slot.ljust(HALF, b'\xff')
out.write_bytes(j)
