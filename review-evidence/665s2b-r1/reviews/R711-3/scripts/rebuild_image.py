#!/usr/bin/env python3
"""Rebuild one harness image at a checkout through its own build.firmware() and print the ELF's sha256.

usage: rebuild_image.py <checkout root> <out dir> <shape> <interfaces> [mutation] [variant]
Compare the printed hash with a measurement leg's image.txt (published packet).
"""
import hashlib
import sys
from pathlib import Path

checkout, out, shape, n_if = sys.argv[1:5]
mutation = sys.argv[5] if len(sys.argv) > 5 else 'none'
variant = sys.argv[6] if len(sys.argv) > 6 else 'none'
sys.path.insert(0, str(Path(checkout) / 'tb/verilator/ctrl_service_budget'))
import build  # noqa: E402

elf = build.firmware(Path(out), shape, int(n_if), mutation, variant)
print(hashlib.sha256(elf.read_bytes()).hexdigest(), shape, n_if, mutation, variant)
