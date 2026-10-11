#!/usr/bin/env python3
"""Reviewer probe: link the PR's own probe program with the PR's ctrl_split.ld,
edited so .data (writable, initialised) is placed in rom (`} > rom` instead of
`} > sram AT > rom`), and ask ctrl_memory.plan whether it accepts the image.
Usage: probe_writable_rom.py <repo> <cc> <workdir>"""
import sys
from pathlib import Path
repo, cc, work = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
sys.path[:0] = [str(repo / "sw/litex"), str(repo / "sw/firmware/gtest")]
import ctrl_memory
import test_ctrl_memory as t
script = (repo / "sw/firmware/ctrl/plat/ctrl_split.ld").read_text()
assert "} > sram AT > rom" in script
work.mkdir(parents=True, exist_ok=True)
for label, edit in (("head script", script), ("data in rom", script.replace("} > sram AT > rom", "} > rom"))):
    d = work / label.replace(" ", "-"); d.mkdir(exist_ok=True)
    img = ctrl_memory.read_elf(t.link(cc, d, edit))
    secs = {s.name: (hex(s.vma), hex(s.lma), s.size, s.loaded) for s in img.sections}
    try:
        p = ctrl_memory.plan(img)
        print(f"{label}: ACCEPTED plan rom={p.rom_bytes} sram={p.ram_bytes} sections={secs}")
    except ctrl_memory.Refusal as e:
        print(f"{label}: REFUSED {e.check}: {e}")
