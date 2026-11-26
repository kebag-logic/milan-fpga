#!/usr/bin/env python3
"""Reviewer control: the boundary judge's text half (ctrl_configs.held's builder_texts loop) at a checkout:
programs naming the firmware's tree that no list accounts for. Usage: boundary_scan.py CHECKOUT"""
import sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
import ctrl_configs as c
names = {b.path for b in c.BUILDERS}
left = [c.rel(p) for p, t in c.builder_texts(None).items()
        if not (c.rel(p) in names or c.rel(p) in c.OUTSIDE or c.rel(p) in c.SUITES or c.rel(p) in c.PART_OF)
        and c.program(p, t)]
print("unlisted programs naming the firmware's tree:", left or "none")
sys.exit(1 if left else 0)
