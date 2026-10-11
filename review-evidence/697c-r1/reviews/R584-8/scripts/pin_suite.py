#!/usr/bin/env python3
"""Run the pin proof's own standing checks of a milan-fpga checkout, without builds:
the CLI pin check, the census, the README figure check with its controls, and every
pin control (ctrl_pin.pin_controls). Usage: pin_suite.py <checkout> <scratch-dir>"""
import sys
from pathlib import Path

root, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(root / "sw/firmware/gtest"))
import ctrl_build  # noqa: E402
import ctrl_pin  # noqa: E402
import ctrl_boundary  # noqa: E402
from ctrl_configs import makefiles  # noqa: E402

print("pin:", ctrl_build.stack_pin())
census = ctrl_pin.proof_census()
print("census findings:", census)
work.mkdir(parents=True, exist_ok=True)
bad, n = ctrl_pin.pin_controls(work, makefiles())
page = ctrl_boundary.README.read_text(encoding="utf-8")
pop = ctrl_boundary.population(n)
print("population:", pop)
stated = ctrl_boundary.figures(page, pop)
print("figure findings:", stated)
fbad, fn = ctrl_boundary.figure_controls(page, pop)
print(f"pin controls {n}, misbehaved {bad}; figure controls {fn}, misbehaved {fbad}")
sys.exit(1 if bad or fbad or census or stated else 0)
