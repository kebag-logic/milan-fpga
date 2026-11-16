#!/usr/bin/env python3
"""util.py <route dir>...: the placed utilisation (alinx_ax7101_utilization_place.rpt) of each route directory, in
the columns of the #810 route report: Slice LUT, LUTRAM, FF, Slice, BRAM tiles (RAMB36 / RAMB18), DSP, CARRY4."""
import re
import sys
from pathlib import Path


def cell(text: str, name: str) -> str:
    m = re.search(r'^\|\s*' + re.escape(name) + r'\s*\|\s*([0-9.]+)\s*\|', text, re.M)
    return m.group(1) if m else '?'


for d in sys.argv[1:]:
    t = (Path(d) / 'alinx_ax7101_utilization_place.rpt').read_text(errors='replace')
    lut = cell(t, 'Slice LUTs')
    if lut == '?':
        lut = cell(t, 'Slice LUTs*')
    print(f"{d}: LUT {lut}, LUTRAM {cell(t, 'LUT as Memory')}, FF {cell(t, 'Slice Registers')}, "
          f"Slice {cell(t, 'Slice')}, BRAM {cell(t, 'Block RAM Tile')} ({cell(t, 'RAMB36/FIFO*')} / "
          f"{cell(t, 'RAMB18')}), DSP {cell(t, 'DSPs')}, CARRY4 {cell(t, 'CARRY4')}")
