#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""
pack_aem_bin.py - aem_rom.json -> aem_rom.bin for the aecpd software responder
(the measured AECP lane, docs/design/AREA_BUDGET.md).

The daemon serves READ_DESCRIPTOR straight out of this image, exactly as the
fabric ROM served it - same bytes, same directory, ONE model source (the
builder's aem_overlay.json -> gen_aem_store.py -> aem_rom.json -> here). The
overlay rows name the live-field patch points (ENTITY_ID at +4 of the ENTITY
descriptor, MAC, AVAIL_IDX...) that the daemon fills from CSR/argv at startup
- the same fields the fabric's dyn-overlay map patched in hardware.

Format (little-endian; private contract between this packer and aecpd.c):
  0x00  magic   "KLAEM1\\0\\0" (8)
  0x08  u32     rom_len
  0x0C  u32     dir_count
  0x10  u32     ovl_count
  0x14  dir     dir_count x { u16 type, u16 index, u32 base, u32 len }
  ...   ovl     ovl_count x { u32 addr, u16 nbytes, char source[12] (NUL-pad) }
  ...   rom     rom_len bytes

Usage:
  python3 avdecc/pack_aem_bin.py [--json avdecc/aem_rom.json] [--out aem_rom.bin]
"""
import argparse
import json
import os
import struct
import sys

MAGIC = b"KLAEM1\x00\x00"


def pack(j):
    rom = bytes.fromhex(j["rom_hex"])
    dirs = j["directory"]
    ovls = j.get("overlays", [])
    out = bytearray()
    out += MAGIC
    out += struct.pack("<III", len(rom), len(dirs), len(ovls))
    for d in dirs:
        if not (0 <= d["base"] and d["base"] + d["len"] <= len(rom)):
            raise SystemExit(f"pack_aem_bin: directory row {d} outside the ROM "
                             f"({len(rom)} bytes) - refusing a lying image")
        out += struct.pack("<HHII", d["type"], d["index"], d["base"], d["len"])
    for o in ovls:
        src = o["source"].encode()
        if len(src) > 12:
            raise SystemExit(f"pack_aem_bin: overlay source {o['source']!r} "
                             "does not fit the 12-byte field - widen the "
                             "format (and aecpd.c) rather than truncating")
        out += struct.pack("<IH12s", o["addr"], o["bytes"], src)
    out += rom
    return bytes(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    here = os.path.dirname(os.path.abspath(__file__))
    ap.add_argument("--json", default=os.path.join(here, "aem_rom.json"))
    ap.add_argument("--out", default=os.path.join(here, "aem_rom.bin"))
    args = ap.parse_args()
    with open(args.json) as f:
        blob = pack(json.load(f))
    with open(args.out, "wb") as f:
        f.write(blob)
    print(f"pack_aem_bin: {args.out} ({len(blob)} bytes)")


if __name__ == "__main__":
    sys.exit(main())
