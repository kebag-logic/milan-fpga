#!/usr/bin/env python3
"""Emit LiteX wishbone.SRAM instances sized for each linked firmware point (M8a memory-fit evidence).

Scratch measurement only; not part of the tree. Each point gets:
  rom_<pt>: read-only SRAM initialised with the ELF's load image (.text, .rodata, .data LMA),
            depth = image words, as LiteX's ROM auto-size gives;
  ram_<pt>: read/write SRAM sized for .data + .bss + .stack;
  uni_<pt>: one read/write SRAM holding the whole span (a loaded-image organisation).
Plus cap50: one read/write SRAM of 50 RAMB36 at 4,096 usable bytes each.
"""
import json
import subprocess
import sys
from pathlib import Path

from migen import ClockDomain
from litex.gen import LiteXModule
from litex.gen.fhdl.verilog import convert
from litex.soc.interconnect import wishbone

FIT = Path(sys.argv[1])
OUT = Path(sys.argv[2])
OBJCOPY = sys.argv[3]
POINTS = [("s1i1", "endstation_ax7101_1x1_tdm8", 1), ("s1i2", "endstation_ax7101_1x1_tdm8", 2),
          ("s8i1", "endstation_ax7101_8x8", 1), ("s8i2", "endstation_ax7101_8x8", 2)]


class Top(LiteXModule):
    def __init__(self, size, read_only=False, init=None):
        self.cd_sys = ClockDomain("sys")
        self.sram = wishbone.SRAM(size, read_only=read_only, init=init)


def emit(name, top):
    bus = top.sram.bus
    ios = {top.cd_sys.clk, top.cd_sys.rst, bus.adr, bus.dat_r, bus.cyc, bus.stb, bus.ack,
           bus.cti, bus.bte, bus.err}
    if not top.sram.bus.mode == "r":
        ios |= {bus.we, bus.sel, bus.dat_w}
    out = convert(top, ios=ios, name=name)
    out.write(str(OUT / f"{name}.v"))


def report(log):
    text = log.read_text()
    return json.loads(text[text.index("{"):])


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    plan = []
    for tag, shape, ifs in POINTS:
        d = FIT / f"img-{shape}-if{ifs}"
        sec = report(FIT / f"img-{shape}-if{ifs}.log")["sections"]
        image = OUT / f"{tag}.bin"
        subprocess.run([OBJCOPY, "-O", "binary", "-j", ".text", "-j", ".rodata", "-j", ".data",
                        str(d / "ctrl_app.elf"), str(image)], check=True)
        data = image.read_bytes()
        data += b"\0" * (-len(data) % 4)
        words = [int.from_bytes(data[i:i + 4], "little") for i in range(0, len(data), 4)]
        ram = sec[".data"] + sec[".bss"] + sec[".stack"]
        ram += -ram % 4
        span = report(FIT / f"img-{shape}-if{ifs}.log")["ram_span"]  # linked span, alignment included
        span += -span % 4
        emit(f"rom_{tag}", Top(len(data), read_only=True, init=words))
        emit(f"ram_{tag}", Top(ram))
        emit(f"uni_{tag}", Top(span))
        plan.append({"tag": tag, "shape": shape, "interfaces": ifs, "sections": sec,
                     "image_bytes": len(data), "rom_bytes": len(data), "ram_bytes": ram,
                     "unified_bytes": span})
    emit("cap50", Top(50 * 4096))
    (OUT / "plan.json").write_text(json.dumps(plan, indent=2))


main()
