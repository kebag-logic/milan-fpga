#!/usr/bin/env python3
"""R570-4 disposable probes of the #621 step regression (tb/verilator/gptp_plane).

Writes a generator variant into <out>/<arm>/gen_gptp_ucode.py:
  orig         the original donor generator (5dce647a), copied as is
  no-pdstep    the servo step no longer sets S_PDSTEP (anchor: the MOVE/WRST pair)
  clear-nrr    the servo step also clears the retained ratio S_NRR
Usage: python3 -I probe_phc_step_plants.py <head generator> <orig generator> <out dir>
Then run: python3 tb/verilator/gptp_plane/phc_step.py --generator <variant> --work <dir>
"""
import sys
from pathlib import Path

head, orig, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
src = head.read_text()
pd = ('    p.emit("MOVE", rd=RT, ra=0, imm=1)\n'
      '    p.emit("WRST", ra=RT, imm=RG_SCR | S_PDSTEP, fmt=FMT_Q)\n')
nr3 = '    p.emit("WRST", ra=0, imm=RG_SCR | S_NR3, fmt=FMT_Q)\n'
assert src.count(pd) == 1 and src.count(nr3) == 1
arms = {
    "orig": orig.read_text(),
    "no-pdstep": src.replace(pd, ""),
    "clear-nrr": src.replace(nr3, nr3 + '    p.emit("WRST", ra=0, imm=RG_SCR | S_NRR, fmt=FMT_Q)\n'),
}
for name, text in arms.items():
    d = out / name
    d.mkdir(parents=True, exist_ok=True)
    (d / "gen_gptp_ucode.py").write_text(text)
    print(name, d / "gen_gptp_ucode.py")
