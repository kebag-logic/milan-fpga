#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The QSPI flash map, read from ``milan_soc.py`` - never transcribed.

``FLASHBOOT_LAYOUT`` + ``FLASHBOOT_RESERVED`` in
[`sw/litex/milan_soc.py`](milan_soc.py) are the one source of truth for what
lives at which offset.  Every other consumer - the flash-map diagram, the
trace-segment budget, the persistence inventory, the roundtrip gates - reads
them THROUGH this module, by parsing the SoC source rather than importing it,
so nothing needs LiteX installed to know the map.

This reader lived in the retired partition emitter (`sw/dts/`) until #259
removed that toolkit with the rest of the host stack.  It is 40 lines and the
map it reads is still real, so it moved here, beside the file it parses,
instead of being copied into each consumer.

Usage:
    from flash_map import load_map, check_map, READ_ONLY
"""
import ast
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SOC = os.path.join(HERE, "milan_soc.py")

#: Slots nothing running on the board may write.  A stray write onto the
#: configuration slot bricks the board's self-config; `journal` and `user` are
#: deliberately writable - they are the whole point of reserving them.
READ_ONLY = {"bitstream", "kernel", "opensbi", "dtb", "rootfs"}


def _literal(name, src=SOC):
    tree = ast.parse(open(src, encoding="utf-8").read())
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id == name:
                    return ast.literal_eval(node.value)
    raise SystemExit(f"flash_map: {name} not found in {src} - fix the reader, "
                     f"do not hand-copy the map")


def load_map():
    """[(name, offset, size, kind)] ordered by offset, plus (flash_size, eb)."""
    layout, reserved = _literal("FLASHBOOT_LAYOUT"), _literal("FLASHBOOT_RESERVED")
    rows = [(n, e["offset"], e["size"], "image") for n, e in layout.items()]
    rows += [(n, e["offset"], e["size"], "reserved") for n, e in reserved.items()]
    return (sorted(rows, key=lambda r: r[1]),
            _literal("FLASH_SIZE"), _literal("FLASH_ERASE_BLOCK"))


def check_map(rows, flash_size, erase):
    """Overlap / alignment / past-the-device, as a list of problem strings."""
    problems, prev_end, prev_name = [], 0, None
    for name, off, size, _kind in rows:
        if size <= 0:
            problems.append(f"{name}: non-positive size {size}")
        if off % erase:
            problems.append(f"{name}: offset 0x{off:X} not erase-block aligned")
        if size % erase:
            problems.append(f"{name}: size 0x{size:X} not an erase-block multiple")
        if off < prev_end:
            problems.append(f"{name} @0x{off:X} overlaps {prev_name} "
                            f"(ends 0x{prev_end:X})")
        if off + size > flash_size:
            problems.append(f"{name}: ends 0x{off + size:X} past the device "
                            f"(0x{flash_size:X})")
        prev_end, prev_name = off + size, name
    return problems


if __name__ == "__main__":
    rows, flash_size, erase = load_map()
    problems = check_map(rows, flash_size, erase)
    for name, off, size, kind in rows:
        print(f"  0x{off:07X}  {size // 1024:>6} KiB  {name:<10} {kind}")
    print(f"{len(rows)} slot(s) of 0x{flash_size:X}, erase block 0x{erase:X}, "
          f"{len(problems)} problem(s)")
    for p in problems:
        print(f"  PROBLEM {p}")
    raise SystemExit(1 if problems else 0)
