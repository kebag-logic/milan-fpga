#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The QSPI flash map, read from ``milan_soc.py`` - never transcribed.

``FLASHBOOT_LAYOUT`` + ``FLASHBOOT_RESERVED`` in
[`sw/litex/milan_soc.py`](milan_soc.py) are the one source of truth for what
lives at which offset.  The flash-map diagram, the trace-segment budget and
the roundtrip gates read them THROUGH this module, by parsing the SoC source
rather than importing it, so nothing needs LiteX installed to know the map.

The reader lives beside the SoC source it parses so every consumer derives the
same map without importing LiteX or maintaining a second copy.

Usage:
    from flash_map import load_map, check_map, literal, READ_ONLY
"""
import ast
import functools
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SOC = os.path.join(HERE, "milan_soc.py")


@functools.lru_cache(maxsize=None)
def _tree(src):
    """The SoC source parsed ONCE per process: four names, one parse."""
    with open(src, encoding="utf-8") as fh:
        return ast.parse(fh.read())


def literal(name, src=SOC):
    """One top-level literal out of the SoC source, by name."""
    for node in _tree(src).body:
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id == name:
                    return ast.literal_eval(node.value)
    raise SystemExit(f"flash_map: {name} not found in {src} - fix the reader, "
                     f"do not hand-copy the map")


_literal = literal          # the name the first consumers were written against

#: Slots nothing running on the board may write.  A stray write onto the
#: configuration slot bricks the board's self-config; the RESERVED slots
#: (`journal`, `user`) are deliberately writable - they are the whole point of
#: reserving them.  DERIVED from the image layout, never transcribed: a
#: mirrored copy of these names diverges the day a slot is added or renamed,
#: and nothing would notice.
READ_ONLY = frozenset(literal("FLASHBOOT_LAYOUT"))


def load_map():
    """[(name, offset, size, kind)] ordered by offset, plus (flash_size, eb)."""
    layout, reserved = literal("FLASHBOOT_LAYOUT"), literal("FLASHBOOT_RESERVED")
    rows = [(n, e["offset"], e["size"], "image") for n, e in layout.items()]
    rows += [(n, e["offset"], e["size"], "reserved") for n, e in reserved.items()]
    return (sorted(rows, key=lambda r: r[1]),
            literal("FLASH_SIZE"), literal("FLASH_ERASE_BLOCK"))


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
        # HIGH-WATER MARK, not the previous row: a slot swallowed whole by an
        # earlier, larger one starts after that row's start and would read as
        # clean if prev_end only tracked its immediate predecessor.
        if off + size > prev_end:
            prev_end, prev_name = off + size, name
        if off + size > flash_size:
            problems.append(f"{name}: ends 0x{off + size:X} past the device "
                            f"(0x{flash_size:X})")
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
