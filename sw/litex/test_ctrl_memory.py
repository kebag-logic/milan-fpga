#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The split placement's firmware memory (#640 M8a): plan, rules, banks, link and SoC build.

`ctrl_memory.py` is the map and its checks; `milan_soc.CtrlMemory` is the
block RAM the SoC builds from them. This file grades seven things:

  1. BANKS. For every need up to past the budget, the banks are powers of two
     of whole RAMB18 granules, largest first, and hold the need with less than
     one granule spare. The oracle is ceil(need / 2,048) and its binary digits.
  2. RULES. ELFs written here, by a writer independent of `read_elf`, are
     planned or refused. A good image is accepted and its rom contents are the
     bytes placed at their load addresses. Every rule in `ctrl_memory.RULES`
     has a planted defect that must be refused by that rule, among them a
     truncated ELF, writable data running in rom and a CPU with other origins.
     The budget boundary is pinned: 56.0 RAMB36 is accepted and 56.5 refused.
  3. BANKS IN SIMULATION. The real `milan_soc.CtrlMemory`, in migen, at the
     largest image's sram banks (64, 32, 8, 4 and 2 KiB). rom reads its image
     at the first and last word of every bank and drops a write; sram writes
     byte lanes and reads them back at every bank boundary. Addresses past the
     last bank, sampled to the top of the 256 KiB window the SoC decodes for a
     region and so past 224 KiB, answer err in either region and write no
     bank. An access presented on the cycle after an err acks with its data.
  4. THE LINK. With an RV32 compiler (sw/firmware/gtest/fw_rv32.py), a probe
     linked by `sw/firmware/ctrl/plat/ctrl_split.ld` behind
     `ctrl_split_start.S` enters at the reset address with the reset entry
     first, loads .data's initial value from rom and is planned. The same
     script with `.data`'s `AT > rom` removed, with `.data` linked in rom, or
     entering at `main` is refused by its rule. Without a compiler this arm is
     a declared skip.
  5. THE SOC BUILD. milan_soc.py's own main(), on the shipping 1x1 config's
     argv (sw/builder/endstation_builder.py), exporting without Vivado or
     software: an allocation over budget, a memory-map overlap and the 8x8
     stage are each refused by its rule before any Verilog is written;
     --ctrl-mailbox alone and --ctrl-firmware alone are each refused; and the
     split export holds the image's banks and no BIOS ROM or SRAM, its rom
     banks hold the image, and the Builder is told to build no BIOS and no
     shipping firmware. LiteX's firmware data packages are refused in every
     interpreter, as the elaborate job installs none, so the arm grades the
     same in either.
  6. THE REGISTER. docs/design/SPLIT_CONTROL_MEMORY.md section 3 lists exactly
     `ctrl_memory.RULES`, and every rule has a refusal arm and a mutant.
  7. MUTANTS. Each mutant rebuilds one function or class of ctrl_memory.py or
     milan_soc.py from its own source with one edit that removes or weakens a
     rule or a property, and must turn its arm red with a named failure. A
     mutant is graded only against an arm that passed unmutated in the same
     run, so a failure of the environment is never counted as a kill.
"""
from __future__ import annotations

import __future__
import ast
import contextlib
import importlib.abc
import inspect
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import textwrap
import types
from collections.abc import Callable, Generator, Iterator
from functools import partial
from pathlib import Path
from typing import Any, NamedTuple

from migen import ClockDomain, Module, run_simulation

from litex.soc.integration.builder import Builder
from litex.soc.interconnect import wishbone

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "sw/firmware/gtest"))
import ctrl_memory  # noqa: E402
import fw_rv32  # noqa: E402
import milan_soc  # noqa: E402

PLAT = ROOT / "sw/firmware/ctrl/plat"
DOC = ROOT / "docs/design/SPLIT_CONTROL_MEMORY.md"
GRANULE = 2048
RAM = ctrl_memory.RAM.origin
#: The largest shipped image's sram need (8x8, two interfaces): 64, 32, 8, 4 and 2 KiB banks.
LARGEST_NEED = 112_208
#: The words of the power-of-two window the SoC decodes for a 224 KiB region (adr[29:16] in the export).
WINDOW = (1 << (ctrl_memory.BUDGET_BYTES - 1).bit_length()) // 4
#: The shipping 1x1 shape, which stages 3,344 bytes; the 8x8 shape stages 13,264.
SOC_CONFIG = ROOT / "configs/endstation_ax7101_1x1_tdm8.yaml"
STAGE_1X1, STAGE_8X8 = 3344, 13264
PAIRING = "--ctrl-mailbox and --ctrl-firmware go together"
MODULES = {"ctrl_memory": ctrl_memory, "milan_soc": milan_soc}

#: What a migen stimulus process is: it yields reads and writes and is sent
#: back whatever a read resolved to.
Stim = Generator[Any, Any, Any]


def check(problems: list[str], ok: bool, what: str) -> None:
    """Record one graded fact."""
    print(f"  [{'ok  ' if ok else 'FAIL'}] {what}")
    if not ok:
        problems.append(what)


def refused(problems: list[str], rule: str, attempt: Callable[[], object], what: str) -> None:
    """`attempt` must raise ctrl_memory.Refusal for `rule`, under the check that rule belongs to."""
    want = ctrl_memory.RULES[rule].check
    try:
        attempt()
    except ctrl_memory.Refusal as exc:
        check(problems, (exc.rule, exc.check) == (rule, want),
              f"{what}: refused by '{exc.check}' rule '{exc.rule}' ({exc})")
        return
    except Exception as exc:     # an unnamed failure is not the refusal the rule promises
        check(problems, False, f"{what}: raised {type(exc).__name__} ({exc}), expected '{want}' rule '{rule}'")
        return
    check(problems, False, f"{what}: accepted, expected '{want}' rule '{rule}'")


def accepted(problems: list[str], attempt: Callable[[], object], what: str) -> object:
    """`attempt` must return; its result, or None with the failure recorded."""
    try:
        result = attempt()
    except Exception as exc:     # a refusal here is the failure this check exists to name
        check(problems, False, f"{what}: raised {type(exc).__name__} ({exc})")
        return None
    check(problems, True, what)
    return result


# ---- 1. banks --------------------------------------------------------------------------------

def bank_arms(problems: list[str]) -> None:
    """Every need from one byte past the budget, at granule edges and between them."""
    needs = sorted({1, GRANULE - 1, GRANULE, GRANULE + 1,
                    *range(0, ctrl_memory.BUDGET_BYTES + 8 * GRANULE, 509),
                    *(k * GRANULE + d for k in range(1, 120) for d in (-1, 0, 1))} - {0})
    bad = []
    for need in needs:
        granules = -(-need // GRANULE)
        got = ctrl_memory.banks(need)
        want = tuple(GRANULE << b for b in range(granules.bit_length() - 1, -1, -1) if granules >> b & 1)
        if got != want or sum(got) - need >= GRANULE or list(got) != sorted(got, reverse=True):
            bad.append(need)
    check(problems, not bad, f"{len(needs)} needs: power-of-two granule banks, largest first, "
                             f"under one granule spare (first wrong: {bad[:3]})")
    check(problems, ctrl_memory.banks(0) == (), "a zero need builds no bank")
    p = ctrl_memory.Plan(1, 1, (65536, 2048), (4096,))
    check(problems, (p.tiles, p.summary()["rom"]["RAMB36"], p.summary()["rom"]["RAMB18"],
                     p.summary()["sram"]["RAMB36"]) == (17.5, 16, 1, 1),
          "a plan counts a 2 KiB bank as one RAMB18, half a tile")


# ---- 2. rules, on ELFs written here ------------------------------------------------------------

def write_elf(entry: int, sections: list[tuple[str, int, int, bytes | int, bool]],
              symbols: dict[str, int], machine: int = 243) -> bytes:
    """A little-endian ELF32 executable, one PT_LOAD per section.

    A section is (name, address, load address, initial bytes or a NOBITS
    size, writable); a symbol is a name and the size of the object it names.
    """
    shstr = b"\0" + b"".join(n.encode() + b"\0" for n, *_ in sections) + b".symtab\0.strtab\0.shstrtab\0"
    strtab = b"\0" + b"".join(n.encode() + b"\0" for n in symbols)
    body, placed = b"", []
    base = 52 + 32 * len(sections)
    for _, _, _, data, _ in sections:
        payload = data if isinstance(data, bytes) else b""
        placed.append(base + len(body))
        body += payload + b"\0" * (-len(payload) % 4)
    symtab = bytes(16)
    for name, size in symbols.items():
        symtab += struct.pack("<IIIBBH", strtab.index(name.encode() + b"\0"), RAM, size, 0x11, 0, 1)
    tables = {"symtab": base + len(body)}
    body += symtab
    tables["strtab"] = base + len(body)
    body += strtab
    tables["shstrtab"] = base + len(body)
    body += shstr + b"\0" * (-len(shstr) % 4)
    shoff = base + len(body)
    head = struct.pack("<16sHHIIIIIHHHHHH", b"\x7fELF\x01\x01\x01" + bytes(9), 2, machine, 1, entry, 52, shoff,
                       0, 52, 32, len(sections), 40, len(sections) + 4, len(sections) + 3)
    programs = b""
    shdrs = bytes(40)
    for (name, vma, lma, data, writable), offset in zip(sections, placed):
        loaded = isinstance(data, bytes)
        size = len(data) if loaded else data
        programs += struct.pack("<8I", 1, offset, vma, lma, size if loaded else 0, size, 6, 4)
        shdrs += struct.pack("<10I", shstr.index(name.encode() + b"\0"), 1 if loaded else 8,
                             0x2 | (0x1 if writable else 0x4), vma, offset, size, 0, 0, 4, 0)
    n = len(sections)
    shdrs += struct.pack("<10I", shstr.index(b".symtab\0"), 2, 0, 0, tables["symtab"], len(symtab), n + 2, 1, 4, 16)
    shdrs += struct.pack("<10I", shstr.index(b".strtab\0"), 3, 0, 0, tables["strtab"], len(strtab), 0, 0, 1, 0)
    shdrs += struct.pack("<10I", shstr.index(b".shstrtab\0"), 3, 0, 0, tables["shstrtab"], len(shstr), 0, 0, 1, 0)
    return head + programs + body + shdrs


class Layout(NamedTuple):
    """A split image's shape; each planted defect moves one field."""

    entry: int = 0
    text_at: int = 0
    bss: int = 40_000
    data_at: int = RAM              # .data's run address
    data_lma: int | None = None     # its load address; None follows .rodata
    bss_at: int | None = None       # None follows .data in sram
    stage: int | None = STAGE_1X1   # nvm_stage's size; None leaves the symbol out
    machine: int = 243


GOOD = Layout()
#: The good image's rom need, .text and .rodata and .data's initial bytes, and its banks' bytes.
ROM_NEED = 9_000 + 3_004 + 64
ROM_BANKED = -(-ROM_NEED // GRANULE) * GRANULE
#: The .bss that brings the good image to exactly the budget: sram's banks fill what rom's leave.
BUDGET_BSS = ctrl_memory.BUDGET_BYTES - ROM_BANKED - 64 - 8192


def elf(tmp: Path, layout: Layout) -> Path:
    """Write `layout`: code and constants in rom, .data loaded from rom, .bss, the stack."""
    at = layout.text_at
    lma = at + 12_004 if layout.data_lma is None else layout.data_lma
    bss_at = RAM + 64 if layout.bss_at is None else layout.bss_at
    stack = RAM + 64 + layout.bss
    symbols = {"_start": 4} if layout.stage is None else {"_start": 4, ctrl_memory.STAGE_SYMBOL: layout.stage}
    path = tmp / ("image-" + "-".join(str(v) for v in layout) + ".elf")
    path.write_bytes(write_elf(layout.entry, [
        (".text", at, at, bytes((i * 7 + 3) & 0xFF for i in range(9_000)), False),
        (".rodata", at + 9_000, at + 9_000, bytes((i * 13 + 5) & 0xFF for i in range(3_002)), False),
        (".data", layout.data_at, lma, bytes(range(64)), True),
        (".bss", bss_at, bss_at, layout.bss, True),
        (".stack", stack, stack, 8192, True)], symbols, layout.machine))
    return path


def image(tmp: Path, layout: Layout) -> ctrl_memory.Image:
    """`layout` written, then read back by `read_elf`."""
    return ctrl_memory.read_elf(elf(tmp, layout))


def edited(tmp: Path, name: str, edit: Callable[[bytearray], None]) -> Path:
    """The good image's bytes with one edit, as a file."""
    data = bytearray(elf(tmp, GOOD).read_bytes())
    edit(data)
    path = tmp / f"{name}.elf"
    path.write_bytes(bytes(data))
    return path


def truncate(size: Callable[[int], int]) -> Callable[[bytearray], None]:
    """An edit that cuts the file to `size(len)` bytes."""
    def cut(data: bytearray) -> None:
        """Drop everything past the new end."""
        del data[size(len(data)):]
    return cut


def poke(offset: Callable[[bytearray], int], value: int) -> Callable[[bytearray], None]:
    """An edit that overwrites the 32-bit field at `offset(data)` with `value`."""
    def write(data: bytearray) -> None:
        """Pack the field in place."""
        struct.pack_into("<I", data, offset(data), value)
    return write


def splice(at: int, value: bytes) -> Callable[[bytearray], None]:
    """An edit that overwrites the bytes at `at` with `value`."""
    def write(data: bytearray) -> None:
        """Overwrite in place."""
        data[at:at + len(value)] = value
    return write


class FakeSoC:
    """The parts of a SoC that add_ctrl_memory reads and calls, recorded."""

    def __init__(self, reset_address: int, sram: int) -> None:
        """A CPU resetting to `reset_address`, with LiteX's sram origin at `sram`."""
        self.cpu = types.SimpleNamespace(reset_address=reset_address)
        self.mem_map = {"sram": sram}
        self.regions: dict[str, Any] = {}
        self.bus = types.SimpleNamespace(add_slave=self.add_slave)
        self.integrated_rom_initialized = False

    def add_module(self, name: str, module: object) -> None:
        """Keep the module as the SoC would, under its name."""
        setattr(self, name, module)

    def add_slave(self, name: str, bus: object, region: Any) -> None:
        """Keep the region each slave was given."""
        self.regions[name] = region


def refusal_arms(tmp: Path) -> list[tuple[str, str, Callable[[], object]]]:
    """One planted defect per rule, with the rule that must refuse it. Every call looks
    `ctrl_memory` and `milan_soc` up when it runs, so a mutant rebinding one is graded."""
    plan = lambda layout: lambda: ctrl_memory.plan(image(tmp, layout))  # noqa: E731
    read = lambda path: lambda: ctrl_memory.plan(ctrl_memory.read_elf(path))  # noqa: E731
    stage = lambda layout, size: lambda: ctrl_memory.check_stage(image(tmp, layout), size, "planted")  # noqa: E731
    cpu = lambda reset, sram: lambda: milan_soc.add_ctrl_memory(FakeSoC(reset, sram), elf(tmp, GOOD))  # noqa: E731
    shoff = lambda data: struct.unpack_from("<I", data, 32)[0]  # noqa: E731
    return [
        ("entry address", "an image entering away from the reset address", plan(GOOD._replace(entry=0x100))),
        ("entry bytes", "an image with no initial bytes at the reset address", plan(GOOD._replace(text_at=0x100))),
        ("cpu origins", "a CPU resetting away from rom's origin", cpu(0x100, RAM)),
        ("cpu origins", "a CPU whose sram is not at sram's origin", cpu(0, 0x2000_0000)),
        ("elf class", "a file that is not an ELF", read(edited(tmp, "not-elf", splice(0, b"#!sh")))),
        ("elf class", "an empty file", read(edited(tmp, "empty", truncate(lambda n: 0)))),
        ("elf class", "an ELF64 file", read(edited(tmp, "elf64", splice(4, b"\x02")))),
        ("elf class", "a big-endian ELF32 file", read(edited(tmp, "big-endian", splice(5, b"\x02")))),
        ("elf machine", "an x86 ELF32 file", plan(GOOD._replace(machine=3))),
        ("elf truncated", "an ELF cut inside its header", read(edited(tmp, "cut-40", truncate(lambda n: 40)))),
        ("elf truncated", "an ELF cut to half", read(edited(tmp, "cut-half", truncate(lambda n: n // 2)))),
        ("elf truncated", "a load segment past the end of the file",
         read(edited(tmp, "segment", poke(lambda data: 52 + 16, 1 << 20)))),
        ("elf truncated", "a section name past the end of the file",
         read(edited(tmp, "name", poke(lambda data: shoff(data) + 40, 1 << 30)))),
        ("outside regions", "a section outside rom and sram", plan(GOOD._replace(bss_at=0x4000_0000))),
        ("loads outside rom", "initial bytes of .data left in sram, which nothing initialises",
         plan(GOOD._replace(data_lma=RAM))),
        ("nobits in rom", ".bss reserved in rom", plan(GOOD._replace(bss_at=12_100, bss=1_000))),
        ("writable in rom", ".data linked to run in rom", plan(GOOD._replace(data_at=12_100, data_lma=12_100))),
        ("regions", "PLANTED: a memory-map overlap (sram moved into rom)",
         lambda: ctrl_memory.plan(image(tmp, GOOD), ram=ctrl_memory.Region("sram", 0x2_0000, ctrl_memory.ROM.size))),
        ("addresses", "PLANTED: a memory-map overlap (.bss over .data)", plan(GOOD._replace(bss_at=RAM + 32))),
        ("initial bytes", ".data's initial bytes loading over .rodata's", plan(GOOD._replace(data_lma=9_000))),
        ("budget", "PLANTED: an allocation over budget (215,000 bytes of .bss: 58 RAMB36, each region inside its own)",
         plan(GOOD._replace(bss=215_000))),
        ("budget", "an allocation of 56.5 RAMB36, half a tile over", plan(GOOD._replace(bss=BUDGET_BSS + GRANULE))),
        ("stage symbol", "an image with no nvm_stage", stage(GOOD._replace(stage=None), STAGE_1X1)),
        ("stage size", "PLANTED: a staging buffer sized for another shape (1x1 image, 8x8 stage)",
         stage(GOOD, STAGE_8X8)),
        ("stage size", "PLANTED: a staging buffer sized for another shape (8x8 image, 1x1 stage)",
         stage(GOOD._replace(stage=STAGE_8X8), STAGE_1X1)),
    ]


def check_arms(problems: list[str], tmp: Path) -> None:
    """The good image, the budget boundary, the hookup's own effects, then every refusal by its rule."""
    plan = accepted(problems, lambda: ctrl_memory.plan(image(tmp, GOOD)), "the good image is planned")
    if plan is not None:
        check(problems, (plan.rom_bytes, plan.ram_bytes) == (ROM_NEED, 64 + 40_000 + 8192),
              f"the plan's needs are rom to the end of .data's initial bytes, sram to the stack's top "
              f"({plan.rom_bytes}, {plan.ram_bytes})")
    raw = b""
    with contextlib.suppress(Exception):     # a mutant that breaks the reader fails the check below
        words = ctrl_memory.rom_words(image(tmp, GOOD))
        raw = struct.pack(f"<{len(words)}I", *words)
    check(problems, raw[:4] == bytes((3, 10, 17, 24)) and raw[9_000:9_002] == bytes((5, 18))
          and raw[12_004:12_068] == bytes(range(64)),
          "rom holds .text at the reset address, .rodata after it and .data's initial bytes at their load address")
    accepted(problems, lambda: ctrl_memory.check_stage(image(tmp, GOOD), STAGE_1X1, "1x1"),
             "a staging buffer of the shape's size is accepted")
    full = accepted(problems, lambda: ctrl_memory.plan(image(tmp, GOOD._replace(bss=BUDGET_BSS))),
                    "an allocation of exactly 56 RAMB36 is accepted")
    check(problems, getattr(full, "tiles", None) == 56.0, f"that allocation plans 56.0 RAMB36 ({full and full.tiles})")
    soc = FakeSoC(ctrl_memory.ROM.origin, RAM)
    accepted(problems, lambda: milan_soc.add_ctrl_memory(soc, elf(tmp, GOOD)), "add_ctrl_memory builds the image")
    regions = {name: (r.origin, r.size, r.mode) for name, r in soc.regions.items()}
    check(problems, regions == {"rom": (0, ctrl_memory.ROM.size, "rx"), "sram": (RAM, ctrl_memory.RAM.size, "rwx")}
          and all(isinstance(getattr(soc, n, None), milan_soc.CtrlMemory) for n in ("rom", "sram")),
          f"add_ctrl_memory adds rom (rx) and sram (rwx) as CtrlMemory, each the whole 224 KiB ({regions})")
    check(problems, soc.integrated_rom_initialized is True,
          "add_ctrl_memory tells LiteX's Builder that rom holds its contents, so it builds no BIOS")
    for rule, what, attempt in refusal_arms(tmp):
        refused(problems, rule, attempt, what)
    text = ctrl_memory.regions_ld()
    check(problems, "rom (rx) : ORIGIN = 0x00000000, LENGTH = 0x00038000" in text
          and "sram (rwx) : ORIGIN = 0x10000000, LENGTH = 0x00038000" in text,
          "regions.ld states both regions at the CPU's origins, each the whole 224 KiB budget")


# ---- 3. banks in simulation --------------------------------------------------------------------

def request(bus: wishbone.Interface, adr: int, we: int = 0, dat: int = 0, sel: int = 0xF) -> Stim:
    """Present one Wishbone request and hold it."""
    yield bus.adr.eq(adr)
    yield bus.we.eq(we)
    yield bus.dat_w.eq(dat)
    yield bus.sel.eq(sel)
    yield bus.cyc.eq(1)
    yield bus.stb.eq(1)


def response(bus: wishbone.Interface) -> Stim:
    """('ack' | 'err' | 'both' | 'none', dat_r) within eight clocks of the request."""
    for _ in range(8):
        yield
        ack, err = (yield bus.ack), (yield bus.err)
        if ack or err:
            return {(1, 0): "ack", (0, 1): "err"}.get((ack, err), "both"), (yield bus.dat_r)
    return "none", None


def release(bus: wishbone.Interface) -> Stim:
    """End the cycle, with one idle clock."""
    yield bus.cyc.eq(0)
    yield bus.stb.eq(0)
    yield


def access(bus: wishbone.Interface, adr: int, we: int = 0, dat: int = 0, sel: int = 0xF) -> Stim:
    """One Wishbone cycle and its answer."""
    yield from request(bus, adr, we, dat, sel)
    answer = yield from response(bus)
    yield from release(bus)
    return answer


def back_to_back(bus: wishbone.Interface, hole: int, good: int) -> Stim:
    """A read of `hole`, then a read of `good` presented on the cycle the first answer is seen."""
    yield from request(bus, hole)
    first = yield from response(bus)
    yield bus.adr.eq(good)
    second = yield from response(bus)
    yield from release(bus)
    return first, second


def pattern(i: int) -> int:
    """A word that names its own index."""
    return (i * 0x9E37_79B1 + 0x0102_0304) & 0xFFFF_FFFF


class Bench(Module):
    """rom and sram as add_ctrl_memory builds them, for one need."""

    def __init__(self, need: int) -> None:
        """Both regions, with the same banks."""
        self.clock_domains.cd_sys = ClockDomain("sys")
        self.banks = ctrl_memory.banks(need)
        self.words = sum(self.banks) // 4
        self.submodules.rom = milan_soc.CtrlMemory(ctrl_memory.ROM, self.banks,
                                                   [pattern(i) for i in range(need // 4)])
        self.submodules.ram = milan_soc.CtrlMemory(ctrl_memory.RAM, self.banks, None)


def hole_addresses(words: int) -> list[int]:
    """Word addresses past the last bank to the top of the decoded window: its edges, the
    upper half a decode one bit short would alias, the 224 KiB edge and a stride across."""
    half, region = WINDOW // 2, ctrl_memory.BUDGET_BYTES // 4
    marks = {words, words + 1, half - 1, half, half + 1, half + words - 1, region - 1, region, region + 1,
             WINDOW - 2, WINDOW - 1, *range(words, WINDOW, 1021)}
    return sorted(a for a in marks if words <= a < WINDOW)


def sweep(bus: wishbone.Interface, addresses: list[int], we: int = 0, dat: int = 0) -> Stim:
    """One access to each address, in order; their answers."""
    out = []
    for a in addresses:
        out.append((yield from access(bus, a, we, dat)))
    return out


def sim_arms(problems: list[str], need: int = LARGEST_NEED) -> None:
    """Every bank's edges in both regions, the whole hole, back-to-back after err, the refused rom write."""
    bench = Bench(need)
    edges, offsets, first = [], [], 0
    for size in bench.banks:
        edges += [first, first + 1, first + size // 4 - 1]
        offsets.append(first)
        first += size // 4
    holes = hole_addresses(bench.words)
    alias = sorted({f + a % (s // 4) for a in holes for f, s in zip(offsets, bench.banks)})
    base, marker = RAM // 4, 0x5555_5555
    lanes = [((pattern(a) ^ 0xFFFF_0000) & ~(0xFF << 8 * (n % 4))) | (0xA5 << 8 * (n % 4))
             for n, a in enumerate(edges)]
    seen: dict[str, Any] = {}

    def run() -> Stim:
        """Read rom and try its hole, write and read sram and try its hole, then read every alias cell."""
        seen["rom"] = yield from sweep(bench.rom.bus, [a for a in edges if a < need // 4])
        seen["rom_write"] = yield from access(bench.rom.bus, edges[1], we=1, dat=0xDEAD_BEEF)
        seen["rom_after"] = yield from access(bench.rom.bus, edges[1])
        seen["rom_hole"] = yield from sweep(bench.rom.bus, holes)
        seen["rom_b2b"] = yield from back_to_back(bench.rom.bus, holes[0], edges[1])
        for n, a in enumerate(edges):
            yield from access(bench.ram.bus, base + a, we=1, dat=pattern(a) ^ 0xFFFF_0000)
            yield from access(bench.ram.bus, base + a, we=1, dat=0xA5 << (8 * (n % 4)), sel=1 << (n % 4))
        seen["ram"] = yield from sweep(bench.ram.bus, [base + a for a in edges])
        seen["ram_hole"] = yield from sweep(bench.ram.bus, [base + a for a in holes], we=1, dat=marker)
        seen["ram_alias"] = yield from sweep(bench.ram.bus, [base + a for a in alias])
        seen["ram_b2b"] = yield from back_to_back(bench.ram.bus, base + holes[-1], base + edges[0])

    run_simulation(bench, run())
    span = f"{len(holes)} addresses from word 0x{holes[0]:x} to the window's top 0x{WINDOW - 1:x}"
    check(problems, seen["rom"] == [("ack", pattern(a)) for a in edges if a < need // 4],
          f"rom reads its image at the first, second and last word of each of {len(bench.banks)} banks "
          f"({', '.join(str(s // 1024) for s in bench.banks)} KiB)")
    check(problems, seen["rom_write"][0] == "ack" and seen["rom_after"] == ("ack", pattern(edges[1])),
          "a write to rom changes nothing")
    for region in ("rom", "ram"):
        wrong = [(hex(a), r[0]) for a, r in zip(holes, seen[f"{region}_hole"]) if r[0] != "err"]
        check(problems, not wrong, f"{region} answers err alone at all {span} (first wrong: {wrong[:3]})")
    check(problems, seen["ram"] == [("ack", w) for w in lanes],
          "sram keeps each byte lane written at every bank's edges, the other lanes intact")
    check(problems, all(r[0] == "ack" and r[1] != marker for r in seen["ram_alias"]),
          f"a write past the last bank lands in none of the {len(alias)} cells it would alias")
    check(problems, seen["rom_b2b"] == (("err", seen["rom_b2b"][0][1]), ("ack", pattern(edges[1]))),
          f"rom: a read presented on the cycle after an err acks with its own data ({seen['rom_b2b']})")
    check(problems, seen["ram_b2b"] == (("err", seen["ram_b2b"][0][1]), ("ack", lanes[0])),
          f"sram: a read presented on the cycle after an err acks with its own data ({seen['ram_b2b']})")


# ---- 4. the link ---------------------------------------------------------------------------

PROBE = """\
int counter = 7;
unsigned char nvm_stage[3344];
int main(void) { return counter + nvm_stage[counter]; }
"""


def link(cc: str, tmp: Path, script: str) -> Path:
    """The probe linked by `script` behind the reset entry."""
    (tmp / "regions.ld").write_text(ctrl_memory.regions_ld())
    (tmp / "probe.c").write_text(PROBE)
    (tmp / "split.ld").write_text(script)
    flags = ["-march=rv32i", "-mabi=ilp32"]
    subprocess.run([cc, *flags, "-ffreestanding", "-Os", "-c", str(tmp / "probe.c"), "-o", str(tmp / "probe.o")],
                   check=True)
    subprocess.run([cc, *flags, "-c", str(PLAT / "ctrl_split_start.S"), "-o", str(tmp / "start.o")], check=True)
    elf_path = tmp / "probe.elf"
    subprocess.run([cc, *flags, "-nostdlib", "-static", "-no-pie", "-Wl,--gc-sections,--build-id=none",
                    "-T", str(tmp / "split.ld"), f"-L{tmp}", str(tmp / "start.o"), str(tmp / "probe.o"),
                    "-o", str(elf_path)], check=True)
    return elf_path


def link_arms(problems: list[str], tmp: Path) -> bool:
    """The real link script and reset entry; False when no RV32 compiler is found."""
    cc = fw_rv32.compiler()
    if cc is None:
        print("  [skip] no RV32 compiler: the link arm did not run")
        return False
    script = (PLAT / "ctrl_split.ld").read_text()
    probe = ctrl_memory.read_elf(link(cc, tmp, script))
    plan = ctrl_memory.plan(probe)
    sections = {s.name: s for s in probe.sections}
    words = ctrl_memory.rom_words(probe)
    data = sections[".data"]
    check(problems, probe.entry == 0 and words[0] & 0xFFF == 0x117,
          "the probe enters at the reset address, whose first word is the reset entry's auipc sp")
    check(problems, data.vma == RAM and data.lma < plan.rom_bytes and data.writable
          and words[data.lma // 4] == 7, ".data runs in sram and its initial value 7 loads from rom")
    check(problems, sections[".stack"].vma + sections[".stack"].size == RAM + plan.ram_bytes,
          "the stack tops the sram need")
    ctrl_memory.check_stage(probe, STAGE_1X1, "1x1")
    check(problems, True, "the probe's nvm_stage passes as the shape's stage")
    for plant, edit, rule in (("no AT > rom on .data", ("} > sram AT > rom", "} > sram"), "loads outside rom"),
                              (".data in rom", ("} > sram AT > rom", "} > rom"), "writable in rom"),
                              ("ENTRY(main)", ("ENTRY(_start)", "ENTRY(main)"), "entry address")):
        broken = tmp / re.sub(r"\W+", "-", plant)
        broken.mkdir()
        refused(problems, rule, lambda b=broken, e=edit: ctrl_memory.plan(
            ctrl_memory.read_elf(link(cc, b, script.replace(*e)))), f"PLANTED link script: {plant}")
    return True


# ---- 5. the SoC build ----------------------------------------------------------------------

#: The shipping 1x1 config's own SoC argv, built once per run.
SOC_ARGV: list[str] = []


def soc_argv() -> list[str]:
    """The shipping 1x1 config's argv from the end-station builder, its output written first."""
    if not SOC_ARGV:
        sys.path.insert(0, str(ROOT / "sw/builder"))
        try:
            import endstation_builder as eb
        except SystemExit as exc:     # the builder exits when PyYAML is absent
            raise RuntimeError(f"the end-station builder cannot load: {exc}") from exc
        cfg = eb.load_config(str(SOC_CONFIG))
        with contextlib.redirect_stdout(None):
            eb.build(str(SOC_CONFIG))
        SOC_ARGV.extend(eb.emit_soc_argv(cfg) + ["--entity-gen-dir", str(ROOT / "configs/generated" / cfg["name"])])
    return SOC_ARGV


class FirmwareDataRefused(importlib.abc.MetaPathFinder):
    """Refuse LiteX's firmware data packages, which the pinned elaborate install lacks."""

    def find_spec(self, name: str, path: Any = None, target: Any = None) -> None:
        """Fail any pythondata_software_* import and defer every other module."""
        if name.startswith("pythondata_software_"):
            raise ImportError(f"{name}: sw/litex/litex_pins.txt installs no firmware data package")
        return None


def soc_child(spec_path: Path) -> int:
    """In a child process: milan_soc.main() on the spec's argv, its mutation applied; write what it decided."""
    spec = json.loads(spec_path.read_text())
    if spec["mutation"]:
        owner, name, old, new = spec["mutation"]
        setattr(MODULES[owner], name, mutated(MODULES[owner], name, old, new))
    # As sw/builder/test_shipping_clock_constraints.py does: the elaborate job
    # installs sw/litex/litex_pins.txt alone, so no interpreter may reach a
    # firmware data package here (#640, R606-2-F2).
    sys.meta_path.insert(0, FirmwareDataRefused())
    result: dict[str, Any] = {"rc": 0, "includes": []}
    original, original_includes = Builder.build, Builder._generate_includes

    def generate_includes(self: Builder, with_bios: bool = True) -> None:
        """Write the SoC headers, omitting only the firmware make inputs."""
        # Those inputs name the picolibc and compiler-rt data packages. Nothing
        # is compiled here, and the gateware and its init files read neither.
        result["includes"].append(with_bios)
        original_includes(self, with_bios=False)

    def build(self: Builder, **kwargs: Any) -> object:
        """Record what the Builder is handed, then build as asked."""
        soc = self.soc
        result["builder"] = {"rom": soc.integrated_rom_size, "sram": soc.integrated_sram_size,
                             "initialized": soc.integrated_rom_initialized,
                             "packages": [name for name, _ in self.software_packages]}
        return original(self, **kwargs)

    Builder.build, Builder._generate_includes = build, generate_includes
    sys.argv = ["milan_soc.py", *spec["argv"]]
    try:
        milan_soc.main()
    except SystemExit as exc:
        result["rc"] = 0 if exc.code is None else exc.code if isinstance(exc.code, int) else 1
    except ctrl_memory.Refusal as exc:
        result.update(rc=1, rule=exc.rule, refusal=str(exc))
    except Exception as exc:     # any other failure is recorded as itself, never as a refusal
        result.update(rc=1, error=f"{type(exc).__name__}: {exc}")
    Path(spec["result"]).write_text(json.dumps(result))
    return 0


def soc_case(tmp: Path, label: str, extra: list[str], mutation: list[str] | None) -> dict[str, Any]:
    """One child run of milan_soc.main(); its result, log and export directory."""
    stem = tmp / re.sub(r"\W+", "-", label).strip("-")
    out, spec, log = stem / "export", stem.with_suffix(".json"), stem.with_suffix(".log")
    stem.mkdir(parents=True)
    spec.write_text(json.dumps({"argv": [*soc_argv(), *extra, "--output-dir", str(out), "--no-compile-software"],
                                "result": str(stem.with_suffix(".result.json")), "mutation": mutation}))
    with log.open("w") as fh:
        subprocess.run([sys.executable, str(Path(__file__).resolve()), "--soc-child", str(spec)], cwd=HERE,
                       env=dict(os.environ, PYTHONHASHSEED="0"), stdout=fh, stderr=subprocess.STDOUT, check=False)
    result_path = stem.with_suffix(".result.json")
    result = json.loads(result_path.read_text()) if result_path.exists() else {"rc": None, "error": "no result"}
    result.update(log=log.read_text(), out=out, verilog=sorted(out.glob("gateware/*.v")))
    return result


def split_export(problems: list[str], result: dict[str, Any], firmware: Path) -> None:
    """The passing split export: the image's banks and contents, the map, and no BIOS."""
    check(problems, result["rc"] == 0 and len(result["verilog"]) == 1,
          f"the split build exports (rc {result['rc']}, {result.get('error') or result.get('refusal') or 'no error'})")
    if result["rc"] != 0 or len(result["verilog"]) != 1:
        return
    linked = ctrl_memory.read_elf(firmware)
    plan, out = ctrl_memory.plan(linked), result["out"]
    memories = dict(re.findall(r"^reg \[31:0\] (\w+)\[0:(\d+)\];", result["verilog"][0].read_text(), re.M))
    want = {f"{region}_bank{n}": str(size // 4 - 1)
            for region, banks in (("rom", plan.rom_banks), ("sram", plan.ram_banks)) for n, size in enumerate(banks)}
    check(problems, {k: v for k, v in memories.items() if "_bank" in k} == want,
          f"the split export's memories are the image's banks ({sorted(want)})")
    check(problems, not {"rom", "sram"} & set(memories), "the split export holds no BIOS ROM and no BIOS SRAM")
    inits = sorted(out.glob("gateware/*_rom_bank*.init"), key=lambda p: int(p.stem.rsplit("bank", 1)[1]))
    words = [int(w, 16) for p in inits for w in p.read_text().split()]
    check(problems, words == ctrl_memory.rom_words(linked), "the rom banks' init files hold the image word for word")
    rows = [line.split(",") for line in (out / "csr.csv").read_text().splitlines() if line.startswith("memory_region,")]
    regions = {row[1]: (row[2], row[3]) for row in rows}
    want_regions = {r.name: (f"0x{r.origin:08x}", str(r.size)) for r in (ctrl_memory.ROM, ctrl_memory.RAM)}
    check(problems, {k: regions.get(k) for k in want_regions} == want_regions,
          f"csr.csv maps rom and sram at the CPU's origins, each 224 KiB ({regions.get('rom')}, {regions.get('sram')})")
    told = result.get("builder", {})
    check(problems, (told.get("rom"), told.get("sram"), told.get("initialized")) == (0, 0, True),
          f"the Builder is handed no BIOS ROM or SRAM and a rom that holds its contents, so builds no BIOS ({told})")
    check(problems, result.get("includes") == [True],
          f"the Builder writes the SoC headers once, without the firmware make inputs ({result.get('includes')})")
    check(problems, "libmilan_baremetal" not in told.get("packages", ["?"])
          and not (out / "software/libmilan_baremetal").exists(), "the split build adds no shipping firmware")


def soc_arms(problems: list[str], tmp: Path, mutation: list[str] | None = None) -> None:
    """The planted controls, the flag pairings and the split export, through milan_soc.main()."""
    tmp.mkdir(parents=True, exist_ok=True)
    good = elf(tmp, GOOD)
    mbx = ["--ctrl-mailbox", "--ctrl-firmware"]
    for label, extra, rule in (
            ("an allocation over budget", [*mbx, str(elf(tmp, GOOD._replace(bss=215_000)))], "budget"),
            ("a memory-map overlap", [*mbx, str(elf(tmp, GOOD._replace(bss_at=RAM + 32)))], "addresses"),
            ("the 8x8 stage in the 1x1 build", [*mbx, str(elf(tmp, GOOD._replace(stage=STAGE_8X8)))], "stage size")):
        result = soc_case(tmp, label, extra, mutation)
        check(problems, (result["rc"], result.get("rule"), result["verilog"]) == (1, rule, []),
              f"SoC build: {label} is refused by rule '{rule}' before any Verilog is written "
              f"(rc {result['rc']}: {result.get('refusal') or result.get('error')})")
    for label, extra in (("--ctrl-mailbox alone", ["--ctrl-mailbox"]),
                         ("--ctrl-firmware alone", ["--ctrl-firmware", str(good)])):
        result = soc_case(tmp, label, extra, mutation)
        check(problems, result["rc"] == 2 and PAIRING in result["log"] and not result["verilog"],
              f"SoC build: {label} is refused, '{PAIRING}' (rc {result['rc']}: {result.get('error', '')})")
    result = soc_case(tmp, "the split build", [*mbx, str(good)], mutation)
    split_export(problems, result, good)
    shutil.rmtree(tmp)


# ---- 6. the register, and 7. the mutants ---------------------------------------------------

class Mutant(NamedTuple):
    """One edit of one function or class, and the rule or property it removes or weakens."""

    name: str
    target: str
    owner: str
    attribute: str
    old: str
    new: str
    arm: str


#: What the mutants target besides ctrl_memory.RULES: the documented behaviour that is not a refusal.
PROPERTIES = {
    "load address": "a section's load address is read through its segment",
    "bank order": "banks are largest first",
    "decode width": "a region decodes its whole window",
    "hole width": "the hole compares the whole window",
    "hole start": "the hole starts at the first word past the last bank",
    "hole answer": "the hole answers err",
    "err pulse": "err lasts one cycle",
    "rom contents": "each rom bank holds its own words of the image",
    "read-only rom": "rom drops writes",
    "no BIOS build": "add_ctrl_memory tells the Builder that rom holds its contents",
    "no BIOS memory": "the split build adds no BIOS ROM or SRAM",
    "memory hookup": "the split build adds the control memory",
    "stage in main": "main() runs the staging check before any export",
    "pairing": "--ctrl-mailbox and --ctrl-firmware are refused apart",
    "no shipping firmware": "the split build adds no shipping firmware library",
}

_CHECKS = ("ctrl_memory", "check_map")
_ORIGINS = 'if (soc.cpu.reset_address, soc.mem_map["sram"]) != (ctrl_memory.ROM.origin, ctrl_memory.RAM.origin):'
_ERR = "hole.err.eq(hole.cyc & hole.stb & ~hole.err)"
_HOLE = "slaves.append((lambda a: a[:low] >= first, hole))"
_BIOS = "kwargs.update(integrated_rom_size=0, integrated_sram_size=0)"
MUTANTS = tuple(Mutant(*row) for row in (
    ("elf class weakened", "elf class", "ctrl_memory", "read_elf",
     'if data[:6] != b"\\x7fELF\\x01\\x01":', 'if data[:4] != b"\\x7fELF":', "checks"),
    ("elf machine off", "elf machine", "ctrl_memory", "read_elf", "if machine != _EM_RISCV:", "if False:", "checks"),
    ("truncated fields read", "elf truncated", "ctrl_memory", "_unpack",
     "if offset + struct.calcsize(layout) > len(data):", "if False:", "checks"),
    ("truncated segments read", "elf truncated", "ctrl_memory", "read_elf",
     "if offset + filesz > len(data):", "if False:", "checks"),
    ("unterminated names read", "elf truncated", "ctrl_memory", "_string", "if end < 0:", "if False:", "checks"),
    ("load address read as the run address", "load address", "ctrl_memory", "read_elf",
     "return paddr + vma - vaddr", "return vma", "checks"),
    ("entry address off", "entry address", *_CHECKS, "if image.entry != rom.origin:", "if False:", "checks"),
    ("entry bytes off", "entry bytes", *_CHECKS, "if not any(s.loaded and s.vma <= image.entry",
     "if False and not any(s.loaded and s.vma <= image.entry", "checks"),
    ("outside regions off", "outside regions", *_CHECKS, "if home is None:", "if False:", "checks"),
    ("loads outside rom off", "loads outside rom", *_CHECKS,
     "if s.loaded and not rom.holds(s.lma, s.lma + s.size):", "if False:", "checks"),
    ("nobits in rom off", "nobits in rom", *_CHECKS, "if not s.loaded and home is rom:", "if False:", "checks"),
    ("writable in rom off", "writable in rom", *_CHECKS, "if s.writable and home is rom:", "if False:", "checks"),
    ("region overlap off", "regions", *_CHECKS, '_overlap("regions", ', '0 and _overlap("regions", ', "checks"),
    ("address overlap off", "addresses", *_CHECKS, '_overlap("addresses", ', '0 and _overlap("addresses", ',
     "checks"),
    ("load-address overlap off", "initial bytes", *_CHECKS, '_overlap("initial bytes", ',
     '0 and _overlap("initial bytes", ', "checks"),
    ("budget off", "budget", "ctrl_memory", "plan", "if need.tiles > budget:", "if False:", "checks"),
    ("budget refuses exactly 56", "budget", "ctrl_memory", "plan", "if need.tiles > budget:",
     "if need.tiles >= budget:", "checks"),
    ("budget half a tile slack", "budget", "ctrl_memory", "plan", "if need.tiles > budget:",
     "if need.tiles > budget + 0.5:", "checks"),
    ("budget 1.5 tiles slack", "budget", "ctrl_memory", "plan", "if need.tiles > budget:",
     "if need.tiles > budget + 1.5:", "checks"),
    ("stage symbol off", "stage symbol", "ctrl_memory", "check_stage", "if STAGE_SYMBOL not in image.symbols:",
     "if False:", "checks"),
    ("stage size off", "stage size", "ctrl_memory", "check_stage", "if size != stage:", "if False:", "checks"),
    ("stage accepts a larger buffer", "stage size", "ctrl_memory", "check_stage", "if size != stage:",
     "if size < stage:", "checks"),
    ("stage accepts a smaller buffer", "stage size", "ctrl_memory", "check_stage", "if size != stage:",
     "if size > stage:", "checks"),
    ("banks smallest first", "bank order", "ctrl_memory", "banks", "reversed(range(granules.bit_length()))",
     "range(granules.bit_length())", "banks"),
    ("cpu origins off", "cpu origins", "milan_soc", "add_ctrl_memory", _ORIGINS, "if False:", "checks"),
    ("cpu origins read the reset address only", "cpu origins", "milan_soc", "add_ctrl_memory", _ORIGINS,
     "if soc.cpu.reset_address != ctrl_memory.ROM.origin:", "checks"),
    ("rom left uninitialised for the Builder", "no BIOS build", "milan_soc", "add_ctrl_memory",
     "soc.integrated_rom_initialized = True", "soc.integrated_rom_initialized = False", "checks"),
    ("decode one bit short", "decode width", "milan_soc", "CtrlMemory",
     "low = (region.size - 1).bit_length() - 2", "low = (region.size - 1).bit_length() - 3", "sim"),
    ("hole compares one bit short", "hole width", "milan_soc", "CtrlMemory", _HOLE,
     _HOLE.replace("a[:low]", "a[:low - 1]"), "sim"),
    ("hole starts a word late", "hole start", "milan_soc", "CtrlMemory", _HOLE, _HOLE.replace(">=", ">"), "sim"),
    ("hole answers nothing", "hole answer", "milan_soc", "CtrlMemory", f"self.sync += {_ERR}",
     "self.sync += hole.err.eq(0)", "sim"),
    ("err held a second cycle", "err pulse", "milan_soc", "CtrlMemory", _ERR, "hole.err.eq(hole.cyc & hole.stb)",
     "sim"),
    ("rom banks from the image start", "rom contents", "milan_soc", "CtrlMemory", "words[first:first + depth]",
     "words[0:depth]", "sim"),
    ("a writable rom", "read-only rom", "milan_soc", "CtrlMemory", "read_only=words is not None",
     "read_only=False", "sim"),
    ("BIOS ROM built", "no BIOS memory", "milan_soc", "MilanSoC", _BIOS, "kwargs.update(integrated_sram_size=0)",
     "soc"),
    ("BIOS SRAM built", "no BIOS memory", "milan_soc", "MilanSoC", _BIOS, "kwargs.update(integrated_rom_size=0)",
     "soc"),
    ("control memory not added", "memory hookup", "milan_soc", "MilanSoC",
     "add_ctrl_memory(self, Path(ctrl_firmware))", "None", "soc"),
    ("main() staging check removed", "stage in main", "milan_soc", "main",
     "ctrl_memory.check_stage(soc.ctrl_image,", "(soc.ctrl_image,", "soc"),
    ("flag pairing off", "pairing", "milan_soc", "main",
     "if args.ctrl_mailbox != (args.ctrl_firmware is not None):", "if False:", "soc"),
    ("shipping firmware linked", "no shipping firmware", "milan_soc", "main",
     'if args.software_profile == "baremetal" and not args.ctrl_mailbox:', 'if args.software_profile == "baremetal":',
     "soc"),
))


def mutated(owner: types.ModuleType, name: str, old: str, new: str) -> Any:
    """`owner.name` rebuilt from its own source with `old` replaced by `new`, which must match once.

    The text compiled is the module's own definition of `name` and nothing else:
    it must parse to exactly that one definition, and it runs in the module's
    own namespace, so the rebuilt object sees every other name as it was.
    """
    source = textwrap.dedent(inspect.getsource(getattr(owner, name)))
    if source.count(old) != 1:
        raise LookupError(f"{owner.__name__}.{name}: the edit matches {source.count(old)} times, not once")
    edited_source = source.replace(old, new)
    tree = ast.parse(edited_source)
    if [getattr(node, "name", None) for node in tree.body] != [name]:
        raise LookupError(f"{owner.__name__}.{name}: the edited source is not one definition of {name}")
    scope: dict[str, Any] = {}
    exec(compile(edited_source, f"<mutant of {owner.__name__}.{name}>", "exec",
                 flags=__future__.annotations.compiler_flag, dont_inherit=True), vars(owner), scope)
    return scope[name]


@contextlib.contextmanager
def patched(owner: object, name: str, value: object) -> Iterator[None]:
    """Replace `owner.name` for the duration of one mutant."""
    original = getattr(owner, name)
    setattr(owner, name, value)
    try:
        yield
    finally:
        setattr(owner, name, original)


def doc_rules() -> list[tuple[str, str, str]]:
    """(check, rule, refuses) for each row of SPLIT_CONTROL_MEMORY.md section 3's rule table."""
    section = DOC.read_text().split("## 3. Named refusals", 1)[-1].split("\n## ", 1)[0]
    return re.findall(r"^\| `([^`]+)` \| `([^`]+)` \| (.+?) \|$", section, re.M)


def registry_arms(problems: list[str], tmp: Path) -> None:
    """The documented rules are the registered ones, and each has a refusal arm and a mutant."""
    want = [(rule.check, key, rule.refuses) for key, rule in ctrl_memory.RULES.items()]
    got = doc_rules()
    differ = next((pair for pair in zip(got, want) if pair[0] != pair[1]), None)
    check(problems, got == want, f"SPLIT_CONTROL_MEMORY.md section 3 lists the {len(want)} rules of "
                                 f"ctrl_memory.RULES in order ({len(got)} rows; first difference: {differ})")
    rules = set(ctrl_memory.RULES)
    armed = {rule for rule, _, _ in refusal_arms(tmp)}
    mutants = {m.target for m in MUTANTS}
    check(problems, armed >= rules, f"every rule has a refusal arm (none: {sorted(rules - armed)})")
    check(problems, mutants >= rules,
          f"every rule has a mutant that removes or weakens it (none: {sorted(rules - mutants)})")
    check(problems, mutants <= rules | set(PROPERTIES),
          f"every mutant targets a rule or a named property (stray: {sorted(mutants - rules - set(PROPERTIES))})")


def mutant_arms(problems: list[str], tmp: Path, green: set[str]) -> None:
    """Each mutant must turn its arm red, named by the first failure it causes.

    Only an arm in `green`, one that passed unmutated in this run, grades a
    mutant: a failure the arm shows anyway is no evidence that the mutant is caught.
    """
    arms = {"banks": bank_arms, "checks": partial(check_arms, tmp=tmp), "sim": sim_arms}
    for n, m in enumerate(MUTANTS):
        if m.arm not in green:
            check(problems, False, f"MUTANT '{m.name}' ({m.target}) is not graded: the {m.arm} arm fails unmutated")
            continue
        caught: list[str] = []
        owner = MODULES[m.owner]
        try:
            rebuilt = mutated(owner, m.attribute, m.old, m.new)
        except LookupError as exc:
            check(problems, False, f"MUTANT '{m.name}': {exc}")
            continue
        with contextlib.redirect_stdout(None):
            try:
                if m.arm == "soc":
                    soc_arms(caught, tmp / f"mutant-{n}", [m.owner, m.attribute, m.old, m.new])
                else:
                    with patched(owner, m.attribute, rebuilt):
                        arms[m.arm](caught)
            except Exception as exc:     # a mutant that breaks an arm outright is caught too
                caught.append(f"the arm raised {type(exc).__name__}: {exc}")
        check(problems, bool(caught), f"MUTANT '{m.name}' ({m.target}) is caught by the {m.arm} arm: "
                                      f"{caught[0] if caught else 'nothing went red'}")


def run_arm(problems: list[str], label: str, arm: Callable[[list[str]], object]) -> object:
    """Run one arm; an exception out of it is a named failure, never a crash."""
    print(f"-- {label}")
    try:
        return arm(problems)
    except Exception as exc:     # every arm reports through `problems`, so an escape is a failure
        check(problems, False, f"the {label} arm raised {type(exc).__name__}: {exc}")
        return None


def main() -> int:
    """Every arm; exit 1 naming each failure."""
    if sys.argv[1:2] == ["--soc-child"]:
        return soc_child(Path(sys.argv[2]))
    problems: list[str] = []
    print("test_ctrl_memory: the split placement's firmware memory (#640 M8a)")
    with tempfile.TemporaryDirectory(prefix="ctrl-memory-") as name:
        tmp = Path(name)
        outcomes: dict[str, object] = {}
        green: set[str] = set()
        for key, label, arm in (("banks", "banks", bank_arms), ("checks", "rules", partial(check_arms, tmp=tmp)),
                                ("sim", "simulation", sim_arms), ("link", "link", partial(link_arms, tmp=tmp)),
                                ("soc", "SoC build", partial(soc_arms, tmp=tmp / "soc"))):
            before = len(problems)
            outcomes[key] = run_arm(problems, label, arm)
            if len(problems) == before:
                green.add(key)
        run_arm(problems, "register", partial(registry_arms, tmp=tmp))
        run_arm(problems, "mutants", partial(mutant_arms, tmp=tmp, green=green))
    for problem in problems:
        print(f"FAIL: {problem}", file=sys.stderr)
    print(f"test_ctrl_memory: {len(problems)} failure(s)")
    if not problems and not outcomes["link"]:
        print("RESULT: SKIP (no RV32 compiler; the link arm needs one, see sw/firmware/gtest/fw_rv32.py)")
        return 0
    print(f"RESULT: {'PASS' if not problems else 'FAIL'}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
