#!/usr/bin/env python3
"""ledger_table.py: the area plan's firmware ledger rows at the four points, from each point's size.json and
symbols.txt (ctrl_plat_image.py) and the out-of-context mapping (ctrl_memory_ooc.py plan json and tsv)."""
import csv, json, sys
from pathlib import Path
S = Path("<scratch>")
POINTS = (("s1i1", "1x1-1if", "1x1, one interface (shipping)"), ("s1i2", "1x1-2if", "1x1, two interfaces"),
          ("s8i1", "8x8-1if", "8x8, one interface"), ("s8i2", "8x8-2if", "8x8, two interfaces (largest)"))
plans = json.loads((S / "memooc/ctrl_memory_plan.json").read_text())
tsv = {r["top"]: r for r in csv.DictReader(open(S / "memooc/ctrl_memory_ooc.tsv"), delimiter="\t")}
out = {}
for tag, d, label in POINTS:
    size = json.loads((S / "ledger" / d / "size.json").read_text())
    syms = {}
    for line in (S / "ledger" / d / "symbols.txt").read_text().splitlines():
        f = line.split()
        if len(f) == 4:
            syms[f[3]] = int(f[1], 16)
    sec = size["sections"]
    plan = plans[tag]
    rom, ram = tsv[f"{tag}_rom"], tsv[f"{tag}_sram"]
    r36 = int(rom["RAMB36E1"]) + int(ram["RAMB36E1"]); r18 = int(rom["RAMB18E1"]) + int(ram["RAMB18E1"])
    usable = sum(plan["rom"]["banks"]) + sum(plan["sram"]["banks"])
    need = plan["rom"]["bytes"] + plan["sram"]["bytes"]
    spans = sec[".text"] + sec[".rodata"] + sec[".data"] + sec[".bss"] + sec[".stack"]
    out[d] = dict(label=label, text=sec[".text"], rodata=sec[".rodata"], data=sec[".data"], bss=sec[".bss"],
                  stack=sec[".stack"], pool=syms["arena"], stage=syms["nvm_stage"],
                  descriptor_values=syms["values"], descriptors=syms.get("descriptors"),
                  rom_need=plan["rom"]["bytes"], sram_need=plan["sram"]["bytes"],
                  # rom holds .text, .rodata and .data's initial bytes; sram .data, .bss and the stack
                  alignment=need - spans - sec[".data"],
                  planned_tiles=plan["tiles"], mapped_ramb36=r36, mapped_ramb18=r18, mapped_tiles=r36 + r18 / 2,
                  mapped_lut=int(rom["LUT"]) + int(ram["LUT"]), mapped_ff=int(rom["FF"]) + int(ram["FF"]),
                  usable=usable, unused_in_banks=usable - need, budget_left_tiles=56 - (r36 + r18 / 2),
                  largest_bss=[(b["symbol"], b["bytes"]) for b in size["largest_bss"]],
                  ledgered=plan.get("ledgered"))
json.dump(out, sys.stdout, indent=1)
print()
