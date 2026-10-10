#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""ctrl_image.py - the composed ctrl_app linked for RV32I, and its sizes (#665 acceptance addition 6030870481).

WHAT IT MEASURES. For each shape (a shipped config), the control-plane
firmware as a Mark II platform composes it (rv32_image/image_main.c): the app
(pool, loop, ADP, lane F2's MAAP with its allocation output on the datapath
CSR window, and, since lane F3, ACMP with its binding owner), lane F1's
saved-state store on the LiteSPI port at the shape's generated container, and
the MMIO platform, booted in ctrl/README.md's order. Every source is
compiled freestanding with its own gate's RV32 flags (ctrl_build.RV32_FLAGS,
nvm_rv32.RV32_FLAGS), with -DNDEBUG (the release build, whose re-entry guards
count instead of asserting) and one section per function and object, then
linked by rv32_image/image.ld into one 128 KB block-RAM region at
--gc-sections, so only what the composition reaches is counted. The ACMP
configuration and the entity take the shape's stream counts from its entity
model (ctrl_arms.fabric_view, the `entity` arm's source).

NO LIBRARY. The image links no library: the pinned SDK's libgcc is built for
its one multilib (rv32imafd, the ilp32d ABI) and cannot link into a soft-float
RV32I image. The compiler's arithmetic helpers come from rv32_image/image_arith.c
(every helper the rv32 arm admits; none is a floating-point one), which must
be leaves: an object that leaves a symbol open or calls a helper is refused,
so no helper can reach itself. The linked ELF is then audited before any
figure is read: ELF32 little-endian RISC-V executable, e_flags 0 (no RVC, the
soft-float ILP32 ABI, not RVE or Ztso), the one architecture attribute
rv32i<version>, every word of every executable section an RV32I base
instruction (no M, A, F, D, C, Zicsr or Zifencei), and no symbol that the
objects and libraries it links reference and none defines (a weak one links
to address 0 and leaves no trace in the image, so the inputs are read). Any
finding refuses the measurement.

WHAT IT PRINTS. The compiler's identity (its version line and its libgcc's
sha256, which is not linked); per shape, the image's text, rodata, data and
bss from the ELF's section headers; the audit's result; every static object
of 64 bytes or more from its symbol table (the app, the pool's arena, the
binding owner, the store's stage, payload, chunk and state); the app's parts
(sizeof each, from a probe object that is not linked); and, apart from the
firmware's bytes, the C-runtime stand-ins (rv32_image/image_rt.c), which the
SoC's libbase replaces, and the arithmetic helpers the image reaches, which
LiteX's libcompiler_rt supplies in the SoC image. The map is written beside
the image.

THE BASE. --base REV measures the firmware of another revision of this
repository (git archive of sw/firmware, never a checkout) with this tree's
harness and shapes, and prints the delta. A base whose ctrl_app composes no
ACMP links the same platform without it, with MAAP through
ctrl_app_start_maap() where the base has lane F2's (image_main.c). The ADP,
ACMP and MAAP cores are the TSN stack's (#697): the base's own copies under
sw/firmware/ctrl for a revision from before they moved, else the tsn-c-stack
gitlink the base records, read from the submodule's objects.

Usage:
    python3 sw/firmware/ctrl/test/ctrl_image.py [--shape NAME ...] [--base REV] [--out DIR]

ctrl_image_selftest.py holds the controls: helpers checked against the host's
arithmetic, and incompatible libraries, instructions and headers refused.

Exit 0 = every image linked, passed the audit and was measured; 2 = a build,
link, audit or measure refused.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import re
import struct
import subprocess
import sys
import tarfile
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "sw/firmware/gtest"))
sys.path.insert(0, str(ROOT / "sw/firmware/ctrl_nvm/test"))

import ctrl_arms  # noqa: E402
import fw_rv32  # noqa: E402
import nvm_bench  # noqa: E402
import nvm_rv32  # noqa: E402
from ctrl_build import (INCLUDE_DIRS, PORTABLE, RV32_FLAGS, STACK, STACK_INCLUDE, STACK_PARTS, Refusal,  # noqa: E402
                        legacy_stack, source, stack_pin)

IMAGE = HERE / "rv32_image"
#: The shipping shape (Mark II's 1x1, lane F1's self-test shape) and the
#: largest supported one (the most streams and the largest saved container).
SHAPES = ("endstation_ax7101_1x1_tdm8", "endstation_ax7101_8x8")
#: Every source of the composition, by tree: the ctrl set the platform links
#: and lane F1's store with its LiteSPI port.
CTRL_SOURCES = PORTABLE + ("plat/mbx_plat_mmio.c",)
NVM_SOURCES = ("nvm_klj2.c", "nvm_store.c", "plat/nvm_flash_litespi.c")
IMAGE_FLAGS = ("-DNDEBUG", "-ffunction-sections", "-fdata-sections", "-fno-pic", "-fno-pie")
LINK_FLAGS = ("-march=rv32i", "-mabi=ilp32", "-nostdlib", "-nostartfiles", "-static", "-no-pie",
              "-Wl,--gc-sections")
#: The arithmetic helpers' source, compiled with the composition.
HELPERS = IMAGE / "image_arith.c"
#: Archives linked after the objects, by path: none, so every helper is HELPERS's (the self-test links an
#: incompatible one here, with a HELPERS that defines none).
LIBRARIES: tuple[str, ...] = ()
#: The image's output sections (image.ld), in the order they are reported.
SECTIONS = ("text", "rodata", "data", "bss")
#: The C runtime the stand-ins supply.
RUNTIME = ("memset", "memcpy", "memmove", "memcmp", "vsnprintf")
#: A static object at least this large is reported by name.
OBJECT_MIN = 64
#: The block RAM the firmware has under the 10 % reserve (6030870481).
BUDGET = 128 * 1024
#: The ELF header's fields the audit reads: EM_RISCV, ET_EXEC; SHF_EXECINSTR, SHT_NOBITS.
EM_RISCV, ET_EXEC, SHF_EXECINSTR, SHT_NOBITS = 243, 2, 0x4, 8
#: e_flags' bits; RV32I with the soft-float ILP32 ABI sets none of them.
E_FLAGS = ((0x1, "RVC"), (0x6, "a hardware-float ABI"), (0x8, "RVE"), (0x10, "Ztso"))
#: RV32I's base opcodes (bits 6:0) and the funct3 values (bits 14:12) each defines; a word whose bits 1:0 are
#: not 11 is a compressed instruction and has no entry. rv32i_word() checks OP-IMM's shifts, OP and SYSTEM further.
RV32I_FUNCT3 = {
    0x37: range(8), 0x17: range(8), 0x6F: range(8),  # LUI, AUIPC, JAL
    0x67: (0,),  # JALR
    0x63: (0, 1, 4, 5, 6, 7),  # BEQ, BNE, BLT, BGE, BLTU, BGEU
    0x03: (0, 1, 2, 4, 5),  # LB, LH, LW, LBU, LHU
    0x23: (0, 1, 2),  # SB, SH, SW
    0x13: range(8),  # ADDI, SLTI, SLTIU, XORI, ORI, ANDI, SLLI, SRLI, SRAI
    0x33: range(8),  # ADD, SUB, SLL, SLT, SLTU, XOR, SRL, SRA, OR, AND
    0x0F: (0,),  # FENCE (FENCE.I is Zifencei)
    0x73: (0,),  # ECALL, EBREAK (the CSR forms are Zicsr)
}


@dataclass
class Image:
    """One linked image's figures."""

    shape: str
    sinks: int
    sources: int
    sections: dict[str, int] = field(default_factory=dict)
    objects: dict[str, int] = field(default_factory=dict)
    parts: dict[str, int] = field(default_factory=dict)
    runtime: int = 0
    helpers: dict[str, int] = field(default_factory=dict)
    audited: str = ""


def run(argv: list[str], cwd: Path | None = None) -> str:
    """Run one tool; its standard output, or a Refusal with its error."""
    res = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, check=False)
    if res.returncode != 0:
        raise Refusal(f"{Path(argv[0]).name} failed: {(res.stderr or res.stdout).strip()[:2000]}")
    return res.stdout


def includes(fw: Path, gen: Path, stack: Path) -> list[str]:
    """The ctrl tree's include directories, the stack's public headers, the store's and the shape's generated
    headers."""
    nvm = fw / "ctrl_nvm"
    return ([f"-I{fw / 'ctrl' / d}" for d in INCLUDE_DIRS] + [f"-I{stack / STACK_INCLUDE}"] +
            [f"-I{gen}", f"-I{nvm}", f"-I{nvm / 'plat'}", f"-I{nvm / 'test/rv32'}"])


def object_name(src: Path) -> str:
    """A source's object under the shape's work directory: its directory's name and its stem."""
    return f"{src.parent.name}_{src.stem}.o"


def compile_all(cc: str, fw: Path, gen: Path, work: Path, shape_defs: list[str], stack: Path) -> list[Path]:
    """Every source of the composition, each with its gate's flags; a ctrl or stack source the tree lacks is not
    compiled."""
    runtime_inc = fw_rv32.includes(cc)
    inc = includes(fw, gen, stack)
    ctrl = [source(fw / "ctrl", stack, s) for s in CTRL_SOURCES]
    jobs = [(src, RV32_FLAGS) for src in ctrl if src.is_file()]
    jobs += [(fw / "ctrl_nvm" / s, nvm_rv32.RV32_FLAGS) for s in NVM_SOURCES]
    # the stand-ins' loops must stay loops, never calls to themselves
    jobs += [(IMAGE / "image_main.c", RV32_FLAGS),
             (IMAGE / "image_rt.c", (*RV32_FLAGS, "-fno-tree-loop-distribute-patterns")),
             (HELPERS, RV32_FLAGS),
             (IMAGE / "image_start.S", ("-march=rv32i", "-mabi=ilp32"))]
    objs = []
    for src, flags in jobs:
        obj = work / object_name(src)
        run([cc, *flags, *IMAGE_FLAGS, *runtime_inc, *inc, *shape_defs, "-c", str(src), "-o", str(obj)])
        objs.append(obj)
    return objs


def section_sizes(tool: str, elf: Path) -> dict[str, int]:
    """The image's allocated sections by name; any section but image.ld's four is refused."""
    sizes: dict[str, int] = {}
    for line in run([tool + "readelf", "-S", "-W", str(elf)]).splitlines():
        m = re.match(r"\s*\[\s*\d+\]\s+\.(\S+)\s+\S+\s+[0-9a-f]+\s+[0-9a-f]+\s+([0-9a-f]+)\s+\S+\s+(\S*)", line)
        if m and "A" in m.group(3):
            sizes[m.group(1)] = int(m.group(2), 16)
    stray = sorted(set(sizes) - set(SECTIONS))
    if stray:
        raise Refusal(f"the image has sections image.ld does not name: {', '.join(stray)}")
    return {s: sizes.get(s, 0) for s in SECTIONS}


def symbol_sizes(tool: str, obj: Path) -> dict[str, tuple[str, int]]:
    """Every sized symbol of an object or image: name -> (nm type, bytes)."""
    found = {}
    for line in run([tool + "nm", "-S", "--defined-only", str(obj)]).splitlines():
        parts = line.split()
        if len(parts) == 4:
            found[parts[3]] = (parts[2], int(parts[1], 16))
    return found


def helper_findings(tool: str, obj: Path) -> list[str]:
    """The helpers must be leaves. GCC lowers an operation RV32I lacks into a call to its helper, even inside
    that helper, so a symbol left open or a relocation naming a helper (a call to one) is a finding."""
    found = []
    undefined = names(run([tool + "nm", "-u", str(obj)]), 2)
    if undefined:
        found.append(f"{obj.name} leaves symbols open: {', '.join(sorted(undefined))}")
    calls = set()
    for line in run([tool + "readelf", "-r", "-W", str(obj)]).splitlines():
        m = re.match(r"\s*[0-9a-f]+\s+[0-9a-f]+\s+\S+\s+[0-9a-f]+\s+(\S+)", line)
        if m and m.group(1) in fw_rv32.HELPERS:
            calls.add(m.group(1))
    if calls:
        found.append(f"{obj.name} calls helpers: {', '.join(sorted(calls))}")
    return found


def exec_sections(data: bytes) -> list[tuple[str, int, bytes]]:
    """Each executable section of an ELF32 file that has bytes: (name, address, bytes)."""
    shoff = struct.unpack_from("<I", data, 32)[0]
    shentsize, shnum, shstrndx = struct.unpack_from("<HHH", data, 46)
    headers = [struct.unpack_from("<10I", data, shoff + i * shentsize) for i in range(shnum)]
    names = headers[shstrndx][4]
    found = []
    for name, kind, flags, addr, offset, size, *_ in headers:
        if flags & SHF_EXECINSTR and kind != SHT_NOBITS:
            label = data[names + name:data.index(b"\0", names + name)].decode()
            found.append((label, addr, data[offset:offset + size]))
    return found


def rv32i_word(word: int) -> bool:
    """One 32-bit word is an RV32I base instruction: none of M, A, F, D, C, Zicsr or Zifencei."""
    opcode, funct3, funct7 = word & 0x7F, (word >> 12) & 0x7, word >> 25
    if funct3 not in RV32I_FUNCT3.get(opcode, ()):
        return False
    if opcode == 0x13 and funct3 in (1, 5):  # SLLI, SRLI, SRAI: a 5-bit shift on RV32
        return funct7 == 0 or (funct3 == 5 and funct7 == 0x20)
    if opcode == 0x33:  # funct7 1 is M's
        return funct7 == 0 or (funct7 == 0x20 and funct3 in (0, 5))
    if opcode == 0x73:
        return word in (0x00000073, 0x00100073)
    return True


def header_findings(data: bytes) -> list[str]:
    """A RISC-V executable whose e_flags are 0; the caller has checked it is a little-endian ELF32 file."""
    e_type, machine = struct.unpack_from("<HH", data, 16)
    flags = struct.unpack_from("<I", data, 36)[0]
    found = []
    if machine != EM_RISCV:
        found.append(f"machine {machine}, not RISC-V")
    if e_type != ET_EXEC:
        found.append(f"ELF type {e_type}, not an executable")
    if flags:
        named = [n for bit, n in E_FLAGS if flags & bit] or ["bits RV32I ILP32 does not set"]
        found.append(f"e_flags {flags:#x}, not 0: {', '.join(named)}")
    return found


def names(listing: str, fields: int) -> set[str]:
    """The symbol names of an nm listing whose symbol lines have `fields` fields (an archive's member headers
    have one)."""
    return {parts[-1] for parts in map(str.split, listing.splitlines()) if len(parts) == fields}


def open_symbols(tool: str, elf: Path, inputs: list[str]) -> list[str]:
    """Symbols the link's inputs reference and neither they nor the image (image.ld's) define. A weak one links
    to address 0 and leaves no trace in the image, so the inputs are what is read."""
    undefined: set[str] = set()
    defined = names(run([tool + "nm", "-g", "--defined-only", str(elf)]), 3)
    for path in inputs:
        undefined |= names(run([tool + "nm", "-u", path]), 2)
        defined |= names(run([tool + "nm", "-g", "--defined-only", path]), 3)
    return sorted(undefined - defined)


def audit(tool: str, elf: Path, inputs: list[str]) -> tuple[list[str], str]:
    """The linked image and its inputs against RV32I and ILP32: the findings, and a line saying what was
    checked."""
    data = elf.read_bytes()
    if len(data) < 52 or data[:6] != b"\x7fELF\x01\x01":
        return [f"{elf.name} is not a little-endian ELF32 file"], ""
    found = header_findings(data)
    arches = re.findall(r'Tag_RISCV_arch: "([^"]+)"', run([tool + "readelf", "-A", str(elf)]))
    if len(arches) != 1 or not re.fullmatch(r"rv32i\d+p\d+", arches[0]):
        found.append(f"architecture attribute {arches}, not RV32I alone")
    words = 0
    for name, addr, code in exec_sections(data):
        if len(code) % 4:
            found.append(f"{name}: {len(code)} bytes, not whole 32-bit instructions")
        bad = []
        for i in range(0, len(code) - 3, 4):
            word = int.from_bytes(code[i:i + 4], "little")
            if not rv32i_word(word):
                bad.append((addr + i, word))
        words += len(code) // 4
        if bad:
            found.append(f"{name}: {len(bad)} words outside RV32I, the first {bad[0][1]:#010x} at {bad[0][0]:#x}")
    undefined = open_symbols(tool, elf, inputs)
    if undefined:
        found.append(f"symbols left undefined: {', '.join(undefined)}")
    arch = arches[0] if arches else "none"
    return found, f"RV32I audit: e_flags 0, {arch}, {words:,} words all RV32I base instructions, nothing undefined"


def identity(cc: str) -> str:
    """The compiler's version line and its libgcc's sha256 (not linked): the toolchain the figures name."""
    libgcc = Path(run([cc, "-print-libgcc-file-name"]).strip())
    digest = hashlib.sha256(libgcc.read_bytes()).hexdigest() if libgcc.is_file() else "absent"
    return f"{run([cc, '--version']).splitlines()[0]}; libgcc.a sha256 {digest} (not linked)"


def app_parts(cc: str, fw: Path, gen: Path, work: Path, stack: Path) -> dict[str, int]:
    """sizeof each part of struct ctrl_app, from a probe object that is never linked."""
    probe = work / "app_parts.c"
    probe.write_text('#include "ctrl_app.h"\nstruct ctrl_app size_app;\nstruct ctrl_pool size_pool;\n'
                     "struct ctrl_loop size_loop;\nstruct adp_mbx size_adp;\n#ifdef CTRL_APP_ACMP_FIRST_SLOT\n"
                     "struct acmp_mbx size_acmp;\n#endif\n#ifdef CTRL_MAAP_MBX_H\nstruct maap_mbx size_maap;\n"
                     "#endif\n", encoding="utf-8")
    obj = work / "app_parts.o"
    run([cc, *RV32_FLAGS, "-fno-common", *fw_rv32.includes(cc), *includes(fw, gen, stack), "-c", str(probe), "-o",
         str(obj)])
    return {n.removeprefix("size_"): s for n, (_, s) in symbol_sizes(cc.removesuffix("gcc"), obj).items()}


def shape_build(config: Path, work: Path) -> tuple[Path, list[str]]:
    """What the composition is compiled with at one shape: the store's generated headers (its container and the
    SoC's header), written into work/gen, and the shape's stream counts from its entity model, the -D flags
    image_main.c reads. The boundary gate (ctrl_boundary.py) judges the image under the same."""
    view = ctrl_arms.fabric_view(config)
    try:
        inputs = nvm_bench.shape_inputs(config, work / "shape")
    except nvm_bench.Refusal as exc:
        raise Refusal(str(exc)) from exc
    gen = work / "gen"
    nvm_bench.write_headers(gen, nvm_bench.shape_header(inputs.shape, inputs.donor, inputs.ident), inputs.clock_hz)
    return gen, [f"-DIMAGE_SINKS={view['listener_stream_sinks']}u", f"-DIMAGE_SOURCES={view['talker_stream_sources']}u"]


def measure(cc: str, fw: Path, shape: str, work: Path, stack: Path = STACK) -> Image:
    """Link the composition at one shape and read its figures."""
    config = ROOT / "configs" / f"{shape}.yaml"
    view = ctrl_arms.fabric_view(config)
    image = Image(shape, view["listener_stream_sinks"], view["talker_stream_sources"])
    work.mkdir(parents=True, exist_ok=True)
    gen, defs = shape_build(config, work)
    objs = compile_all(cc, fw, gen, work, defs, stack)
    tool = cc.removesuffix("gcc")
    helpers = work / object_name(HELPERS)
    findings = helper_findings(tool, helpers)
    if findings:
        raise Refusal("; ".join(findings))
    elf = work / "ctrl_app.elf"
    inputs = [*map(str, objs), *LIBRARIES]
    run([cc, *LINK_FLAGS, f"-Wl,-Map={work / 'ctrl_app.map'}", "-T", str(IMAGE / "image.ld"), *inputs, "-o",
         str(elf)])
    findings, image.audited = audit(tool, elf, inputs)
    if findings:
        raise Refusal(f"the image at {shape} is not RV32I ILP32: {'; '.join(findings)}")
    image.sections = section_sizes(tool, elf)
    symbols = symbol_sizes(tool, elf)
    image.objects = {n: s for n, (t, s) in symbols.items() if t in "bBdD" and s >= OBJECT_MIN}
    image.runtime = sum(symbols[n][1] for n in RUNTIME if n in symbols)
    image.helpers = {n: symbols[n][1] for n in symbol_sizes(tool, helpers) if n in symbols}
    image.parts = app_parts(cc, fw, gen, work, stack)
    return image


def report(head: Image, base: Image | None) -> list[str]:
    """One shape's table: each section at the head, at the base and the delta; then its static objects."""
    load = sum(head.sections[s] for s in ("text", "rodata", "data"))
    lines = [f"shape {head.shape}: {head.sinks} STREAM_INPUTs, {head.sources} STREAM_OUTPUTs",
             f"  {'section':<10}{'head':>10}" + (f"{'base':>10}{'delta':>10}" if base else "")]
    for s in SECTIONS:
        row = f"  {s:<10}{head.sections[s]:>10,}"
        if base:
            row += f"{base.sections[s]:>10,}{head.sections[s] - base.sections[s]:>+10,}"
        lines.append(row)
    total = load + head.sections["bss"]
    row = f"  {'total':<10}{total:>10,}"
    if base:
        btotal = sum(base.sections.values())
        row += f"{btotal:>10,}{total - btotal:>+10,}"
    lines += [row, f"  load image (text + rodata + data) {load:,}; with bss {total:,} of the {BUDGET:,}-byte budget "
                   f"({100.0 * total / BUDGET:.1f} %), the stack not counted",
              f"  {head.audited}",
              f"  C-runtime stand-ins in text: {head.runtime:,} bytes (libbase's in the SoC image)",
              f"  arithmetic helpers in text: {sum(head.helpers.values()):,} bytes "
              f"({', '.join(sorted(head.helpers))}; libcompiler_rt's in the SoC image)",
              "  static objects of 64 bytes or more:"]
    lines += [f"    {n:<24}{s:>8,}" for n, s in sorted(head.objects.items(), key=lambda kv: -kv[1])]
    lines.append("  struct ctrl_app, by part (sizeof): " +
                 ", ".join(f"{n} {s:,}" for n, s in sorted(head.parts.items(), key=lambda kv: -kv[1])))
    return lines


def extract(repo: Path, rev: str, paths: tuple[str, ...], into: Path) -> None:
    """`paths` of revision `rev` of the repository at `repo`, read from its objects into `into`."""
    res = subprocess.run(["git", "-C", str(repo), "archive", rev, *paths], capture_output=True, check=False)
    if res.returncode != 0:
        raise Refusal(f"git archive {rev} in {repo.name}: {res.stderr.decode(errors='replace').strip()}")
    with tarfile.open(fileobj=io.BytesIO(res.stdout)) as tar:
        tar.extractall(into, filter="data")


def base_tree(rev: str, into: Path) -> tuple[Path, Path]:
    """sw/firmware of revision `rev`, read from the repository's objects into `into`, and the stack it builds
    against: the base's own cores in the stack's layout for a revision from before #697, else the stack at the
    tsn-c-stack gitlink the revision records, read from the submodule's objects."""
    extract(ROOT, rev, ("sw/firmware",), into)
    fw = into / "sw/firmware"
    legacy = legacy_stack(fw / "ctrl", into / "legacy-stack")
    if legacy is not None:
        return fw, legacy
    entry = run(["git", "-C", str(ROOT), "ls-tree", rev, "--", STACK.relative_to(ROOT).as_posix()]).split()
    if len(entry) != 4 or entry[0] != "160000":
        raise Refusal(f"{rev} holds neither the cores nor a tsn-c-stack gitlink")
    top = run(["git", "-C", str(STACK), "rev-parse", "--show-toplevel"]).strip()
    if Path(top).resolve() != STACK.resolve():
        raise Refusal(f"{STACK.relative_to(ROOT)} is not its own checkout: initialise the submodule")
    extract(STACK, entry[2], STACK_PARTS, into / "tsn-c-stack")
    return fw, into / "tsn-c-stack"


def main(argv: list[str] | None = None) -> int:
    """Measure each shape at the head, and at the base when given."""
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("--shape", action="append", help="a config under configs/ (default: the shipping and the largest)")
    ap.add_argument("--base", help="a revision whose firmware is measured with the same harness, for the delta")
    ap.add_argument("--out", type=Path, help="keep the images and maps here (default: a temporary directory)")
    args = ap.parse_args(argv)
    cc = fw_rv32.compiler()
    if cc is None:
        print("REFUSED: no RV32 compiler (the pinned SDK's riscv32-linux-gcc or MILAN_RV32_CC)")
        return 2
    print(f"compiler: {cc}, {identity(cc)}")
    with tempfile.TemporaryDirectory(prefix="ctrl-image-") as tmp:
        out = args.out.resolve() if args.out else Path(tmp)
        try:
            print(f"tsn-c-stack at {stack_pin()}")
            base_fw, base_stack = base_tree(args.base, out / "base-tree") if args.base else (None, None)
            for shape in args.shape or SHAPES:
                head = measure(cc, ROOT / "sw/firmware", shape, out / "head" / shape, STACK)
                base = measure(cc, base_fw, shape, out / "base" / shape, base_stack) if base_fw else None
                print("\n".join(report(head, base)))
        except (Refusal, ValueError) as exc:
            print(f"REFUSED: {exc}")
            return 2
    if args.base:
        print(f"base: {args.base}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
