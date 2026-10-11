#!/usr/bin/env python3
"""Reviewer plants, linked by the PR's own ctrl_split.ld and reset entry:
over-budget (120,000 B of .rodata in rom + 110,000 B of .bss in sram: each
region inside its own 224 KiB window, together over 56 RAMB36) and overlap
(.bss placed at ADDR(.data) in an edited copy of the script).
Usage: make_plants.py <repo> <cc> <outdir>"""
import subprocess, sys
from pathlib import Path
repo, cc, out = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
sys.path[:0] = [str(repo / "sw/litex")]
import ctrl_memory
plat = repo / "sw/firmware/ctrl/plat"
script = (plat / "ctrl_split.ld").read_text()
srcs = {
 "over-budget": ("const unsigned char table[120000] = {1};\nunsigned char pool[110000];\n"
                 "unsigned char nvm_stage[3344];\nint counter = 7;\n"
                 "int main(void) { return table[counter] + pool[counter] + nvm_stage[counter] + counter; }\n", script),
 "overlap": ("int counter = 7;\nunsigned char nvm_stage[3344];\n"
             "int main(void) { return counter + nvm_stage[counter]; }\n",
             script.replace(".bss (NOLOAD) : ALIGN(4)", ".bss ADDR(.data) (NOLOAD) : ALIGN(4)")),
}
flags = ["-march=rv32i", "-mabi=ilp32"]
for name, (c, ld) in srcs.items():
    d = out / name; d.mkdir(parents=True, exist_ok=True)
    assert ld != script or name == "over-budget"
    (d / "regions.ld").write_text(ctrl_memory.regions_ld())
    (d / "p.c").write_text(c); (d / "split.ld").write_text(ld)
    subprocess.run([cc, *flags, "-ffreestanding", "-O1", "-c", str(d / "p.c"), "-o", str(d / "p.o")], check=True)
    subprocess.run([cc, *flags, "-c", str(plat / "ctrl_split_start.S"), "-o", str(d / "s.o")], check=True)
    subprocess.run([cc, *flags, "-nostdlib", "-static", "-no-pie", "-Wl,--build-id=none", "-T", str(d / "split.ld"),
                    f"-L{d}", str(d / "s.o"), str(d / "p.o"), "-o", str(d / "plant.elf")], check=True)
    try:
        ctrl_memory.plan(ctrl_memory.read_elf(d / "plant.elf")); print(name, "plan: ACCEPTED")
    except ctrl_memory.Refusal as e:
        print(name, f"plan: REFUSED [{e.check}] {e}")
