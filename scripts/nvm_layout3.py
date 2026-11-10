#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""nvm_layout3.py - read the split placement's record space, layout 3 (#823).

The space is declared once, in sw/firmware/ctrl_nvm/nvm_layout3.h, which the
split placement's saved-state store's codec compiles. This module is how
every Python reader takes it from there instead of restating it: the
builder's split output
(sw/builder/endstation_builder.py, emit_nvm_split), the reference codec
(scripts/nvm_klj3.py) and the format page's figures
(scripts/nvm_format_32x32.py).

The rules it reads by, each a refusal rather than an assumption:
  * every NVM3_CAP_<block> is ONE live `#define` with a decimal value;
  * every NVM3_ID_<block> after the first is the base before it plus that
    block's capacity, in the order of BLOCKS, so the bases this module derives
    are the ones the C preprocessor derives;
  * NVM3_LAYOUT and NVM3_REC_HDR are one decimal `#define` each.

usage:
    python3 scripts/nvm_layout3.py        # print the blocks
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HEADER = ROOT / "sw/firmware/ctrl_nvm/nvm_layout3.h"

#: (the group's name in scripts/nvm_contract.py, the header's block suffix),
#: in the declaration's order.
BLOCKS = (("CFG_IDX", "CFG"), ("SUID", "SUID"), ("RATE", "RATE"),
          ("CLKSRC", "CLKS"), ("MCR", "MCR"), ("BINDING", "BIND"),
          ("FMT_IN", "FMTI"), ("FMT_OUT", "FMTO"), ("PT_OFS", "PTOF"),
          ("MAPS_IN", "MAPI"), ("MAPS_OUT", "MAPO"), ("NAME", "NAME"))

_DEFINE = re.compile(r"\s*#\s*define\s+(NVM3_\w+)\s+(.*?)\s*$")
_DECIMAL = re.compile(r"(\d+)u?")
_CHAIN = re.compile(r"\(\s*NVM3_ID_(\w+)\s*\+\s*NVM3_CAP_(\w+)\s*\)")


class LayoutError(Exception):
    """The header does not say what a reader needs."""


@dataclass(frozen=True)
class Block:
    """One block of the space."""

    group: str      # the group, as scripts/nvm_contract.py names it
    base: int       # its first id
    cap: int        # how many ids it holds
    where: str      # the NVM3_CAP_* declaration, as path:line

    @property
    def last(self) -> int:
        """Its last id."""
        return self.base + self.cap - 1


@dataclass(frozen=True)
class Layout3:
    """The declared space: every block, the layout version and the header."""

    blocks: tuple[Block, ...]
    layout: int
    rec_hdr: int
    header: str     # the declaration's path, as shown

    @property
    def id_space(self) -> int:
        """One past the last id."""
        return self.blocks[-1].base + self.blocks[-1].cap

    def block(self, group: str) -> Block:
        """The block of `group`."""
        for b in self.blocks:
            if b.group == group:
                return b
        raise KeyError(group)


def _live_defines(text: str) -> dict[str, list[tuple[int, str]]]:
    """name -> [(line, value)] for every live NVM3_* define (comments cut)."""
    code = re.sub(r"/\*.*?\*/", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)
    found: dict[str, list[tuple[int, str]]] = {}
    for n, line in enumerate(code.splitlines(), 1):
        m = _DEFINE.fullmatch(line.split("//", 1)[0])
        if m:
            found.setdefault(m.group(1), []).append((n, m.group(2)))
    return found


def _one_decimal(defs: dict, name: str, shown: str) -> tuple[int, int]:
    """(value, line) of the one live decimal define `name`."""
    hits = defs.get(name, [])
    if len(hits) != 1:
        raise LayoutError(f"{shown}: {len(hits)} live `#define {name} <decimal>` lines, need exactly 1; "
                          "the layout 3 record space cannot be read, refusing rather than assuming one (#823)")
    line, value = hits[0]
    m = _DECIMAL.fullmatch(value)
    if m is None:
        raise LayoutError(f"{shown}:{line}: {name} is `{value}`, not a decimal")
    return int(m.group(1)), line


def read(path: Path = HEADER) -> Layout3:
    """The layout 3 space as `path` declares it."""
    shown = str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)
    defs = _live_defines(path.read_text(encoding="utf-8"))
    blocks, base, before = [], 0, None
    for group, tag in BLOCKS:
        cap, line = _one_decimal(defs, f"NVM3_CAP_{tag}", shown)
        if before is None:
            first, _ = _one_decimal(defs, f"NVM3_ID_{tag}", shown)
            if first != 0:
                raise LayoutError(f"{shown}: NVM3_ID_{tag} is {first}; the first block starts at id 0")
        else:
            hits = defs.get(f"NVM3_ID_{tag}", [])
            m = _CHAIN.fullmatch(hits[0][1]) if len(hits) == 1 else None
            if m is None or m.group(1) != before or m.group(2) != before:
                raise LayoutError(f"{shown}: NVM3_ID_{tag} is not (NVM3_ID_{before} + NVM3_CAP_{before}); "
                                  "the blocks must follow one another in the declared order")
        blocks.append(Block(group, base, cap, f"{shown}:{line}"))
        base += cap
        before = tag
    layout, _ = _one_decimal(defs, "NVM3_LAYOUT", shown)
    rec_hdr, _ = _one_decimal(defs, "NVM3_REC_HDR", shown)
    return Layout3(tuple(blocks), layout, rec_hdr, shown)


def main() -> int:
    """Print the blocks."""
    try:
        lay = read()
    except LayoutError as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 2
    for b in lay.blocks:
        print(f"{b.group:<9} {b.base:>5} .. {b.last:>5}  ({b.cap} ids, {b.where})")
    print(f"id space {lay.id_space}, layout {lay.layout}, record header {lay.rec_hdr} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
