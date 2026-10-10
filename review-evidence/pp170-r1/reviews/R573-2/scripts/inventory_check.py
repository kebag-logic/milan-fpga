#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer's independent check of the name_state oracle against AEMI images.

Parses the image header, the per-(configuration, type) index map and each
descriptor body's own (type, index) key, derives every (type, index,
name_index) -> ordinal from name_base, and compares it with the oracle
enumeration that tb/name_state/sim_main.cpp encodes (re-stated here from its
group table). Also reports whether the factory names are pairwise distinct and
whether the bench's patterned saved values are pairwise distinct.

usage: inventory_check.py IMAGE AAF
"""
import struct
import sys

img = open(sys.argv[1], "rb").read()
aaf = int(sys.argv[2])
magic, ver, ncfg, nent, nnames, ioff, noff, size = struct.unpack(">IHHHHIII", img[:24])
assert magic == 0x41454D49 and ver == 1 and size == len(img), "bad header"
found = {}
for e in range(nent):
    cfg, dtype, count, elen, eoff, nbase, stride = struct.unpack(
        ">HHHHIHH", img[ioff + 16 * e: ioff + 16 * e + 16])
    if nbase == 0xFFFF:
        continue
    per = 2 if dtype == 0 else 1
    for i in range(count):
        body = img[eoff + i * stride: eoff + i * stride + 4]
        btype, bindex = struct.unpack(">HH", body)
        assert btype == dtype, (dtype, btype)
        for ni in range(per):
            found[(btype, bindex, ni)] = nbase + i * per + ni
names = [img[noff + 64 * k: noff + 64 * (k + 1)] for k in range(nnames)]

groups = [(0x0000, 1), (0x0001, 1), (0x0002, 1), (0x0005, aaf + 1), (0x0006, aaf + 1),
          (0x0009, 1), (0x000A, aaf + 2), (0x0014, 25 if aaf == 1 else 72),
          (0x001A, 1), (0x0024, 1)]
oracle = {}
for t, c in groups:
    for i in range(c):
        for ni in range(2 if t == 0 else 1):
            oracle[(t, i, ni)] = len(oracle)

def value(o):
    v = bytes(33 + (o * 11 + b * 7) % 90 for b in range(64))
    return bytes(64) if o % 7 == 2 else v

vals = [value(o) for o in range(len(oracle))]
dup_full = sorted({(a, b) for a in range(len(vals)) for b in range(a + 1, len(vals))
                   if vals[a] == vals[b] and any(vals[a])})
print(f"image {sys.argv[1]} bytes={len(img)} index_entries={nent} n_names={nnames}")
print(f"named tuples in image: {len(found)}; oracle tuples: {len(oracle)}")
print(f"ordinal map identical: {found == oracle}")
print(f"ordinals dense 0..n-1: {sorted(found.values()) == list(range(nnames))}")
print(f"factory names pairwise distinct (informational): {len(set(names)) == len(names)}")
print(f"bench saved values: {sum(1 for v in vals if not any(v))} empty; "
      f"non-empty duplicate ordinal pairs: {len(dup_full)} {dup_full[:4]}")
ok = found == oracle  # factory-name distinctness is informational only
sys.exit(0 if ok else 1)
