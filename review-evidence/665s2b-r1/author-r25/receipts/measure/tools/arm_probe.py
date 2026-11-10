#!/usr/bin/env python3
"""Scratch: link a harness point's image (optionally a variant arm) from a checkout against a given flash map, as
build.firmware does, and print its rom and the ledger's verdict. usage: arm_probe.py CHECKOUT OUT SHAPE N_IF VARIANT FLASH_MAP"""
import sys, subprocess
from pathlib import Path
ck, out, shape, n_if, variant, fmap = Path(sys.argv[1]).resolve(), Path(sys.argv[2]), sys.argv[3], int(sys.argv[4]), sys.argv[5], Path(sys.argv[6])
sys.path.insert(0, str(ck / 'tb/verilator/ctrl_service_budget'))
import build
try:
    elf = build.firmware(out, shape, n_if, variant=variant, flash_map=fmap)
    print('ELF', elf)
except Exception as e:  # the ledger refusal surfaces as the image step's failure
    print('FAILED', type(e).__name__, e)
log = (out / 'image.log')
if log.exists():
    for line in log.read_text().splitlines():
        if any(w in line for w in ('rom', 'REFUSED', 'RAMB36', 'tiles', 'bytes')):
            print(line[:300])
