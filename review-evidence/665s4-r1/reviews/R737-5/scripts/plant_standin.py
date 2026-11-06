#!/usr/bin/env python3
"""Plant one RV32 stand-in header into a disposable copy's image links only.

usage: plant_standin.py CHECKOUT csr|mem

The two image() calls of tb/verilator/ctrl_split_boot/run.py get a copy of the real map whose named header holds the
stand-in's bytes: the compile a map lacking that header gets from the include path, with the SoC export left on the
real map. The refusal cannot see it, because the header is there.
"""
import sys
from pathlib import Path

checkout, name = Path(sys.argv[1]), sys.argv[2]
run = checkout / "tb/verilator/ctrl_split_boot/run.py"
text = run.read_text()
old_first = "first = image(out, 'image-provisional', (shape, n_if), ImageMaps(PROVISIONAL, flash_map), archives)"
old_second = "elf = image(out, 'image', (shape, n_if), ImageMaps(csr_csv, flash_map), archives,"
assert text.count(old_first) == 1 and text.count(old_second) == 1
plant = (f"planted_map = out / 'split-soc/flash-map-planted'\n"
         f"    shutil.copytree(flash_map, planted_map, dirs_exist_ok=True)\n"
         f"    shutil.copy(ROOT / 'sw/firmware/ctrl_nvm/test/rv32/generated/{name}.h', "
         f"planted_map / 'generated/{name}.h')\n    ")
text = text.replace(old_first, plant + old_first.replace("ImageMaps(PROVISIONAL, flash_map)",
                                                         "ImageMaps(PROVISIONAL, planted_map)"))
text = text.replace(old_second, old_second.replace("ImageMaps(csr_csv, flash_map)", "ImageMaps(csr_csv, planted_map)"))
run.write_text(text)
print(f"planted {name}.h into {run}")
