#!/usr/bin/env python3
"""Independent parse of a KL AEMI descriptor image: index map and name table.

Usage: image_inventory.py <img.bin> <aaf>
Prints every index-map entry, derives (type, index, name_index) -> ordinal
from name_base (ENTITY carries 2 names, every other named type 1), and
compares with the population the tb/name_state oracle enumerates for <aaf>
(written out here independently from the README's inventory table).
"""
import struct, sys
img = open(sys.argv[1], "rb").read(); aaf = int(sys.argv[2])
magic, ver, ncfg, nent, nnames, ioff, noff, ibytes = struct.unpack(">IHHHHIII", img[:24])
assert magic == 0x41454D49 and ibytes == len(img), (hex(magic), ibytes, len(img))
assert sum(struct.unpack(">8I", img[:32])) & 0xFFFFFFFF == 0xFFFFFFFF
print(f"n_config {ncfg} entries {nent} n_names {nnames}")
tuples = {}
for e in range(nent):
    cfg, typ, cnt, elen, eoff, nbase, stride = struct.unpack(">HHHHIHH", img[ioff + 16*e: ioff + 16*e + 16])
    print(f"  type 0x{typ:04x} count {cnt:3d} len {elen:4d} name_base {nbase if nbase != 0xFFFF else '-'}")
    if nbase == 0xFFFF:
        continue
    npd = 2 if typ == 0 else 1
    for i in range(cnt):
        body = img[eoff + i*stride: eoff + i*stride + 4]
        btyp, bidx = struct.unpack(">HH", body)
        assert btyp == typ, (typ, btyp)
        for k in range(npd):
            tuples[(typ, bidx, k)] = nbase + i*npd + k
# the oracle population of tb/name_state/sim_main.cpp, restated
groups = [(0x0000,1),(0x0001,1),(0x0002,1),(0x0005,aaf+1),(0x0006,aaf+1),(0x0009,1),
          (0x000A,aaf+2),(0x0014,25 if aaf == 1 else 72),(0x001A,1),(0x0024,1)]
oracle = {}
for t, c in groups:
    for i in range(c):
        for k in range(2 if t == 0 else 1):
            oracle[(t, i, k)] = len(oracle)
ords = sorted(tuples.values())
print(f"image named tuples {len(tuples)}; ordinals dense 0..{len(tuples)-1}: {ords == list(range(len(tuples)))}; n_names match: {len(tuples) == nnames}")
print(f"oracle tuples {len(oracle)}; identical tuple->ordinal map: {oracle == tuples}")
for key in sorted(set(oracle) | set(tuples)):
    if oracle.get(key) != tuples.get(key):
        print("  DIFF", key, "oracle", oracle.get(key), "image", tuples.get(key))
sys.exit(0 if oracle == tuples and len(tuples) == nnames else 1)
