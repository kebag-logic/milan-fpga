#!/usr/bin/env python3
"""Reviewer probe: the two ctrl_boundary judgements the hosted firmware jobs failed on, without the builds.

Usage: python3 ctrl_boundary_probe.py <repo-root> <scratch-dir>
1. Every file ctrl_configs.builder_texts() finds naming the firmware's tree that
   is a program and is none of BUILDERS, PART_OF, OUTSIDE or SUITES: the
   condition held() refuses by name (firmware-boundary's REFUSED line).
2. ctrl_pin.pin_controls() over ctrl_configs.makefiles(): the pin-control
   count the self-test compares with sw/firmware/ctrl/README.md's figure
   (firmware-verilator's FAIL line), beside the README's stated figure.
"""
import re
import sys
from pathlib import Path

root, scratch = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
import ctrl_configs as cc  # noqa: E402
from ctrl_pin import pin_controls  # noqa: E402

names = {b.path for b in cc.BUILDERS}
print("1. programs naming the firmware's tree that no list classifies:")
n = 0
for path, text in cc.builder_texts().items():
    name = cc.rel(path)
    if name in names or name in cc.OUTSIDE or name in cc.SUITES or name in cc.PART_OF:
        continue
    if cc.program(path, text):
        hit = [ln.strip() for ln in text.splitlines() if "sw/firmware/ctrl" in ln][:2]
        print(f"   UNCLASSIFIED PROGRAM {name}: {hit}")
        n += 1
print(f"   {n} unclassified")
work = scratch / "pins"
work.mkdir(parents=True, exist_ok=True)
misbehaved, pins = pin_controls(work, cc.makefiles())
page = (root / "sw/firmware/ctrl/README.md").read_text()
m = re.search(r"(\d+) pin controls follow the boundary controls", page)
print(f"2. pin controls: the self-test's {pins} (misbehaved {misbehaved}); the README states {m.group(1) if m else None}")
