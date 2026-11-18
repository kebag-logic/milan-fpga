#!/usr/bin/env python3
"""Build the CPU budget harness's split firmware image of one (point, arm) at a clone's head, as build.build does
before the SoC and the native model (its flash map, then the image), and print ctrl_app.elf's sha256.
usage: fwimage.py <clone> <out> <point: 1x1 | 8x8-1if | 8x8> <arm: none | answering-every-port | answering-ports |
valid-destinations>"""
import hashlib
import sys
from pathlib import Path

clone, out, point, arm = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3], sys.argv[4]
sys.path.insert(0, str(clone / 'tb/verilator/ctrl_service_budget'))
sys.dont_write_bytecode = True
import build  # noqa: E402
import run  # noqa: E402
import split_soc  # noqa: E402
shape, n_if = run.POINTS[point]
out.mkdir(parents=True, exist_ok=True)
flash = build.flash_map(out / split_soc.FLASH_MAP, shape)
elf = build.firmware(out, shape, n_if, 'none', arm, flash)
print(f'{point} {arm} {hashlib.sha256(elf.read_bytes()).hexdigest()}')
