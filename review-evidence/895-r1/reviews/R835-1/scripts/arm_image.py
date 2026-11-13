#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer-owned: link one CPU budget harness arm's image at 8x8/2if with the harness's own builder (build.firmware),
then print its plan (size.json). Usage: arm_image.py TREE VARIANT FLASH_MAP OUT"""
import json
import sys
from pathlib import Path

tree, variant, flash_map, out = Path(sys.argv[1]).resolve(), sys.argv[2], Path(sys.argv[3]), Path(sys.argv[4])
sys.path.insert(0, str(tree / 'tb/verilator/ctrl_service_budget'))
import build  # noqa: E402

elf = build.firmware(out, 'endstation_ax7101_8x8', 2, variant=variant, flash_map=flash_map)
s = json.loads((elf.parent / 'size.json').read_text())['split']
print(f"{variant} 8x8/2if rom={s['rom']['bytes']} sram={s['sram']['bytes']} tiles={s['tiles']} "
      f"rom_banks={sum(s['rom']['banks'])} sram_banks={sum(s['sram']['banks'])}")
