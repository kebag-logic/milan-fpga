"""The firmware README's figure check (ctrl_boundary.figures, figure_controls) at a tree, for a given pin-control count.

usage: python3 -B figures_check.py TREE PINS
"""
import sys
from pathlib import Path

tree, pins = Path(sys.argv[1]).resolve(), int(sys.argv[2])
sys.path.insert(0, str(tree / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(tree / "sw/firmware/gtest"))
import ctrl_boundary  # noqa: E402

page = ctrl_boundary.README.read_text(encoding="utf-8")
counts = ctrl_boundary.population(pins)
stated = ctrl_boundary.figures(page, counts)
bad, controls = ctrl_boundary.figure_controls(page, counts)
print(f"population {counts}")
print(f"figure findings {len(stated)}: {stated}")
print(f"figure controls {controls}, misbehaved {bad}")
sys.exit(1 if stated or bad else 0)
