#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The split placement's firmware memory (#640 M8a): plan, checks, banks and link.

`ctrl_memory.py` is the map and its checks; `milan_soc.CtrlMemory` is the
block RAM the SoC builds from them. This file grades five things:

  1. BANKS. For every need up to past the budget, the banks are powers of two
     of whole RAMB18 granules, largest first, and hold the need with less than
     one granule spare. The oracle is ceil(need / 2,048) and its binary digits.
  2. CHECKS. ELFs written here, by a writer independent of `read_elf`, are
     planned or refused: a good image is accepted and its rom contents are the
     bytes placed at their load addresses. The three planted controls the
     assignment names fail by name: an allocation over budget
     (`allocation over budget`), a memory-map overlap (`memory-map overlap`,
     both two sections and two regions) and a staging buffer of the wrong
     shape (`staging buffer`). So do an image entering elsewhere than the
     reset address (`reset entry`), initial bytes outside rom and a section
     outside both regions (`memory map`).
  3. BANKS IN SIMULATION. The real `milan_soc.CtrlMemory`, in migen: rom
     reads its image at the first and last word of every bank and refuses a
     write; sram writes byte lanes and reads them back at every bank boundary;
     an address past the last bank answers err in either region and writes no
     bank.
  4. PLANTED DEFECTS. Each of these must turn at least one arm red: banks
     smallest first, the hole answering nothing, a writable rom, the map
     check, the budget check and the staging check each switched off.
  5. THE LINK. With an RV32 compiler (sw/firmware/gtest/fw_rv32.py), a probe
     linked by `sw/firmware/ctrl/plat/ctrl_split.ld` behind
     `ctrl_split_start.S` enters at the reset address with the reset entry
     first, loads .data's initial value from rom and is planned. The same
     script with `.data`'s `AT > rom` removed, or entering at `main`, is
     refused by name. Without a compiler this arm is a declared skip.
"""
from __future__ import annotations

import contextlib
import struct
import subprocess
import sys
import tempfile
from collections.abc import Callable, Generator, Iterator
from functools import partial
from pathlib import Path
from typing import Any

from migen import ClockDomain, Module, run_simulation

from litex.soc.interconnect import wishbone

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "sw/firmware/gtest"))
import ctrl_memory  # noqa: E402
import fw_rv32  # noqa: E402
import milan_soc  # noqa: E402

PLAT = ROOT / "sw/firmware/ctrl/plat"
GRANULE = 2048

#: What a migen stimulus process is: it yields reads and writes and is sent
#: back whatever a read resolved to.
Stim = Generator[Any, Any, Any]


def check(problems: list[str], ok: bool, what: str) -> None:
    """Record one graded fact."""
    print(f"  [{'ok  ' if ok else 'FAIL'}] {what}")
    if not ok:
        problems.append(what)


def refused(problems: list[str], name: str, attempt: Callable[[], object], what: str) -> None:
    """`attempt` must raise ctrl_memory.Refusal for the check called `name`."""
    try:
        attempt()
    except ctrl_memory.Refusal as exc:
        check(problems, exc.check == name, f"{what}: refused by '{exc.check}' ({exc})")
        return
    check(problems, False, f"{what}: accepted, expected a '{name}' refusal")


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


# ---- 2. checks, on ELFs written here -----------------------------------------------------------

def write_elf(entry: int, sections: list[tuple[str, int, int, bytes | int]],
              symbols: dict[str, int]) -> bytes:
    """A little-endian RV32 executable, one PT_LOAD per section.

    A section is (name, address, load address, initial bytes or a NOBITS
    size); a symbol is a name and the size of the object it names.
    """
    shstr = b"\0" + b"".join(n.encode() + b"\0" for n, *_ in sections) + b".symtab\0.strtab\0.shstrtab\0"
    strtab = b"\0" + b"".join(n.encode() + b"\0" for n in symbols)
    body, placed = b"", []
    base = 52 + 32 * len(sections)
    for _, vma, lma, data in sections:
        payload = data if isinstance(data, bytes) else b""
        placed.append(base + len(body))
        body += payload + b"\0" * (-len(payload) % 4)
    symtab = bytes(16)
    for n, (name, size) in enumerate(symbols.items()):
        symtab += struct.pack("<IIIBBH", strtab.index(name.encode() + b"\0"), 0x1000_0000, size, 0x11, 0, 1)
    tables = {"symtab": base + len(body)}
    body += symtab
    tables["strtab"] = base + len(body)
    body += strtab
    tables["shstrtab"] = base + len(body)
    body += shstr + b"\0" * (-len(shstr) % 4)
    shoff = base + len(body)
    head = struct.pack("<16sHHIIIIIHHHHHH", b"\x7fELF\x01\x01\x01" + bytes(9), 2, 243, 1, entry, 52, shoff,
                       0, 52, 32, len(sections), 40, len(sections) + 4, len(sections) + 3)
    programs = b""
    shdrs = bytes(40)
    for (name, vma, lma, data), offset in zip(sections, placed):
        loaded = isinstance(data, bytes)
        size = len(data) if loaded else data
        programs += struct.pack("<8I", 1, offset, vma, lma, size if loaded else 0, size, 6, 4)
        shdrs += struct.pack("<10I", shstr.index(name.encode() + b"\0"), 1 if loaded else 8,
                             0x2 | (0x4 if vma == lma else 0x1), vma, offset, size, 0, 0, 4, 0)
    n = len(sections)
    shdrs += struct.pack("<10I", shstr.index(b".symtab\0"), 2, 0, 0, tables["symtab"], len(symtab), n + 2, 1, 4, 16)
    shdrs += struct.pack("<10I", shstr.index(b".strtab\0"), 3, 0, 0, tables["strtab"], len(strtab), 0, 0, 1, 0)
    shdrs += struct.pack("<10I", shstr.index(b".shstrtab\0"), 3, 0, 0, tables["shstrtab"], len(shstr), 0, 0, 1, 0)
    return head + programs + body + shdrs


def image(tmp: Path, entry: int = 0, bss: int = 40_000, data_lma: int | None = None,
          bss_at: int | None = None, stage: int = 3344) -> ctrl_memory.Image:
    """The shape of a split image: code and constants in rom, .data loaded from rom, .bss, the stack."""
    text = bytes((i * 7 + 3) & 0xFF for i in range(9_000))
    rodata = bytes((i * 13 + 5) & 0xFF for i in range(3_002))
    data = bytes(range(64))
    ram = ctrl_memory.RAM.origin
    lma = 9_000 + 3_004 if data_lma is None else data_lma
    bss_vma = ram + 64 if bss_at is None else bss_at
    path = tmp / f"probe-{entry}-{bss}-{lma}-{bss_vma}-{stage}.elf"
    path.write_bytes(write_elf(entry, [(".text", 0, 0, text), (".rodata", 9_000, 9_000, rodata),
                                       (".data", ram, lma, data), (".bss", bss_vma, bss_vma, bss),
                                       (".stack", ram + 64 + bss, ram + 64 + bss, 8192)],
                               {"_start": 4, ctrl_memory.STAGE_SYMBOL: stage}))
    return ctrl_memory.read_elf(path)


def check_arms(problems: list[str], tmp: Path) -> None:
    """The good image, then every refusal by its name."""
    good = image(tmp)
    plan = ctrl_memory.plan(good)
    check(problems, (plan.rom_bytes, plan.ram_bytes) == (9_000 + 3_004 + 64, 64 + 40_000 + 8192),
          f"the plan's needs are rom to the end of .data's initial bytes, sram to the stack's top "
          f"({plan.rom_bytes}, {plan.ram_bytes})")
    words = ctrl_memory.rom_words(good)
    raw = struct.pack(f"<{len(words)}I", *words)
    check(problems, raw[:4] == bytes((3, 10, 17, 24)) and raw[9_000:9_002] == bytes((5, 18))
          and raw[12_004:12_068] == bytes(range(64)),
          "rom holds .text at the reset address, .rodata after it and .data's initial bytes at their load address")
    ctrl_memory.check_stage(good, 3344, "1x1")
    check(problems, True, "a staging buffer of the shape's size is accepted")
    refused(problems, "allocation over budget", lambda: ctrl_memory.plan(image(tmp, bss=215_000)),
            "PLANTED: an allocation over budget (215,000 bytes of .bss: 58 RAMB36, each region inside its own)")
    refused(problems, "memory-map overlap", lambda: ctrl_memory.plan(image(tmp, bss_at=ctrl_memory.RAM.origin + 32)),
            "PLANTED: a memory-map overlap (.bss over .data)")
    refused(problems, "memory-map overlap",
            lambda: ctrl_memory.plan(good, ram=ctrl_memory.Region("sram", 0x2_0000, ctrl_memory.BUDGET_BYTES)),
            "PLANTED: a memory-map overlap (sram moved into rom)")
    refused(problems, "staging buffer", lambda: ctrl_memory.check_stage(good, 13264, "8x8"),
            "PLANTED: a staging buffer sized for another shape (1x1 image, 8x8 stage)")
    refused(problems, "staging buffer", lambda: ctrl_memory.check_stage(image(tmp, stage=13264), 3344, "1x1"),
            "PLANTED: a staging buffer sized for another shape (8x8 image, 1x1 stage)")
    refused(problems, "reset entry", lambda: ctrl_memory.plan(image(tmp, entry=0x100)),
            "an image entering away from the reset address")
    refused(problems, "memory map", lambda: ctrl_memory.plan(image(tmp, data_lma=ctrl_memory.RAM.origin)),
            "initial bytes of .data left in sram, which nothing initialises")
    refused(problems, "memory map", lambda: ctrl_memory.plan(image(tmp, bss_at=0x4000_0000)),
            "a section outside rom and sram")
    text = ctrl_memory.regions_ld()
    check(problems, "rom (rx) : ORIGIN = 0x00000000, LENGTH = 0x00038000" in text
          and "sram (rwx) : ORIGIN = 0x10000000, LENGTH = 0x00038000" in text,
          "regions.ld states both regions at the CPU's origins, each the whole 224 KiB budget")


# ---- 3. banks in simulation --------------------------------------------------------------------

def access(bus: wishbone.Interface, adr: int, we: int = 0, dat: int = 0, sel: int = 0xF) -> Stim:
    """One Wishbone cycle; ('ack' | 'err' | 'none', dat_r) within eight clocks."""
    yield bus.adr.eq(adr)
    yield bus.we.eq(we)
    yield bus.dat_w.eq(dat)
    yield bus.sel.eq(sel)
    yield bus.cyc.eq(1)
    yield bus.stb.eq(1)
    answer = ("none", None)
    for _ in range(8):
        yield
        ack, err = (yield bus.ack), (yield bus.err)
        if ack or err:
            answer = ("ack" if ack else "err", (yield bus.dat_r))
            break
    yield bus.cyc.eq(0)
    yield bus.stb.eq(0)
    yield
    return answer


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


def sim_arms(problems: list[str], need: int = 7 * GRANULE - 100) -> None:
    """Every bank's edges in both regions, the hole and the refused rom write."""
    bench = Bench(need)
    edges, offsets, first = [], [], 0
    for size in bench.banks:
        edges += [first, first + 1, first + size // 4 - 1]
        offsets.append(first)
        first += size // 4
    image_words = need // 4
    seen: dict[str, Any] = {}

    def reads(bus: wishbone.Interface, addresses: list[int]) -> Stim:
        """One read of each address, in order."""
        out = []
        for a in addresses:
            out.append((yield from access(bus, a)))
        return out

    def run() -> Stim:
        ram_base = ctrl_memory.RAM.origin // 4
        seen["rom"] = yield from reads(bench.rom.bus, [a for a in edges if a < image_words])
        seen["rom_write"] = yield from access(bench.rom.bus, edges[1], we=1, dat=0xDEAD_BEEF)
        seen["rom_after"] = yield from access(bench.rom.bus, edges[1])
        seen["rom_hole"] = yield from access(bench.rom.bus, bench.words)
        for n, a in enumerate(edges):
            yield from access(bench.ram.bus, ram_base + a, we=1, dat=pattern(a) ^ 0xFFFF_0000, sel=0xF)
            yield from access(bench.ram.bus, ram_base + a, we=1, dat=0xA5 << (8 * (n % 4)), sel=1 << (n % 4))
        seen["ram"] = yield from reads(bench.ram.bus, [ram_base + a for a in edges])
        seen["ram_hole"] = yield from access(bench.ram.bus, ram_base + bench.words, we=1, dat=0x5555_5555)
        # the cell of each bank the hole's address would reach if the bank decoded it
        seen["ram_alias"] = yield from reads(bench.ram.bus, [ram_base + f + bench.words % (s // 4)
                                                             for f, s in zip(offsets, bench.banks)])

    run_simulation(bench, run())
    rom_want = [("ack", pattern(a)) for a in edges if a < image_words]
    check(problems, seen["rom"] == rom_want,
          f"rom reads its image at the first, second and last word of each of {len(bench.banks)} banks")
    check(problems, seen["rom_write"][0] == "ack" and seen["rom_after"] == ("ack", pattern(edges[1])),
          "a write to rom changes nothing")
    check(problems, seen["rom_hole"][0] == "err", "rom past its last bank answers err at once")
    ram_want = []
    for n, a in enumerate(edges):
        word = pattern(a) ^ 0xFFFF_0000
        lane = 8 * (n % 4)
        ram_want.append(("ack", (word & ~(0xFF << lane)) | (0xA5 << lane)))
    check(problems, seen["ram"] == ram_want,
          "sram keeps each byte lane written at every bank's edges, the other lanes intact")
    check(problems, seen["ram_hole"][0] == "err", "sram past its last bank answers err at once")
    check(problems, all(r[0] == "ack" and r[1] != 0x5555_5555 for r in seen["ram_alias"]),
          "a write past the last bank lands in no bank")


# ---- 4. planted defects ------------------------------------------------------------------------

@contextlib.contextmanager
def patched(owner: object, name: str, value: object) -> Iterator[None]:
    """Replace `owner.name` for the duration of one planted defect."""
    original = getattr(owner, name)
    setattr(owner, name, value)
    try:
        yield
    finally:
        setattr(owner, name, original)


def no_hole(master: object, slaves: list, register: bool = False) -> wishbone.Decoder:
    """The decoder without its last slave, the hole."""
    return DECODER(master, slaves[:-1], register)


def writable(size: int, read_only: bool | None = None, **kw: object) -> wishbone.SRAM:
    """Every bank built writable."""
    return SRAM(size, read_only=False, **kw)


DECODER, SRAM = wishbone.Decoder, wishbone.SRAM
MUTANTS = (
    ("banks smallest first", ctrl_memory, "banks",
     lambda need, f=ctrl_memory.banks: tuple(reversed(f(need))), sim_arms),
    ("the hole answers nothing", wishbone, "Decoder", no_hole, sim_arms),
    ("a writable rom", wishbone, "SRAM", writable, sim_arms),
    ("the map check off", ctrl_memory, "check_map", lambda *a, **k: None, None),
    ("the budget check off", ctrl_memory, "plan", partial(ctrl_memory.plan, budget=10**6), None),
    ("the staging check off", ctrl_memory, "check_stage", lambda *a, **k: None, None),
)


def mutant_arms(problems: list[str], tmp: Path) -> None:
    """Each planted defect must turn an arm red."""
    for name, owner, attribute, value, arm in MUTANTS:
        caught: list[str] = []
        with patched(owner, attribute, value), contextlib.redirect_stdout(None):
            try:
                (arm or partial(check_arms, tmp=tmp))(caught)
            except Exception as exc:     # a defect that breaks the arm outright is caught too
                caught.append(f"{type(exc).__name__}: {exc}")
        check(problems, bool(caught), f"PLANTED DEFECT '{name}' is caught ({len(caught)} red)")


# ---- 5. the link ---------------------------------------------------------------------------

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
    elf = tmp / "probe.elf"
    subprocess.run([cc, *flags, "-nostdlib", "-static", "-no-pie", "-Wl,--gc-sections,--build-id=none",
                    "-T", str(tmp / "split.ld"), f"-L{tmp}", str(tmp / "start.o"), str(tmp / "probe.o"),
                    "-o", str(elf)], check=True)
    return elf


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
    check(problems, data.vma == ctrl_memory.RAM.origin and data.lma < plan.rom_bytes
          and words[data.lma // 4] == 7, ".data runs in sram and its initial value 7 loads from rom")
    check(problems, sections[".stack"].vma + sections[".stack"].size == ctrl_memory.RAM.origin + plan.ram_bytes,
          "the stack tops the sram need")
    ctrl_memory.check_stage(probe, 3344, "1x1")
    check(problems, True, "the probe's nvm_stage passes as the shape's stage")
    for plant, edit, name in (("no AT > rom on .data", ("} > sram AT > rom", "} > sram"), "memory map"),
                              ("ENTRY(main)", ("ENTRY(_start)", "ENTRY(main)"), "reset entry")):
        broken = tmp / plant.replace(" ", "-")
        broken.mkdir()
        refused(problems, name, lambda b=broken, e=edit: ctrl_memory.plan(
            ctrl_memory.read_elf(link(cc, b, script.replace(*e)))), f"PLANTED link script: {plant}")
    return True


def main() -> int:
    """Every arm; exit 1 naming each failure."""
    problems: list[str] = []
    print("test_ctrl_memory: the split placement's firmware memory (#640 M8a)")
    with tempfile.TemporaryDirectory(prefix="ctrl-memory-") as tmp:
        bank_arms(problems)
        check_arms(problems, Path(tmp))
        sim_arms(problems)
        mutant_arms(problems, Path(tmp))
        linked = link_arms(problems, Path(tmp))
    for problem in problems:
        print(f"FAIL: {problem}", file=sys.stderr)
    print(f"test_ctrl_memory: {len(problems)} failure(s)")
    if not problems and not linked:
        print("RESULT: SKIP (no RV32 compiler; the link arm needs one, see sw/firmware/gtest/fw_rv32.py)")
        return 0
    print(f"RESULT: {'PASS' if not problems else 'FAIL'}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
