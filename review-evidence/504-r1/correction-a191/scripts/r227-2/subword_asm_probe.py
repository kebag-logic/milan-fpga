#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Compile the byte-overwrite plant shape with the census flags and show what
the head resolver reports for it (R227-2, issue #504 / PR #521).

Usage: subword_asm_probe.py <checkout-root> <sdk-prefix> <workdir>
"""
import importlib.util, subprocess, sys
from pathlib import Path

root, sdk, work = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
work.mkdir(parents=True, exist_ok=True)
src = work / "subword.c"
src.write_text(
    "#include <stdint.h>\n"
    "typedef struct { volatile uint32_t ctrl; } *probe_r227_blk;\n"
    "static unsigned int probe_r227_page = 0x9000u;\n"
    "void configure_fabric(void)\n{\n"
    "\t{\n\t\tunion { uint32_t w; uint8_t b; } milan_u;\n"
    "\t\tmilan_u.w = (probe_r227_page << 16) | 0x600u;\n"
    "\t\tmilan_u.b = 0u;\n"
    "\t\t((probe_r227_blk)milan_u.w)->ctrl = 1u;\n\t}\n}\n")
asm = work / "subword.s"
subprocess.run([str(sdk / "bin/riscv32-linux-gcc"), "-std=gnu99", "-O0", "-fno-inline",
                "-S", "-o", str(asm), str(src)], check=True)
spec = importlib.util.spec_from_file_location("tb", root / "sw/builder/test_builder.py")
tb = importlib.util.module_from_spec(spec); spec.loader.exec_module(tb)
text = asm.read_text()
body = tb.rv32_functions(text)["configure_fabric"]
print("emitted configure_fabric():")
for _label, mnem, ops in body:
    if mnem:
        print(f"\t{mnem}\t{ops}")
unit = tb.rv32_unit(text)
stores = [a for _at, (a, _v) in unit["runs"]["configure_fabric"]["stores"]]
print("resolver-reported store addresses:", [hex(a) if isinstance(a, int) else repr(a) for a in stores])
print("real target of the last store: 0x90000600 (ADP_CTRL; the byte write keeps low byte 0x00)")
