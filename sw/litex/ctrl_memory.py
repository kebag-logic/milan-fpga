#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""ctrl_memory.py - the split placement's control-firmware memory (#640 M8a).

In the split placement (`milan_soc.py --ctrl-mailbox`) the control firmware
owns the CPU's reset entry and runs from block RAM; the BIOS ROM and SRAM are
not built. This file is the one statement of that memory map. The SoC reads it
(`add_ctrl_memory`), the firmware link reads it (`regions.ld` for
`sw/firmware/ctrl/plat/ctrl_split.ld`) and so does the fit evidence:

- two regions at the CPU's own origins: `rom` at the reset address holds the
  load image (.text, .rodata and the initial values of .data), and `sram`
  holds .data, .bss and the stack. Each region spans the whole budget, so the
  CPU netlist, which is generated from the region list, does not depend on the
  image;
- the populated part of each region is sized from the linked image, in
  power-of-two banks of whole RAMB18 granules (2,048 bytes: 512 32-bit
  words), largest first. Each bank maps to whole block RAMs with no rounding,
  so a region wastes less than one granule;
- the allocation is held to the owner's 224 KB: 56 RAMB36 at 4,096 usable
  bytes each, a RAMB18 counting half (#640 ruling 6101485877). LEDGERED
  names the one point allowed past it, only when its measurement asks for it
  by name (#665); the SoC build asks for none.

Every refusal names its check: `reset entry`, `memory map`, `memory-map
overlap`, `allocation over budget` and `staging buffer`. RULES lists each
rule a check enforces, as docs/design/SPLIT_CONTROL_MEMORY.md section 3 does,
and a refusal names its rule too; test_ctrl_memory.py requires every rule to
have an arm that fails when the rule is removed.

    python3 sw/litex/ctrl_memory.py regions <directory>
    python3 sw/litex/ctrl_memory.py plan <elf> [--stage-bytes N] [--ledgered-point NAME]
"""

from __future__ import annotations

import argparse
import json
import struct
import sys
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[2] / "scripts"

#: One RAMB36: 1,024 32-bit words. Its parity bits are not byte-addressable.
TILE_BYTES = 4096
#: One RAMB18: 512 32-bit words, the smallest bank.
GRANULE_BYTES = 2048
#: The owner's 224 KB as RAMB36 at 4,096 usable bytes (#640 ruling 6101485877).
BUDGET_TILES = 56
BUDGET_BYTES = BUDGET_TILES * TILE_BYTES
#: The F1 store's staging buffer (sw/firmware/ctrl_nvm/nvm_store.c).
STAGE_SYMBOL = "nvm_stage"

_PT_LOAD = 1
_SHT_SYMTAB = 2
_SHT_NOBITS = 8
_SHF_WRITE = 0x1
_SHF_ALLOC = 0x2
_EM_RISCV = 243


@dataclass(frozen=True)
class Rule:
    """One documented refusal: the check that names it and what it refuses."""

    check: str
    refuses: str


#: Every refusal rule, keyed by rule, in the order of SPLIT_CONTROL_MEMORY.md
#: section 3, whose table test_ctrl_memory.py requires to equal this one.
RULES: dict[str, Rule] = {
    "entry address": Rule("reset entry", "An image entering anywhere but `rom`'s first byte"),
    "entry bytes": Rule("reset entry", "An image with no initial bytes at the reset address"),
    "cpu origins": Rule("reset entry", "A CPU whose reset address or `sram` origin is not this map's"),
    "elf class": Rule("memory map", "A file that is not a little-endian ELF32 file"),
    "elf machine": Rule("memory map", "An ELF32 file for a machine other than RISC-V"),
    "elf truncated": Rule("memory map", "A header, table, name or load segment running past the end of the file"),
    "outside regions": Rule("memory map", "A section outside both regions"),
    "loads outside rom": Rule("memory map", "Initial bytes loading outside `rom`, the only region the bitstream "
                                            "initialises"),
    "load coverage": Rule("memory map", "A section with initial bytes that the load segments' file bytes, which "
                                        "program `rom`, do not all carry"),
    "nobits in rom": Rule("memory map", "A NOBITS section in `rom`, which the firmware cannot write"),
    "writable in rom": Rule("memory map", "A writable section with initial bytes running in `rom`, which drops "
                                          "its writes"),
    "regions": Rule("memory-map overlap", "The two regions sharing an address"),
    "addresses": Rule("memory-map overlap", "Two sections sharing an address"),
    "initial bytes": Rule("memory-map overlap", "Two sections sharing a load address"),
    "budget": Rule("allocation over budget", "Banks totalling more than 56 RAMB36, a RAMB18 counting half, or "
                                             "more than a ledgered point's tiles; that point's override on any "
                                             "other image"),
    "stage symbol": Rule("staging buffer", "An image with no `nvm_stage`"),
    "stage size": Rule("staging buffer", "An `nvm_stage` that is not the selected shape's stage: its KLJ2 "
                                         "container plus one record header"),
}


class Refusal(ValueError):
    """An image or a map the split placement cannot hold, named by its check and rule."""

    def __init__(self, rule: str, detail: str) -> None:
        """Keep the check's and the rule's names apart from the detail, for callers that test them."""
        self.rule = rule
        self.check = RULES[rule].check
        super().__init__(f"{self.check}: {detail}")


@dataclass(frozen=True)
class Region:
    """One window of the CPU's address map, in bytes."""

    name: str
    origin: int
    size: int

    @property
    def end(self) -> int:
        """The first address past the region."""
        return self.origin + self.size

    def holds(self, start: int, end: int) -> bool:
        """Whether [start, end) lies inside the region."""
        return self.origin <= start and end <= self.end


#: The VexiiRiscv origins LiteX gives `rom` (the reset address) and `sram`.
ROM = Region("rom", 0x0000_0000, BUDGET_BYTES)
RAM = Region("sram", 0x1000_0000, BUDGET_BYTES)


@dataclass(frozen=True)
class Section:
    """One allocated section of a linked image."""

    name: str
    vma: int
    lma: int
    size: int
    loaded: bool       # it has initial bytes in the file (not NOBITS)
    writable: bool     # SHF_WRITE: the firmware writes it


@dataclass(frozen=True)
class Image:
    """What the split placement reads from a linked ELF."""

    entry: int
    sections: tuple[Section, ...]
    symbols: Mapping[str, tuple[int, int]]     # name -> (value, size)
    segments: tuple[tuple[int, bytes], ...]    # (physical address, initial bytes)


@dataclass(frozen=True)
class Plan:
    """The banks each region is built from, in bytes, largest first."""

    rom_bytes: int
    ram_bytes: int
    rom_banks: tuple[int, ...]
    ram_banks: tuple[int, ...]
    budget: float = BUDGET_TILES        # what the plan was held to
    ledgered: str | None = None         # the LEDGERED point it was planned as, if any

    @property
    def tiles(self) -> float:
        """The allocation in RAMB36 equivalents, a RAMB18 counting half."""
        return (sum(self.rom_banks) + sum(self.ram_banks)) / TILE_BYTES

    def summary(self) -> dict[str, object]:
        """The plan as the fit evidence and the build log print it."""
        def region(need: int, banks: tuple[int, ...]) -> dict[str, object]:
            """One region's need, banks and the block RAMs they map to."""
            return {"bytes": need, "banks": list(banks),
                    "RAMB36": sum(b // TILE_BYTES for b in banks),
                    "RAMB18": sum(b == GRANULE_BYTES for b in banks)}
        held = {} if self.ledgered is None else {"ledgered": self.ledgered, "ledgered_tiles": self.budget}
        return {"rom": region(self.rom_bytes, self.rom_banks),
                "sram": region(self.ram_bytes, self.ram_banks),
                "tiles": self.tiles, "budget_tiles": BUDGET_TILES, **held}


@dataclass(frozen=True)
class Ledgered:
    """A point the owner let plan past the budget, until the lane it is owed to recovers it."""

    point: str                              # the point, as the ledger names it
    symbols: tuple[tuple[str, int], ...]    # (symbol, size): what makes an image that point
    tiles: float                            # what it may plan
    owed: str                               # the lane that recovers the tiles, and the ruling


#: The only points `plan` may let past BUDGET_TILES, each only when its own
#: measurement names it (`plan --ledgered-point`, ctrl_srp_image.py); the SoC
#: build names none, so no build is held to more than 56 RAMB36. An image is the
#: point when it carries every listed symbol at its listed size: the 8x8 shape's
#: staging buffer and the size fixture's per-interface table at two interfaces
#: (ctrl_aecp_image.c, `uint64_t image_allocation[MBX_N_IF]`). The tile and a
#: half over budget are ledgered in docs/design/SPLIT_CONTROL_MEMORY.md section 5.
LEDGERED: dict[str, Ledgered] = {
    "8x8-two-interfaces": Ledgered("8x8, two interfaces", ((STAGE_SYMBOL, 13_264), ("image_allocation", 16)),
                                   57.5, "lane S14, the hybrid XIP (#665 decision D3, rulings 6412739248 and "
                                         "6425357821)"),
}


def ledgered_tiles(image: Image, name: str) -> float:
    """The tiles LEDGERED[name] may plan, refused for any image that is not its point."""
    point = LEDGERED.get(name)
    if point is None:
        raise Refusal("budget", f"no ledgered point is named {name!r}; the ledger holds {sorted(LEDGERED)}")
    carried = {symbol: image.symbols.get(symbol, (0, None))[1] for symbol, _ in point.symbols}
    if carried != dict(point.symbols):
        raise Refusal("budget", f"the override {name!r} is for the {point.point} image alone, the one "
                      f"carrying {dict(point.symbols)}; this image carries {carried}")
    return point.tiles


def banks(need: int) -> tuple[int, ...]:
    """`need` bytes as power-of-two banks of whole granules, largest first."""
    granules = -(-need // GRANULE_BYTES)
    return tuple(GRANULE_BYTES << bit for bit in reversed(range(granules.bit_length()))
                 if granules >> bit & 1)


def _unpack(path: Path, data: bytes, layout: str, offset: int, what: str) -> tuple[int, ...]:
    """`struct.unpack_from`, refused by name when the field runs past the end of the file."""
    if offset + struct.calcsize(layout) > len(data):
        raise Refusal("elf truncated", f"{path}: the {what} at byte {offset} runs past the end "
                      f"of the {len(data)}-byte file")
    return struct.unpack_from(layout, data, offset)


def _string(path: Path, data: bytes, offset: int) -> str:
    """The NUL-terminated string at `offset`."""
    end = data.find(b"\0", offset)
    if end < 0:
        raise Refusal("elf truncated", f"{path}: the name at byte {offset} runs past the end "
                      f"of the {len(data)}-byte file")
    return data[offset:end].decode()


def read_elf(path: Path) -> Image:
    """The entry, allocated sections, symbols and load bytes of a little-endian RV32 ELF."""
    data = path.read_bytes()
    if data[:6] != b"\x7fELF\x01\x01":
        raise Refusal("elf class", f"{path} is not a little-endian ELF32 file")
    (_, machine, _, entry, phoff, shoff, _, _, phentsize, phnum, shentsize, shnum,
     shstrndx) = _unpack(path, data, "<HHIIIIIHHHHHH", 16, "ELF header")
    if machine != _EM_RISCV:
        raise Refusal("elf machine", f"{path} is not a RISC-V image")
    headers = [_unpack(path, data, "<10I", shoff + i * shentsize, f"section header {i}")
               for i in range(shnum)]
    programs = [_unpack(path, data, "<8I", phoff + i * phentsize, f"program header {i}")
                for i in range(phnum)]
    loads = [p for p in programs if p[0] == _PT_LOAD]
    for _, offset, _, _, filesz, _, _, _ in loads:
        if offset + filesz > len(data):
            raise Refusal("elf truncated", f"{path}: the {filesz} initial bytes at byte {offset} "
                          f"run past the end of the {len(data)}-byte file")
    names = headers[shstrndx][4]

    def lma(vma: int) -> int:
        """The load address of `vma`, through the segment that holds it."""
        for _, _, vaddr, paddr, _, memsz, _, _ in loads:
            if vaddr <= vma < vaddr + memsz:
                return paddr + vma - vaddr
        return vma

    sections, symbols = [], {}
    for name, kind, flags, addr, offset, size, link, _, _, entsize in headers:
        if flags & _SHF_ALLOC and size:
            sections.append(Section(_string(path, data, names + name), addr, lma(addr), size,
                                    kind != _SHT_NOBITS, bool(flags & _SHF_WRITE)))
        if kind == _SHT_SYMTAB:
            strings = headers[link][4]
            for at in range(offset, offset + size, entsize):
                st_name, value, st_size = _unpack(path, data, "<III", at, "symbol")
                if st_name:
                    symbols[_string(path, data, strings + st_name)] = (value, st_size)
    segments = tuple((p[3], data[p[1]:p[1] + p[4]]) for p in loads if p[4])
    return Image(entry, tuple(sections), symbols, segments)


def _carried(segments: tuple[tuple[int, bytes], ...], start: int, end: int) -> bool:
    """Whether the load segments' file bytes, which `rom_words` programs, cover [start, end)."""
    at = start
    for addr, data in sorted(segments, key=lambda segment: segment[0]):
        if addr <= at < addr + len(data):
            at = addr + len(data)
    return at >= end


def _overlap(rule: str, spans: list[tuple[int, int, str]]) -> None:
    """Refuse the first two of `spans` ([start, end) and name) that share an address."""
    spans = sorted(spans)
    for (start, end, name), (other, _, second) in zip(spans, spans[1:]):
        if other < end:
            raise Refusal(rule, f"{second} at 0x{other:08x} lies inside {name} "
                          f"[0x{start:08x}, 0x{end:08x}) ({rule})")


def check_map(image: Image, rom: Region = ROM, ram: Region = RAM) -> None:
    """The reset entry, every section inside its region, and no two sharing an address."""
    _overlap("regions", [(r.origin, r.end, r.name) for r in (rom, ram)])
    if image.entry != rom.origin:
        raise Refusal("entry address", f"the image enters at 0x{image.entry:08x}, not at the "
                      f"CPU's reset address 0x{rom.origin:08x}, the start of {rom.name}")
    if not any(s.loaded and s.vma <= image.entry < s.vma + s.size for s in image.sections):
        raise Refusal("entry bytes", f"no initial bytes at the reset address 0x{image.entry:08x}")
    if not _carried(image.segments, image.entry, image.entry + 4):
        raise Refusal("entry bytes", f"no load segment carries the first word at the reset address "
                      f"0x{image.entry:08x}, so {rom.name} would hold none there")
    for s in image.sections:
        home = next((r for r in (rom, ram) if r.holds(s.vma, s.vma + s.size)), None)
        if home is None:
            raise Refusal("outside regions", f"{s.name} [0x{s.vma:08x}, 0x{s.vma + s.size:08x}) "
                          f"is outside {rom.name} and {ram.name}")
        if s.loaded and not rom.holds(s.lma, s.lma + s.size):
            raise Refusal("loads outside rom", f"{s.name}'s initial bytes load at 0x{s.lma:08x}, "
                          f"outside {rom.name}, the only region the bitstream initialises")
        if s.loaded and not _carried(image.segments, s.lma, s.lma + s.size):
            raise Refusal("load coverage", f"{s.name}'s {s.size} initial bytes at 0x{s.lma:08x} are not all "
                          f"in the load segments' file bytes, the only bytes that program {rom.name}")
        if not s.loaded and home is rom:
            raise Refusal("nobits in rom", f"{s.name} reserves {rom.name}, which the firmware cannot write")
        if s.writable and home is rom:
            raise Refusal("writable in rom", f"{s.name} is writable and runs at 0x{s.vma:08x} in "
                          f"{rom.name}, which drops writes; it runs in {ram.name}, loaded from {rom.name}")
    _overlap("addresses", [(s.vma, s.vma + s.size, s.name) for s in image.sections])
    _overlap("initial bytes", [(s.lma, s.lma + s.size, s.name) for s in image.sections if s.loaded])


def plan(image: Image, rom: Region = ROM, ram: Region = RAM,
         budget: float = BUDGET_TILES, ledgered: str | None = None) -> Plan:
    """The banks the image needs, refused when its map is wrong or it exceeds the budget.

    `ledgered` names a LEDGERED point; its tiles replace the budget, and any
    image that is not that point is refused.
    """
    check_map(image, rom, ram)
    if ledgered is not None:
        budget = ledgered_tiles(image, ledgered)
    rom_end = max((s.lma + s.size for s in image.sections if s.loaded), default=rom.origin)
    ram_end = max((s.vma + s.size for s in image.sections if ram.holds(s.vma, s.vma + s.size)),
                  default=ram.origin)
    need = Plan(rom_end - rom.origin, ram_end - ram.origin,
                banks(rom_end - rom.origin), banks(ram_end - ram.origin), budget, ledgered)
    if need.tiles > budget:
        held = "" if ledgered is None else f" ledgered for {LEDGERED[ledgered].point}"
        raise Refusal("budget",
                      f"{need.tiles:g} RAMB36 ({rom.name} {need.rom_bytes} bytes in "
                      f"{sum(need.rom_banks)}, {ram.name} {need.ram_bytes} bytes in "
                      f"{sum(need.ram_banks)}) exceeds the {budget:g}-RAMB36 budget{held}")
    return need


def rom_words(image: Image, rom: Region = ROM) -> list[int]:
    """The initial contents of `rom` as little-endian 32-bit words."""
    end = max((addr + len(data) for addr, data in image.segments), default=rom.origin)
    contents = bytearray(end - rom.origin + -(end - rom.origin) % 4)
    for addr, data in image.segments:
        contents[addr - rom.origin:addr - rom.origin + len(data)] = data
    return list(struct.unpack(f"<{len(contents) // 4}I", contents))


def stage_bytes(shape: object, donor: object) -> int:
    """The F1 store's stage for `shape`: its container plus one record header.

    The container is `scripts/nvm_klj2.py`'s own, over the shape's record
    inventory, so this reads the derivation the store's host tests grade
    against `nvm_shape.h` (NVM_STAGE_BYTES) rather than restating it.
    """
    if str(SCRIPTS) not in sys.path:
        sys.path.insert(0, str(SCRIPTS))
    from nvm_contract import REC_HDR, Ident
    from nvm_klj2 import erased_record, klj2_assemble
    from nvm_shape import inventory
    frames = {rid: erased_record(plen)
              for _, _, rid, plen, _ in inventory(shape, donor.base) if rid is not None}
    container, _ = klj2_assemble(frames, donor, Ident(seq=0, entity_id=0, model_id=0))
    return len(container) + REC_HDR


def check_stage(image: Image, stage: int, shape: str) -> None:
    """Refuse an image whose staging buffer was built for another shape."""
    if STAGE_SYMBOL not in image.symbols:
        raise Refusal("stage symbol", f"the image has no {STAGE_SYMBOL}")
    size = image.symbols[STAGE_SYMBOL][1]
    if size != stage:
        raise Refusal("stage size", f"{STAGE_SYMBOL} is {size} bytes; the {shape} "
                      f"shape stages {stage}")


def regions_ld(rom: Region = ROM, ram: Region = RAM) -> str:
    """The MEMORY block `ctrl_split.ld` includes as regions.ld."""
    return ("MEMORY\n{\n"
            f"\t{rom.name} (rx) : ORIGIN = 0x{rom.origin:08x}, LENGTH = 0x{rom.size:08x}\n"
            f"\t{ram.name} (rwx) : ORIGIN = 0x{ram.origin:08x}, LENGTH = 0x{ram.size:08x}\n"
            "}\n")


def main(argv: list[str] | None = None) -> int:
    """Write regions.ld, or check one linked image and print its plan."""
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    sub = ap.add_subparsers(dest="command", required=True)
    regions = sub.add_parser("regions", help="write regions.ld into a directory")
    regions.add_argument("directory", type=Path)
    planned = sub.add_parser("plan", help="check a linked image and print its banks")
    planned.add_argument("elf", type=Path)
    planned.add_argument("--stage-bytes", type=int, help="the selected shape's staging buffer")
    planned.add_argument("--ledgered-point", choices=sorted(LEDGERED),
                         help="plan the one ledgered point to its ledgered tiles; any other image is refused")
    args = ap.parse_args(argv)
    if args.command == "regions":
        (args.directory / "regions.ld").write_text(regions_ld())
        return 0
    try:
        image = read_elf(args.elf)
        if args.stage_bytes is not None:
            check_stage(image, args.stage_bytes, "requested")
        print(json.dumps(plan(image, ledgered=args.ledgered_point).summary(), indent=2))
    except Refusal as exc:
        print(f"REFUSED {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
