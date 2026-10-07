#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""ctrl_image.py - the composed ctrl_app linked for RV32I, and its sizes (#665 acceptance addition 6030870481).

WHAT IT MEASURES. For each shape (a shipped config), the control-plane
firmware as a Mark II platform composes it (rv32_image/image_main.c): the app
(pool, loop, ADP and, since lane F3, ACMP with its binding owner), lane F1's
saved-state store on the LiteSPI port at the shape's generated container, and
the MMIO platform, booted in ctrl/README.md's order. Every source is
compiled freestanding with its own gate's RV32 flags (ctrl_build.RV32_FLAGS,
nvm_rv32.RV32_FLAGS), with -DNDEBUG (the release build, whose re-entry guards
count instead of asserting) and one section per function and object, then
linked by rv32_image/image.ld into one 128 KB block-RAM region at
--gc-sections, so only what the composition reaches is counted. The ACMP
configuration and the entity take the shape's stream counts from its entity
model (ctrl_arms.fabric_view, the `entity` arm's source).

WHAT IT PRINTS. The image's text, rodata, data and bss from the ELF's section
headers; every static object of 64 bytes or more from its symbol table (the
app, the pool's arena, the binding owner, the store's stage, payload, chunk
and state); the app's parts (sizeof each, from a probe object that is not
linked); and the C-runtime stand-ins (rv32_image/image_rt.c), which the SoC's
libbase replaces, apart from the firmware's bytes. The map is written beside
the image.

THE BASE. --base REV measures the firmware of another revision of this
repository (git archive of sw/firmware, never a checkout) with this tree's
harness and shapes, and prints the delta. A base whose ctrl_app composes no
ACMP links the same platform without it (image_main.c).

Usage:
    python3 sw/firmware/ctrl/test/ctrl_image.py [--shape NAME ...] [--base REV] [--out DIR]

Exit 0 = every image linked and measured; 2 = a build, link or measure refused.
"""

from __future__ import annotations

import argparse
import io
import re
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
from ctrl_build import INCLUDE_DIRS, PORTABLE, RV32_FLAGS, Refusal  # noqa: E402

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
#: The image's output sections (image.ld), in the order they are reported.
SECTIONS = ("text", "rodata", "data", "bss")
#: The C runtime the stand-ins supply.
RUNTIME = ("memset", "memcpy", "memmove", "memcmp", "vsnprintf")
#: A static object at least this large is reported by name.
OBJECT_MIN = 64
#: The block RAM the firmware has under the 10 % reserve (6030870481).
BUDGET = 128 * 1024


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


def run(argv: list[str], cwd: Path | None = None) -> str:
    """Run one tool; its standard output, or a Refusal with its error."""
    res = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, check=False)
    if res.returncode != 0:
        raise Refusal(f"{Path(argv[0]).name} failed: {(res.stderr or res.stdout).strip()[:2000]}")
    return res.stdout


def includes(fw: Path, gen: Path) -> list[str]:
    """The ctrl tree's include directories, the store's and the shape's generated headers."""
    nvm = fw / "ctrl_nvm"
    return ([f"-I{fw / 'ctrl' / d}" for d in INCLUDE_DIRS] +
            [f"-I{gen}", f"-I{nvm}", f"-I{nvm / 'plat'}", f"-I{nvm / 'test/rv32'}"])


def compile_all(cc: str, fw: Path, gen: Path, work: Path, shape_defs: list[str]) -> list[Path]:
    """Every source of the composition, each with its gate's flags; a ctrl source the tree lacks is not compiled."""
    runtime_inc = fw_rv32.includes(cc)
    inc = includes(fw, gen)
    jobs = [(fw / "ctrl" / s, RV32_FLAGS) for s in CTRL_SOURCES if (fw / "ctrl" / s).is_file()]
    jobs += [(fw / "ctrl_nvm" / s, nvm_rv32.RV32_FLAGS) for s in NVM_SOURCES]
    # the stand-ins' loops must stay loops, never calls to themselves
    jobs += [(IMAGE / "image_main.c", RV32_FLAGS),
             (IMAGE / "image_rt.c", (*RV32_FLAGS, "-fno-tree-loop-distribute-patterns")),
             (IMAGE / "image_start.S", ("-march=rv32i", "-mabi=ilp32"))]
    objs = []
    for src, flags in jobs:
        obj = work / f"{src.parent.name}_{src.stem}.o"
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


def app_parts(cc: str, fw: Path, gen: Path, work: Path) -> dict[str, int]:
    """sizeof each part of struct ctrl_app, from a probe object that is never linked."""
    probe = work / "app_parts.c"
    probe.write_text('#include "ctrl_app.h"\nstruct ctrl_app size_app;\nstruct ctrl_pool size_pool;\n'
                     "struct ctrl_loop size_loop;\nstruct adp_mbx size_adp;\n#ifdef CTRL_APP_ACMP_FIRST_SLOT\n"
                     "struct acmp_mbx size_acmp;\n#endif\n", encoding="utf-8")
    obj = work / "app_parts.o"
    run([cc, *RV32_FLAGS, "-fno-common", *fw_rv32.includes(cc), *includes(fw, gen), "-c", str(probe), "-o",
         str(obj)])
    return {n.removeprefix("size_"): s for n, (_, s) in symbol_sizes(cc.removesuffix("gcc"), obj).items()}


def measure(cc: str, fw: Path, shape: str, work: Path) -> Image:
    """Link the composition at one shape and read its figures."""
    config = ROOT / "configs" / f"{shape}.yaml"
    view = ctrl_arms.fabric_view(config)
    image = Image(shape, view["listener_stream_sinks"], view["talker_stream_sources"])
    work.mkdir(parents=True, exist_ok=True)
    try:
        inputs = nvm_bench.shape_inputs(config, work / "shape")
    except nvm_bench.Refusal as exc:
        raise Refusal(str(exc)) from exc
    gen = work / "gen"
    nvm_bench.write_headers(gen, nvm_bench.shape_header(inputs.shape, inputs.donor, inputs.ident), inputs.clock_hz)
    defs = [f"-DIMAGE_SINKS={image.sinks}u", f"-DIMAGE_SOURCES={image.sources}u"]
    objs = compile_all(cc, fw, gen, work, defs)
    elf = work / "ctrl_app.elf"
    run([cc, *LINK_FLAGS, f"-Wl,-Map={work / 'ctrl_app.map'}", "-T", str(IMAGE / "image.ld"), *map(str, objs),
         "-lgcc", "-o", str(elf)])
    tool = cc.removesuffix("gcc")
    image.sections = section_sizes(tool, elf)
    symbols = symbol_sizes(tool, elf)
    image.objects = {n: s for n, (t, s) in symbols.items() if t in "bBdD" and s >= OBJECT_MIN}
    image.runtime = sum(symbols[n][1] for n in RUNTIME if n in symbols)
    image.parts = app_parts(cc, fw, gen, work)
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
              f"  C-runtime stand-ins in text: {head.runtime:,} bytes (libbase's in the SoC image)",
              "  static objects of 64 bytes or more:"]
    lines += [f"    {n:<24}{s:>8,}" for n, s in sorted(head.objects.items(), key=lambda kv: -kv[1])]
    lines.append("  struct ctrl_app, by part (sizeof): " +
                 ", ".join(f"{n} {s:,}" for n, s in sorted(head.parts.items(), key=lambda kv: -kv[1])))
    return lines


def base_tree(rev: str, into: Path) -> Path:
    """sw/firmware of revision `rev`, read from the repository's objects into `into`."""
    res = subprocess.run(["git", "-C", str(ROOT), "archive", rev, "sw/firmware"], capture_output=True, check=False)
    if res.returncode != 0:
        raise Refusal(f"git archive {rev}: {res.stderr.decode(errors='replace').strip()}")
    with tarfile.open(fileobj=io.BytesIO(res.stdout)) as tar:
        tar.extractall(into, filter="data")
    return into / "sw/firmware"


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
    print(f"compiler: {cc}, {run([cc, '--version']).splitlines()[0]}")
    with tempfile.TemporaryDirectory(prefix="ctrl-image-") as tmp:
        out = args.out.resolve() if args.out else Path(tmp)
        try:
            base_fw = base_tree(args.base, out / "base-tree") if args.base else None
            for shape in args.shape or SHAPES:
                head = measure(cc, ROOT / "sw/firmware", shape, out / "head" / shape)
                base = measure(cc, base_fw, shape, out / "base" / shape) if base_fw else None
                print("\n".join(report(head, base)))
        except (Refusal, ValueError) as exc:
            print(f"REFUSED: {exc}")
            return 2
    if args.base:
        print(f"base: {args.base}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
