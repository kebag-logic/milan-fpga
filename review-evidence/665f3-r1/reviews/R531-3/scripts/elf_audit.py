#!/usr/bin/env python3
"""Audit linked images independently of the section-size reporter."""
import hashlib
from pathlib import Path
import re
import subprocess
import sys
out, prefix = Path(sys.argv[1]), sys.argv[2]
bad = 0
for elf in sorted(out.glob("*/*/ctrl_app.elf")):
    print("IMAGE", elf.relative_to(out), "sha256", hashlib.sha256(elf.read_bytes()).hexdigest())
    hdr = subprocess.check_output([prefix + "readelf", "-h", "-l", "-S", "-W", "-A", str(elf)], text=True)
    undefined = subprocess.check_output([prefix + "nm", "-u", str(elf)], text=True)
    print(hdr)
    print("Undefined symbols:", undefined.strip() or "NONE")
    assert "EXEC (Executable file)" in hdr and "ELF32" in hdr and "RISC-V" in hdr and not undefined.strip()
    arches = re.findall(r'Tag_RISCV_arch: "([^"]+)"', hdr)
    valid = len(arches) == 1 and re.fullmatch(r"rv32i\d+p\d+", arches[0]) is not None
    print("RV32I attribute check:", "PASS" if valid else "FAIL")
    dis = subprocess.check_output([prefix + "objdump", "-d", str(elf)], text=True)
    symbol = ""
    forbidden = []
    for line in dis.splitlines():
        if re.match(r"^[0-9a-f]+ <.*>:$", line):
            symbol = line
        if re.search(r"\t(?:mul|mulh|mulhu|mulhsu|div|divu|rem|remu|amo\w+|lr\.w|sc\.w)\s", line):
            forbidden.append((symbol, line.strip()))
    print("M/A instructions:", len(forbidden))
    for pair in forbidden:
        print(*pair, sep=" : ")
    print("Call sites of affected helpers:")
    for line in dis.splitlines():
        if re.search(r"(?:jal|jalr).*<__(?:udivdi3|umoddi3|muldi3)>", line):
            print(line)
    print("Library provenance from link map:")
    for line in elf.with_suffix(".map").read_text().splitlines()[:30]:
        print(line)
    bad += not valid or bool(forbidden)
print("RV32I audit failed images:", bad)
sys.exit(bool(bad))
