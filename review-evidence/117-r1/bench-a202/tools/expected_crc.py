#!/usr/bin/env python3
"""Reference CRC32/SHA-256 values for the on-board identity readback (issue 117, A200).

For each seed build directory given, print the length, CRC32 and SHA-256 of:
  rom      software/bios/bios.bin without its trailing 4-byte CRC (what the
           BIOS 'crc 0x00000000 <len>' reads back from the ROM region)
  bitpay   the Xilinx .bit payload after the parsed header (what QSPI offset 0 holds)
  aem      aem_desc.bin (what QSPI +4 MiB holds)

usage: expected_crc.py <build_dir> [<build_dir> ...]
"""
import hashlib
import struct
import sys
import zlib
from pathlib import Path


def bit_payload(raw: bytes) -> bytes:
    # Xilinx .bit: 2-byte length + 9-byte magic, 2-byte 0x0001, then keyed fields
    # 'a'..'d' (2-byte length each) and 'e' (4-byte length) followed by the payload.
    off = 2 + struct.unpack(">H", raw[:2])[0]
    off += 2  # the 0x0001 record
    while True:
        key = raw[off:off + 1]
        off += 1
        if key == b"e":
            n = struct.unpack(">I", raw[off:off + 4])[0]
            off += 4
            payload = raw[off:off + n]
            if len(payload) != n or off + n != len(raw):
                raise SystemExit("bit header parse mismatch")
            return payload
        if key not in (b"a", b"b", b"c", b"d"):
            raise SystemExit(f"unexpected bit key {key!r} at {off - 1}")
        n = struct.unpack(">H", raw[off:off + 2])[0]
        off += 2 + n


def line(tag: str, data: bytes) -> str:
    return (f"{tag:7s} len={len(data):8d} crc32={zlib.crc32(data) & 0xffffffff:08x} "
            f"sha256={hashlib.sha256(data).hexdigest()}")


def main() -> int:
    for d in map(Path, sys.argv[1:]):
        bios = (d / "software/bios/bios.bin").read_bytes()
        bit = (d / "gateware/alinx_ax7101.bit").read_bytes()
        aem_path = d / "aem_desc.bin"
        aem = aem_path.read_bytes() if aem_path.exists() else None
        pay = bit_payload(bit)
        print(f"== {d.name}")
        print(f"   header_bytes={len(bit) - len(pay)}")
        print("   " + line("rom", bios[:-4]))
        print("   " + line("bitpay", pay))
        print("   " + (line("aem", aem) if aem is not None else "aem     (no aem_desc.bin in this seed directory)"))
        print("   " + line("bitfile", bit))
    return 0


if __name__ == "__main__":
    sys.exit(main())
