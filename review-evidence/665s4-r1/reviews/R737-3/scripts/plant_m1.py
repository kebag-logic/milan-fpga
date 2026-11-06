"""Plant M1 in a disposable tree: the final link compiles the flash port on the RV32 stand-ins.

The provisional link and both exports keep the generated map, so the only change is a
placeholder image on the generated SoC. It asks whether ctrl_split_boot can tell.
usage: plant_m1.py <tree>
"""
import sys
from pathlib import Path

path = Path(sys.argv[1]) / 'tb/verilator/ctrl_split_boot/run.py'
text = path.read_text()
old = "'--flash-map', str(maps.flash_map), '--output', str(out / name),"
new = "*([] if name == 'image' else ['--flash-map', str(maps.flash_map)]), '--output', str(out / name),"
if text.count(old) != 1:
    raise SystemExit(f'anchor occurs {text.count(old)} times')
path.write_text(text.replace(old, new))
print('planted M1 in', path)
