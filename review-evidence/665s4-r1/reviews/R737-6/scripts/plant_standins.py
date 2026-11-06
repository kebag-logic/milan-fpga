#!/usr/bin/env python3
"""Plant RV32 stand-in headers into a disposable copy's image links only.

usage: plant_standins.py CHECKOUT csr,mem

The two image() calls of tb/verilator/ctrl_split_boot/run.py get a copy of the real map whose named headers hold the
stand-ins' bytes: the compile a map lacking them gets from the include path, with the SoC export left on the real map.
"""
import sys
from pathlib import Path

checkout, names = Path(sys.argv[1]), sys.argv[2].split(',')
run = checkout / "tb/verilator/ctrl_split_boot/run.py"
text = run.read_text()
old_first = "first = image(out, 'image-provisional', (shape, n_if), ImageMaps(PROVISIONAL, flash_map), archives)"
old_second = "elf = image(out, 'image', (shape, n_if), ImageMaps(csr_csv, flash_map), archives,"
assert text.count(old_first) == 1 and text.count(old_second) == 1
copies = "".join(f"shutil.copy(ROOT / 'sw/firmware/ctrl_nvm/test/rv32/generated/{name}.h', "
                 f"planted_map / 'generated/{name}.h')\n    " for name in names)
plant = (f"planted_map = out / 'split-soc/flash-map-planted'\n"
         f"    shutil.copytree(flash_map, planted_map, dirs_exist_ok=True)\n    {copies}")
text = text.replace(old_first, plant + old_first.replace("ImageMaps(PROVISIONAL, flash_map)",
                                                         "ImageMaps(PROVISIONAL, planted_map)"))
text = text.replace(old_second, old_second.replace("ImageMaps(csr_csv, flash_map)", "ImageMaps(csr_csv, planted_map)"))
run.write_text(text)
print(f"planted {names} into {run}")
