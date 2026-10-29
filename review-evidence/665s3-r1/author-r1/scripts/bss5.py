#!/usr/bin/env python3
"""The five largest .bss objects of a linked platform image, by ctrl_plat_image.py's own largest_bss, read from the
image directory it leaves even when the bank plan refuses the image (the ELF and the member probe are written first).

usage: bss5.py CHECKOUT IMAGE_DIR
"""
import re
import subprocess
import sys
from pathlib import Path

checkout, out = Path(sys.argv[1]), Path(sys.argv[2])
sys.path[:0] = [str(checkout / "sw/firmware/ctrl/test"), str(checkout / "sw/firmware/gtest")]
import ctrl_plat_image  # noqa: E402
import fw_rv32  # noqa: E402

tool = fw_rv32.compiler().removesuffix("gcc")
elf = out / "ctrl_app.elf"
symbols = subprocess.run([tool + "nm", "-S", str(elf)], capture_output=True, text=True, check=True).stdout
size = subprocess.run([tool + "size", "-A", "-x", str(elf)], capture_output=True, text=True, check=True).stdout
sections = {name: (int(addr, 16), int(length, 16))
            for name, length, addr in re.findall(r"^(\.\S+)\s+(0x[0-9a-f]+)\s+(0x[0-9a-f]+)", size, re.M)}
members = {}
probe = subprocess.run([tool + "nm", "-S", str(out / "ctrl_plat_members.o")], capture_output=True, text=True,
                       check=True).stdout
for line in probe.splitlines():
    fields = line.split()
    if len(fields) == 4 and fields[3].startswith("ctrl_plat_member_"):
        members[fields[3].removeprefix("ctrl_plat_member_")] = int(fields[1], 16)
assert set(members) == set(ctrl_plat_image.MEMBERS), sorted(members)
print({name: length for name, (_, length) in sections.items()})
for row in ctrl_plat_image.largest_bss(symbols, sections, members):
    print(f"{row['symbol']} {row['bytes']}")
