#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Map the split placement's firmware memory out of context (#640 M8a).

For each linked control-firmware image, this emits the two regions exactly as
the SoC builds them (`milan_soc.CtrlMemory` over `ctrl_memory.plan`). Each
region becomes its own top with the Wishbone port the SoC bus drives. It also
writes a Vivado script that synthesises every top out of context at the
shipping part and directive and records its block RAM, LUT and flip-flop
counts. A missing ROM image is an error, never an empty memory.

    python3 syn/ooc/ctrl_memory_ooc.py <directory> TAG=ELF [TAG=ELF ...]
    cd <directory> && vivado -mode batch -nojournal -source ctrl_memory_ooc.tcl

Run it with the LiteX interpreter; the Vivado step writes ctrl_memory_ooc.tsv.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "sw/litex"))

import ctrl_memory  # noqa: E402
import milan_soc  # noqa: E402
from litex.gen import LiteXModule  # noqa: E402
from litex.gen.fhdl.verilog import convert  # noqa: E402
from migen import ClockDomain  # noqa: E402

#: The AX7101's part and the shipping synthesis directive (sw/litex/build.sh).
PART = "xc7a100t-fgg484-2"
DIRECTIVE = "AreaOptimized_high"
TSV = "ctrl_memory_ooc.tsv"
COLUMNS = ("top", "RAMB36E1", "RAMB18E1", "LUT", "FF", "LUTRAM")


class Top(LiteXModule):
    """One region of the split placement's firmware memory and its clock."""

    def __init__(self, region: ctrl_memory.Region, banks: tuple[int, ...],
                 words: list[int] | None) -> None:
        """The region as add_ctrl_memory builds it."""
        self.cd_sys = ClockDomain("sys")
        self.memory = milan_soc.CtrlMemory(region, banks, words)


def emit(directory: Path, name: str, top: Top) -> None:
    """Write `name`.v and its memory images into `directory`."""
    bus = top.memory.bus
    ios = {top.cd_sys.clk, top.cd_sys.rst, bus.adr, bus.dat_w, bus.dat_r, bus.sel, bus.cyc,
           bus.stb, bus.ack, bus.we, bus.err, bus.cti, bus.bte}
    output = convert(top, ios=ios, name=name)
    (directory / f"{name}.v").write_text(output.main_source)
    for filename, content in output.data_files.items():
        (directory / filename).write_text(content)


def tcl(tops: list[str]) -> str:
    """Synthesise each top alone and append its primitive counts to the TSV."""
    lines = ["set_msg_config -id {Synth 8-4445} -new_severity ERROR",
             f"set out [open {TSV} w]", f'puts $out "{chr(9).join(COLUMNS)}"']
    for top in tops:
        lines += [
            f"read_verilog {top}.v",
            f"synth_design -top {top} -part {PART} -mode out_of_context -directive {DIRECTIVE}",
            "set n {}",
            "foreach f {{REF_NAME == RAMB36E1} {REF_NAME == RAMB18E1} {PRIMITIVE_GROUP == LUT} "
            "{PRIMITIVE_GROUP == FLOP_LATCH} {PRIMITIVE_GROUP == DMEM}} {",
            "  lappend n [llength [get_cells -quiet -hier -filter $f]]",
            "}",
            f'puts $out "{top}\\t[join $n \\t]"',
            f"report_utilization -file {top}_utilization.rpt",
            "close_design",
            "close_project -quiet",
        ]
    return "\n".join(lines + ["close $out", ""])


def image(text: str) -> tuple[str, Path]:
    """TAG=ELF."""
    tag, sep, path = text.partition("=")
    if not sep or not tag.isidentifier():
        raise argparse.ArgumentTypeError(f"{text!r} is not TAG=ELF")
    return tag, Path(path)


def main(argv: list[str] | None = None) -> int:
    """Emit both regions of every image, their plans and the Vivado script."""
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("directory", type=Path)
    ap.add_argument("images", type=image, nargs="+", metavar="TAG=ELF")
    args = ap.parse_args(argv)
    args.directory.mkdir(parents=True, exist_ok=True)
    plans, tops = {}, []
    try:
        for tag, elf in args.images:
            linked = ctrl_memory.read_elf(elf)
            plan = ctrl_memory.plan(linked)
            plans[tag] = plan.summary()
            for region, banks, words in ((ctrl_memory.ROM, plan.rom_banks, ctrl_memory.rom_words(linked)),
                                         (ctrl_memory.RAM, plan.ram_banks, None)):
                tops.append(f"{tag}_{region.name}")
                emit(args.directory, tops[-1], Top(region, banks, words))
    except ctrl_memory.Refusal as exc:
        print(f"REFUSED {exc}", file=sys.stderr)
        return 2
    (args.directory / "ctrl_memory_plan.json").write_text(json.dumps(plans, indent=2) + "\n")
    (args.directory / "ctrl_memory_ooc.tcl").write_text(tcl(tops))
    print(json.dumps(plans, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
