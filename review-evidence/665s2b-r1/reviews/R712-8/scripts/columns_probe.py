#!/usr/bin/env python3
"""Reviewer probe: bind load_grade.COLUMNS wrongly in-process and report whether the load gate's controls refuse it.
Usage: columns_probe.py <repo root>"""
import sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
import load_grade as g
NAME = "a column's name bound to the other's table"
good = g.COLUMNS
cases = {
  'as at the head': good,
  'tables swapped under their names': ((good[0][0], good[1][1]), (good[1][0], good[0][1])),
  'names swapped over their tables': ((good[1][0], good[0][1]), (good[0][0], good[1][1])),
  'the pin table twice': ((good[0][0], good[0][1]), (good[1][0], good[0][1])),
  'the donor column dropped': (good[0],),
  'a copy of the pin table (equal, not the same object)': ((good[0][0], dict(good[0][1])), good[1]),
}
for what, cols in cases.items():
    g.COLUMNS = cols
    esc = g.controls(root)
    print(f"{what}: {'REFUSED' if NAME in esc else 'not refused'} by the binding control; held: {g.held(root)}")
g.COLUMNS = good
