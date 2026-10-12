#!/usr/bin/env python3
"""Run the pin proof's standing controls (ctrl_pin.pin_controls) alone, as ctrl_boundary.py --selftest runs them.

usage: pin_controls.py <tree> <work directory>
Exit 0 iff no control misbehaved.
"""
import platform
import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
work = Path(sys.argv[2]).resolve()
sys.path[:0] = [str(tree / "sw/firmware/ctrl/test"), str(tree / "sw/firmware/gtest")]

import ctrl_boundary  # noqa: E402
import ctrl_pin  # noqa: E402

print(f"python {platform.python_version()} tree {tree}")
work.mkdir(parents=True, exist_ok=True)
bad, count = ctrl_pin.pin_controls(work, ctrl_boundary.makefiles())
print(f"pin controls: {count}, misbehaved: {bad}")
sys.exit(1 if bad else 0)
