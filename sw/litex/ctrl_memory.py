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
  bytes each, a RAMB18 counting half (#640 ruling 6101485877).

Every refusal names its check: `reset entry`, `memory map`, `memory-map
overlap`, `allocation over budget` and `staging buffer`.

    python3 sw/litex/ctrl_memory.py regions <directory>
    python3 sw/litex/ctrl_memory.py plan <elf> [--stage-bytes N]
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
_SHF_ALLOC = 0x2
_EM_RISCV = 243


class Refusal(ValueError):
    """An image or a map the split placement cannot hold, named by its check."""

    def __init__(self, check: str, detail: str) -> None:
        """Keep the check's name apart from the detail, for callers that test it."""
        super().__init__(f"{check}: {detail}")
        self.check = check


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
        return {"rom": region(self.rom_bytes, self.rom_banks),
                "sram": region(self.ram_bytes, self.ram_banks),
                "tiles": self.tiles, "budget_tiles": BUDGET_TILES}


def banks(need: int) -> tuple[int, ...]:
    """`need` bytes as power-of-two banks of whole granules, largest first."""
    granules = -(-need // GRANULE_BYTES)
    return tuple(GRANULE_BYTES << bit for bit in reversed(range(granules.bit_length()))
                 if granules >> bit & 1)


def _string(data: bytes, offset: int) -> str:
    """The NUL-terminated string at `offset`."""
    return data[offset:data.index(b"\0", offset)].decode()


def read_elf(path: Path) -> Image:
    """The entry, allocated sections, symbols and load bytes of a little-endian RV32 ELF."""
    data = path.read_bytes()
    if data[:6] != b"\x7fELF\x01\x01":
        raise Refusal("memory map", f"{path} is not a little-endian ELF32 file")
    (_, machine, _, entry, phoff, shoff, _, _, phentsize, phnum, shentsize, shnum,
     shstrndx) = struct.unpack_from("<HHIIIIIHHHHHH", data, 16)
    if machine != _EM_RISCV:
        raise Refusal("memory map", f"{path} is not a RISC-V image")
    headers = [struct.unpack_from("<10I", data, shoff + i * shentsize) for i in range(shnum)]
    programs = [struct.unpack_from("<8I", data, phoff + i * phentsize) for i in range(phnum)]
    loads = [p for p in programs if p[0] == _PT_LOAD]
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
            sections.append(Section(_string(data, names + name), addr, lma(addr), size,
                                    kind != _SHT_NOBITS))
        if kind == _SHT_SYMTAB:
            strings = headers[link][4]
            for at in range(offset, offset + size, entsize):
                st_name, value, st_size = struct.unpack_from("<III", data, at)
                if st_name:
                    symbols[_string(data, strings + st_name)] = (value, st_size)
    segments = tuple((p[3], data[p[1]:p[1] + p[4]]) for p in loads if p[4])
    return Image(entry, tuple(sections), symbols, segments)


def _overlap(kind: str, spans: list[tuple[int, int, str]]) -> None:
    """Refuse the first two of `spans` ([start, end) and name) that share an address."""
    spans = sorted(spans)
    for (start, end, name), (other, _, second) in zip(spans, spans[1:]):
        if other < end:
            raise Refusal("memory-map overlap",
                          f"{second} at 0x{other:08x} lies inside {name} "
                          f"[0x{start:08x}, 0x{end:08x}) ({kind})")


def check_map(image: Image, rom: Region = ROM, ram: Region = RAM) -> None:
    """The reset entry, every section inside its region, and no two sharing an address."""
    _overlap("regions", [(r.origin, r.end, r.name) for r in (rom, ram)])
    if image.entry != rom.origin:
        raise Refusal("reset entry", f"the image enters at 0x{image.entry:08x}, not at the "
                      f"CPU's reset address 0x{rom.origin:08x}, the start of {rom.name}")
    if not any(s.loaded and s.vma <= image.entry < s.vma + s.size for s in image.sections):
        raise Refusal("reset entry", f"no initial bytes at the reset address 0x{image.entry:08x}")
    for s in image.sections:
        home = next((r for r in (rom, ram) if r.holds(s.vma, s.vma + s.size)), None)
        if home is None:
            raise Refusal("memory map", f"{s.name} [0x{s.vma:08x}, 0x{s.vma + s.size:08x}) "
                          f"is outside {rom.name} and {ram.name}")
        if s.loaded and not rom.holds(s.lma, s.lma + s.size):
            raise Refusal("memory map", f"{s.name}'s initial bytes load at 0x{s.lma:08x}, "
                          f"outside {rom.name}, the only region the bitstream initialises")
        if not s.loaded and home is rom:
            raise Refusal("memory map", f"{s.name} reserves {rom.name}, which the firmware cannot write")
    _overlap("addresses", [(s.vma, s.vma + s.size, s.name) for s in image.sections])
    _overlap("initial bytes", [(s.lma, s.lma + s.size, s.name) for s in image.sections if s.loaded])


def plan(image: Image, rom: Region = ROM, ram: Region = RAM,
         budget: int = BUDGET_TILES) -> Plan:
    """The banks the image needs, refused when its map is wrong or it exceeds the budget."""
    check_map(image, rom, ram)
    rom_end = max((s.lma + s.size for s in image.sections if s.loaded), default=rom.origin)
    ram_end = max((s.vma + s.size for s in image.sections if ram.holds(s.vma, s.vma + s.size)),
                  default=ram.origin)
    need = Plan(rom_end - rom.origin, ram_end - ram.origin,
                banks(rom_end - rom.origin), banks(ram_end - ram.origin))
    if need.tiles > budget:
        raise Refusal("allocation over budget",
                      f"{need.tiles:g} RAMB36 ({rom.name} {need.rom_bytes} bytes in "
                      f"{sum(need.rom_banks)}, {ram.name} {need.ram_bytes} bytes in "
                      f"{sum(need.ram_banks)}) exceeds the {budget}-RAMB36 budget")
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
        raise Refusal("staging buffer", f"the image has no {STAGE_SYMBOL}")
    size = image.symbols[STAGE_SYMBOL][1]
    if size != stage:
        raise Refusal("staging buffer", f"{STAGE_SYMBOL} is {size} bytes; the {shape} "
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
    args = ap.parse_args(argv)
    if args.command == "regions":
        (args.directory / "regions.ld").write_text(regions_ld())
        return 0
    try:
        image = read_elf(args.elf)
        if args.stage_bytes is not None:
            check_stage(image, args.stage_bytes, "requested")
        print(json.dumps(plan(image).summary(), indent=2))
    except Refusal as exc:
        print(f"REFUSED {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
