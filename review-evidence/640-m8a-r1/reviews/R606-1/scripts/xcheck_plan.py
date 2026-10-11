#!/usr/bin/env python3
"""Reviewer cross-check: recompute each split image's rom/sram need, banks and
tiles from `readelf -S -l -s` output (not ctrl_memory.read_elf), and the as-mapped
tiles from the author's Vivado TSV.  Usage: xcheck_plan.py READELF TSV label=elf..."""
import re, subprocess, sys, math
readelf, tsv = sys.argv[1], sys.argv[2]
mapped = {}
for line in open(tsv).read().splitlines()[1:]:
    top, r36, r18, lut, ff, _ = line.split("\t")
    mapped[top] = (int(r36), int(r18), int(lut), int(ff))
def banks(need):
    g = -(-need // 2048)
    return [2048 << b for b in reversed(range(g.bit_length())) if g >> b & 1]
tot36 = tot18 = 0
for arg in sys.argv[3:]:
    label, elf = arg.split("=", 1)
    s = subprocess.run([readelf, "-W", "-S", "-l", "-s", elf], capture_output=True, text=True, check=True).stdout
    secs = []
    for m in re.finditer(r"\]\s+(\S+)\s+(PROGBITS|NOBITS)\s+([0-9a-f]+)\s+([0-9a-f]+)\s+([0-9a-f]+)\s+\S+\s+(\S*A\S*)", s):
        secs.append((m[1], m[2], int(m[3], 16), int(m[5], 16), m[6]))
    loads = [(int(m[2], 16), int(m[3], 16), int(m[4], 16), int(m[5], 16)) for m in
             re.finditer(r"LOAD\s+0x([0-9a-f]+)\s+0x([0-9a-f]+)\s+0x([0-9a-f]+)\s+0x([0-9a-f]+)\s+0x([0-9a-f]+)", s)]
    rom_end = max(p + f for v, p, f, _ in loads if f)
    ram_end = max(a + z for n, k, a, z, fl in secs if a >= 0x1000_0000)
    entry = int(re.search(r"Entry point 0x([0-9a-f]+)", s)[1], 16)
    stage = [int(m[1]) for m in re.finditer(r"\d+:\s+[0-9a-f]+\s+(\d+)\s+OBJECT\s+\S+\s+\S+\s+\S+\s+nvm_stage$", s, re.M)]
    writable_in_rom = [n for n, k, a, z, fl in secs if a < 0x1000_0000 and "W" in fl]
    rb, sb = banks(rom_end), banks(ram_end - 0x1000_0000)
    tiles = (sum(rb) + sum(sb)) / 4096
    r = mapped[f"{label}_rom"]; m_ = mapped[f"{label}_sram"]
    m36, m18 = r[0] + m_[0], r[1] + m_[1]
    tot36, tot18 = m36, m18
    print(f"{label}: entry=0x{entry:x} rom_need={rom_end} sram_need={ram_end-0x10000000} "
          f"sum={rom_end+ram_end-0x10000000} rom_banks={rb} sram_banks={sb} planned_tiles={tiles} "
          f"mapped={m36}/{m18} mapped_tiles={m36+m18/2} lut={r[2]+m_[2]} ff={r[3]+m_[3]} "
          f"nvm_stage={stage} writable_in_rom={writable_in_rom} within56={tiles<=56}")
